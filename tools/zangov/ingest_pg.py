import json
from collections import defaultdict
from time import sleep

from httpx import HTTPStatusError
from sqlmodel import Session, select, SQLModel

from .client import get_document_versions, get_document, iterate_documents
from .enums import ActTypeEnum
from .models import Act, engine, ActType, ActVersion, ActContent
from .schemas import MultiLangDocument

ACT_TYPES = {}

TROUBLED_CODES = [
    "2574",  # ru/kz разные документы
]


ACT_TYPES_TO_INGEST = [
    ActTypeEnum.KONS,
    ActTypeEnum.KZAK,
    ActTypeEnum.KOD,
    ActTypeEnum.ZAK,
    ActTypeEnum.UZAK,
    ActTypeEnum.UKAZ,
    ActTypeEnum.UKON,
    ActTypeEnum.NPOS,
    ActTypeEnum.POST,
    ActTypeEnum.PRIK,
    ActTypeEnum.RASP,
    ActTypeEnum.RESH,
]


def init_db(recreate=False):
    if recreate:
        SQLModel.metadata.drop_all(engine)

    SQLModel.metadata.create_all(engine, checkfirst=True)

    # create act types if not created yet, and cache them all
    with Session(engine) as session:
        for at_enum in ActTypeEnum:
            at = session.exec(
                select(ActType).where(ActType.code == at_enum.value)
            ).first()
            if not at:
                at = ActType(code=at_enum.value)
                session.add(at)
                session.commit()
                session.refresh(at)
            ACT_TYPES[at.code] = at


def get_latest_documents(doc_id: str):
    try:
        # not every document has kazakh language version
        kz = get_document(doc_id, "kaz")
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            kz = None
        else:
            raise

    try:
        # russian documents are more widespread, but also could be missing
        ru = get_document(doc_id, "rus")
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            ru = None
        else:
            raise

    return ru, kz


def construct_act_version(version_docs: MultiLangDocument):
    av = ActVersion(
        date=version_docs.version_date, is_actual=version_docs.actual_version
    )

    if version_docs.version.cause:
        # ensure it to be equal among languages, if present in both
        codes = {
            doc.version.cause.code for doc in version_docs.docs if doc.version.cause
        }
        if len(codes) > 1:
            raise ValueError(f"cause codes mismatch: {codes}")

        av.cause_act_code = version_docs.version.cause.code

    for doc in version_docs.docs:
        ac = ActContent(
            language=doc.language,
            version_id=doc.version.id,
            content=json.dumps(doc.content, ensure_ascii=False),
        )
        av.contents.append(ac)

    return av


def construct_act(doc_id: str) -> Act | None:
    """
    Construct a single act, together with its versions and language contents.

    Do not follow cause documents, write them as a string into an act version instead.
        We will link them together as a second step when all acts are here.
    """
    ru, kz = get_latest_documents(doc_id)
    if not (ru or kz):
        print(doc_id, "no documents found")
        return None

    ml_act = MultiLangDocument(kaz=kz, rus=ru)

    act = Act(
        code=ml_act.code,
        sa_doc_number_ru=ml_act.rus.metadata.state_agency_doc_number
        if ml_act.rus
        else "",
        sa_doc_number_kz=ml_act.kaz.metadata.state_agency_doc_number
        if ml_act.kaz
        else "",
        ju_doc_number=ml_act.metadata.judiciary_doc_number,
        ngr=ml_act.ngr,
        status=ml_act.metadata.status,
        sa_approval_date=ml_act.metadata.state_agency_approval_date,
        ju_approval_date=ml_act.metadata.judiciary_approval_date,
        action_date=ml_act.metadata.action_date,
        effective_date=ml_act.metadata.effective_date,
        types=[ACT_TYPES[_type] for _type in ml_act.metadata.act_types],
        title=ml_act.metadata.title.rus,
        requisite=ml_act.metadata.requisites.rus,
    )

    # collect act versions. Structure of ver_lang_doc:
    # {
    #    "2020-01-01": {
    #        "rus": {...} | None,
    #        "kaz": {...} | None
    #    }
    # }
    ver_lang_doc = defaultdict(dict)
    for doc in ml_act.docs:
        lang_versions = get_document_versions(doc.id, doc.language)[:-1]
        lang_versions.append(doc)  # latest actual version
        for v in lang_versions:
            doc_version = get_document(doc.id, doc.language, v.version_date)
            ver_lang_doc[v.version_date][v.language] = doc_version
            sleep(0.2)  # api precaution

    for version_date, docs in ver_lang_doc.items():
        ml_doc = MultiLangDocument(**docs)
        act_version = construct_act_version(ml_doc)
        act.versions.append(act_version)

    return act


def ingest_all(recreate: bool, start_page: int = 1):
    init_db(recreate=recreate)

    follow_page = start_page
    with Session(engine) as session:
        for page, doc_meta in iterate_documents(
            start_page, per_page=20, act_types=ACT_TYPES_TO_INGEST
        ):
            if page > follow_page:
                # next page event
                # commit flushed batch of `per_page` amount of acts
                session.commit()
                print("page", follow_page, "committed", flush=True)
                follow_page = page

            if doc_meta.id in TROUBLED_CODES:
                print(f"Skipping {doc_meta.id}")
                continue

            act = session.exec(select(Act).where(Act.code == doc_meta.id)).first()
            if act:
                print(doc_meta.id, "already ingested")
                continue

            print("page", page, "act", doc_meta.id, end="\r", flush=True)
            try:
                act = construct_act(doc_meta.id)
            except Exception as e:
                print(f"Failed to construct act {doc_meta.id}")
                raise

            if act:  # a constructed act
                session.add(act)
                session.flush()

        session.commit()
        print("final page committed")

    return None

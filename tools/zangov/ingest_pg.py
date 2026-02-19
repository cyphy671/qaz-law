import json
from datetime import date

from httpx import HTTPStatusError
from sqlmodel import Session, select, SQLModel

from .client import get_document_versions, get_document, iterate_documents
from .enums import ActTypeEnum
from .models import Act, engine, ActType, ActVersion
from .schemas import MultiLangDocument, Document

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


def construct_act_version(doc: Document):
    # ensure actual_version is the same for all languages
    #
    # NOTE there are documents that have different actual versions by a language.
    # example https://zan.gov.kz/client/#!/history/429/rus
    # so actual_version should belong to the content, not version.
    # the question is - is it a bug or
    #
    # assert len({doc.actual_version for doc in version_docs.docs}) == 1

    av = ActVersion(
        date=doc.version_date,
        language=doc.language,
        is_actual=doc.actual_version,
        version_id=doc.version.id,
        content=json.dumps(doc.content, ensure_ascii=False),
    )
    if doc.version.cause and doc.version.cause.code:
        av.cause_act_code = doc.version.cause.code
    return av


def construct_act(doc_id: str, s: Session) -> Act | None:
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
    s.add(act)
    s.flush()

    for doc in ml_act.docs:
        versions = get_document_versions(doc.id, doc.language)

        # should be unique by date and language
        dedup_versions: dict[tuple[str, date], Document] = {}
        for v in versions:
            key = (v.language, v.version_date)
            if key not in dedup_versions:
                dedup_versions[key] = v

        v_docs = []
        for v in dedup_versions.values():
            v_doc = get_document(doc.id, doc.language, v.version_date)
            v_docs.append(v_doc)

        for v_doc in v_docs:
            act.versions.append(construct_act_version(v_doc))
            s.flush()  # make flush for every version to avoid sending a huge data packet on commit

    return act


def ingest_all(recreate: bool, start_page: int = 1):
    init_db(recreate=recreate)

    with Session(engine) as session:
        for page, doc_meta in iterate_documents(
            start_page, per_page=20, act_types=ACT_TYPES_TO_INGEST
        ):
            if doc_meta.id in TROUBLED_CODES:
                print(f"Skipping {doc_meta.id}")
                continue

            act = session.exec(select(Act).where(Act.code == doc_meta.id)).first()
            if act:
                print(doc_meta.id, "already ingested")
                continue

            print("page", page, "act", doc_meta.id, end="\r", flush=True)
            try:
                act = construct_act(doc_meta.id, session)
                if act:  # a constructed and flushed act
                    session.commit()

            except Exception as e:
                print(f"Failed to ingest act {doc_meta.id}: {e}")
                return doc_meta

    return None

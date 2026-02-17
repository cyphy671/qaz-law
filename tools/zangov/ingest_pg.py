from httpx import HTTPStatusError
from pydantic import ValidationError
from sqlmodel import Session, select, SQLModel
import json

from .client import get_document_versions, get_document, iterate_documents
from .enums import ActTypeEnum
from .md import document_to_md
from .models import Act, engine, ActType, ActVersion, ActContent
from .schemas import MultiLangAct, Document

ACT_TYPES = {}

TROUBLED_CODES = [
    "2574",  # ru/kz разные документы
    # "191",  # ru/kz разные state_agency_approval_date
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
        SQLModel.metadata.create_all(engine)

    # create act types if not created yet
    with Session(engine) as session:
        for at_enum in ActTypeEnum:
            at = session.exec(select(ActType).where(ActType.code == at_enum.value)).first()
            if not at:
                at = ActType(code=at_enum.value)
                session.add(at)
                session.commit()
                session.refresh(at)
            ACT_TYPES[at.code] = at


def ingest_act_version_content(s: Session, act_version: ActVersion, doc: Document, cause_path: list[str]):
    global sideloaded
    # first try to convert content
    # markdown = document_to_md(doc)

    if doc.version.cause and not act_version.cause_act_id:
        # recursively ingest the causing act for the version
        if doc.version.cause.code == doc.id:
            # cause can link to itself, this is wrong, and we treat it as if it has no cause
            print(doc.id, "causes itself, ignoring")
        else:
            cause_act = s.exec(select(Act).where(Act.code == doc.version.cause.code)).first()
            if not cause_act:
                cause_act = ingest_act(s, doc.version.cause.code, cause_path=cause_path)
                if cause_act:
                    s.add(cause_act)
                    s.commit()
                    sideloaded += 1
                    # print(cause_act.code, 'committed as cause act')
                    act_version.cause_act_id = cause_act.id

    ac = ActContent(
        language=doc.language,
        version_id=doc.version.id,
        content=json.dumps(doc.content, ensure_ascii=False),
    )
    act_version.contents.append(ac)


sideloaded = 0


def ingest_act(s: Session, doc_id: str, cause_path: list[str] | None = None) -> Act | None:
    global sideloaded
    # to see how long the cause path
    if not cause_path:
        sideloaded = 0
        cause_path = []
    cause_path.append(doc_id)
    cause_path_str = " > ".join(cause_path)

    act = s.exec(select(Act).where(Act.code == doc_id)).first()
    if act:
        # already ingested
        print(doc_id, "already ingested")
        return None

    print(cause_path_str, end="\r", flush=True)
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

    if not (kz or ru):
        print(doc_id, "no documents found, skipping")
        return None

    ml_act = MultiLangAct(kaz=kz, rus=ru)

    act = Act(
        code=ml_act.code,
        sa_doc_number_ru=ml_act.rus.metadata.state_agency_doc_number if ml_act.rus else "",
        sa_doc_number_kz=ml_act.kaz.metadata.state_agency_doc_number if ml_act.kaz else "",
        ju_doc_number=ml_act.metadata.judiciary_doc_number,
        ngr=ml_act.ngr,
        status=ml_act.metadata.status,
        # approval_place=ml_act.approval_place,
        # classified=ml_act.classified,
        # developing_state_agency=ml_act.developing_state_agency,
        # judicial_authority=ml_act.judicial_authority,
        # legal_validity=ml_act.legal_validity,
        registry_number=ml_act.metadata.registry_number,
        sa_approval_date=ml_act.metadata.state_agency_approval_date,
        ju_approval_date=ml_act.metadata.judiciary_approval_date,
        action_date=ml_act.metadata.action_date,
        effective_date=ml_act.metadata.effective_date,
        types=[ACT_TYPES[_type] for _type in ml_act.metadata.act_types],
        title=ml_act.metadata.title.rus,
        requisite=ml_act.metadata.requisites.rus,
    )

    # ingest act versions, together with causing acts
    act_versions = {}
    for doc in [ml_act.rus, ml_act.kaz]:
        if not doc:
            continue
        if doc.versions_count <= 1:
            # the act has the only version
            continue

        act_contents = [doc]
        # all versions, except the actual version that we already have
        other_versions = get_document_versions(doc.id, doc.language)[:-1]
        for v in other_versions:
            doc_v = get_document(doc_id, doc.language, v.version_date)
            act_contents.append(doc_v)

        # deduplicate versions by date
        act_contents = sorted({v.version_date: v for v in act_contents}.values(), key=lambda v: v.version_date)

        for doc_v in act_contents:
            # pre-create act versions, because they are shared between ml_act.rus and ml_act.kaz content versions
            if doc_v.version_date not in act_versions:
                act_versions[doc_v.version_date] = ActVersion(
                    date=doc_v.version_date,
                    is_actual=doc_v.actual_version
                )

            ingest_act_version_content(s, act_versions[doc_v.version_date], doc_v, cause_path=cause_path[:])

    for act_version in act_versions.values():
        act.versions.append(act_version)

    return act


def ingest_all(start_page: int = 1):
    init_db(recreate=True)

    with Session(engine) as session:
        for doc_meta in iterate_documents(start_page, act_types=ACT_TYPES_TO_INGEST):
            if doc_meta.id in TROUBLED_CODES:
                print(f"Skipping {doc_meta.id}")
                continue
            try:
                act = ingest_act(session, doc_meta.id)
                if act:
                    session.add(act)
                    session.commit()
                    print(act.code, "committed", f"({sideloaded} sideloaded)")
            except ValidationError:
                raise
            except Exception as e:
                print(f"Error processing {doc_meta.id}: {e}")
                return doc_meta

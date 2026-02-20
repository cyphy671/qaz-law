import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from datetime import date

from httpx import HTTPStatusError
from sqlmodel import Session, select, SQLModel

from .client import (
    get_document_versions,
    get_document,
    iterate_documents,
)
from .enums import ActTypeEnum
from .models import Act, engine, ActType, ActVersion
from .schemas import MultiLangDocument, Document, SearchActMetadata

_thread_cache = threading.local()


TROUBLED_CODES = [
    "2574",  # ru/kz разные документы
]


# ACT_TYPES_TO_INGEST = [
#     ActTypeEnum.KONS,
#     ActTypeEnum.KZAK,
#     ActTypeEnum.KOD,
#     ActTypeEnum.ZAK,
#     ActTypeEnum.UZAK,
#     ActTypeEnum.UKAZ,
#     ActTypeEnum.UKON,
#     ActTypeEnum.NPOS,
#     ActTypeEnum.POST,
#     ActTypeEnum.PRIK,
#     ActTypeEnum.RASP,
#     ActTypeEnum.RESH,
# ]


def get_act_types(session) -> dict[str, ActType]:
    if not hasattr(_thread_cache, "act_types"):
        _thread_cache.act_types = {
            at.code: at for at in session.exec(select(ActType)).all()
        }
    return _thread_cache.act_types


def init_db(recreate=False):
    if recreate:
        SQLModel.metadata.drop_all(engine)

    SQLModel.metadata.create_all(engine, checkfirst=True)

    # create act types if not created yet
    with Session(engine) as session:
        for at_enum in ActTypeEnum:
            at = session.exec(
                select(ActType).where(ActType.code == at_enum.value)
            ).first()
            if not at:
                at = ActType(code=at_enum.value)
                session.add(at)
        session.commit()


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
        pages_count=doc.pages_count,
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
        types=[get_act_types(s)[_type] for _type in ml_act.metadata.act_types],
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
            for additional_page in range(2, v_doc.pages_count + 1):
                # the document can have multiple pages, we will extend the content with them
                page_doc = get_document(
                    doc.id, doc.language, v.version_date, page=additional_page
                )
                v_doc.content.extend(page_doc.content)

            v_docs.append(v_doc)

        for v_doc in v_docs:
            act.versions.append(construct_act_version(v_doc))
            s.flush()  # make flush for every version to avoid sending a huge data packet on commit

    return act


def process_doc(page: int, doc_meta: SearchActMetadata):
    if doc_meta.id in TROUBLED_CODES:
        print(f"Skipping {doc_meta.id}")
        return

    with Session(engine) as session:
        act = session.exec(select(Act).where(Act.code == doc_meta.id)).first()
        if act:
            # print(
            #     "page",
            #     page,
            #     "act",
            #     doc_meta.id,
            #     "already ingested",
            # )
            return

        t1 = time.time()
        act = construct_act(doc_meta.id, session)
        if act:  # a constructed and flushed act
            session.commit()
            vc = len(act.versions)
            print(
                threading.current_thread().name,
                "page",
                page,
                "act",
                doc_meta.id,
                f"({vc} ver)",
                f"[{time.time() - t1:.02f}s]",
            )


def ingest_all(recreate: bool, start_page: int = 1, max_workers: int = 2):
    init_db(recreate=recreate)
    docs_iterable = iterate_documents(start_page, per_page=100)

    futures = set()
    stop_consuming = False
    interrupted = False

    with ThreadPoolExecutor(
        max_workers=max_workers, thread_name_prefix="thread"
    ) as executor:

        def submit_next():
            page, doc_meta = next(docs_iterable)
            return executor.submit(process_doc, page, doc_meta)

        try:
            # Prime pool
            for _ in range(max_workers):
                futures.add(submit_next())

            # Rolling saturation
            while futures:
                done, futures = wait(futures, return_when=FIRST_COMPLETED)

                for future in done:
                    try:
                        future.result()  # surface worker errors
                    except Exception as e:
                        print(f"Worker failed: {e}")
                        stop_consuming = True

                    # Only refill if no failure occurred
                    if not stop_consuming:
                        futures.add(submit_next())

                # If failure happened, stop refilling entirely
                if stop_consuming:
                    break

        except KeyboardInterrupt:
            print("\nCtrl+C received. Stopping submission...")
            interrupted = True
        except StopIteration:
            print("No more documents to ingest")
        except Exception as e:
            print("Error running ingestion loop:", e)

        if futures:
            print("Waiting for running tasks to finish...")
            wait(futures)

        print("All running tasks are finished")
        if interrupted:
            print("Exited due to user interrupt")

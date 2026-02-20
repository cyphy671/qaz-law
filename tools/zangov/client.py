"""Main API client for Zan.gov.kz legislative documents API."""

import logging
import time
from datetime import date
from pathlib import Path
from time import sleep
from typing import Iterable, Literal

import httpx
from fake_useragent import UserAgent
from httpx_retries import RetryTransport

from .enums import ActTypeEnum
from .md import document_to_md
from .schemas import Document, SearchActMetadata, SearchPage, VersionInfo

logger = logging.getLogger(__name__)


# Default values
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0

# Base URL
BASE_URL = "https://zan.gov.kz/api"

# HTTP Headers
ua = UserAgent()
DEFAULT_HEADERS = {
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://zan.gov.kz/client/",
    "User-Agent": ua.random,
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}


httpx_client = httpx.Client(
    base_url=BASE_URL,
    headers=DEFAULT_HEADERS.copy(),
    transport=RetryTransport(transport=httpx.HTTPTransport(verify=False)),
    timeout=60,  # huge docs take a long time to download
)


def list_documents(
    page: int = 1, per_page: int = 20, act_types: list[ActTypeEnum] | None = None
) -> SearchPage:
    url = f"/documents/search"
    json_payload = {
        "page": page,
        "limit": per_page,
        "sortBy": {"desc": False, "field": "stateAgencyApprovalDate"},
    }
    if act_types:
        json_payload["actTypes"] = [v.value for v in act_types]

    response = httpx_client.post(url, json=json_payload)
    response.raise_for_status()
    return SearchPage.model_validate(response.json(), extra="forbid")


def iterate_documents(
    start_page: int = 1, **kwargs
) -> Iterable[tuple[int, SearchActMetadata]]:
    page = end_page = start_page
    while page <= end_page:
        search_page = list_documents(page, **kwargs)
        end_page = search_page.page_count  # update end page
        print("page", page, "of", end_page)
        for doc in search_page.documents:
            yield page, doc
        page += 1
        sleep(0.1)


def get_document(
    document_id: str,
    language: Literal["rus", "kaz"] | str,
    version: date | None = None,
    html: bool = False,
    page: int = 1,
) -> Document:
    """Get a document by ID and language."""
    url = f"/documents/{document_id}/{language}"
    if version:
        url += f"/{version.strftime('%d.%m.%Y')}"

    params = {
        "withHtml": "true" if html else "false",
        "page": page,
        "r": int(time.time() * 1000),
    }

    response = httpx_client.get(url, params=params)
    response.raise_for_status()
    return Document.model_validate(response.json(), extra="forbid")


def get_document_versions(document_id: str, language: str):
    url = f"/documents/{document_id}/{language}/versions"
    response = httpx_client.get(url)
    response.raise_for_status()
    return [
        VersionInfo.model_validate(item, extra="forbid") for item in response.json()
    ]


def dump(d: Document) -> Path:
    if isinstance(d.content, str):
        ext = "html"
    else:
        ext = "md"

    filename = f"{d.version_date.strftime('%Y%m%d')}-{d.id}-{d.language}.{ext}"

    path = Path("code") / filename
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(d.content, str):
            f.write(d.content)
        else:
            f.write(document_to_md(d))
    return path

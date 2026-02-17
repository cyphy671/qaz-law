"""Main API client for Zan.gov.kz legislative documents API."""

import logging
import time
from datetime import date
from time import sleep
from typing import Literal, Iterable

import httpx
from httpx_retries import RetryTransport

from .enums import BASE_URL, DEFAULT_HEADERS, ActTypeEnum
from .schemas import Document, VersionInfo, SearchPage, SearchActMetadata

logger = logging.getLogger(__name__)


httpx_client = httpx.Client(
    base_url=BASE_URL,
    headers=DEFAULT_HEADERS.copy(),
    transport=RetryTransport(transport=httpx.HTTPTransport(verify=False)),
    timeout=30,
)

def list_documents(page: int = 1, act_types: list[ActTypeEnum] = None) -> SearchPage:
    url = f"/documents/search"
    json_payload = {
        "page": page,
        "limit": 20,
        "sortBy": {
            "desc": False,
            "field": "stateAgencyApprovalDate"
        },
    }
    if act_types:
        json_payload["actTypes"] = [v.value for v in act_types]

    response = httpx_client.post(url, json=json_payload)
    response.raise_for_status()
    return SearchPage.model_validate(response.json(), extra="forbid")


def iterate_documents(start_page: int = 1, **kwargs) -> Iterable[SearchActMetadata]:
    page = end_page = start_page
    while page <= end_page:
        search_page = list_documents(page, **kwargs)
        end_page = search_page.page_count  # update end page
        print(f"page {page} of {end_page}")
        for doc in search_page.documents:
            yield doc
        sleep(0.5)
        page += 1


def get_document(document_id: str, language: Literal["rus", "kaz"] | str, version: date = None, html: bool = False) -> Document:
    """Get a document by ID and language."""
    url = f"/documents/{document_id}/{language}"
    if version:
        url += f"/{version.strftime('%d.%m.%Y')}"

    params = {
        "withHtml": "true" if html else "false",
        "page": 1,
        "r": int(time.time() * 1000),
    }

    response = httpx_client.get(url, params=params)
    response.raise_for_status()
    return Document.model_validate(response.json(), extra="forbid")


def get_document_versions(document_id: str, language: str):
    url = f"/documents/{document_id}/{language}/versions"
    response = httpx_client.get(url)
    response.raise_for_status()
    return [VersionInfo.model_validate(item, extra="forbid") for item in response.json()]

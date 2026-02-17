"""Pydantic models for Zan.gov.kz API responses."""

from datetime import date
from typing import Any, Self, Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator, BeforeValidator

from .enums import ContentType
from .enums import ActTypeEnum, ActStatus


def parse_date(v: Any) -> Any:
    if isinstance(v, int):
        # single year
        return date.strptime(str(v), "%Y")
    if isinstance(v, str):
        # standard format
        return date.strptime(v, "%Y-%m-%d")
    return v

FlexDate = Annotated[date, BeforeValidator(parse_date)]


class BilingualText(BaseModel):
    """Bilingual text in Kazakh and Russian."""

    model_config = ConfigDict(extra="allow")

    kaz: str = Field(default="", description="Text in Kazakh")
    rus: str = Field(default="", description="Text in Russian")


class KeyValueProperty(BaseModel):
    """Key-value property pair."""
    key: str = Field(..., description="Property key")
    value: str | None = Field(default=None, description="Property value")


class SearchActMetadata(BaseModel):
    """Act metadata in a search context."""
    id: str = Field(..., description="Document ID", examples=["221968"])
    code: str = Field(..., description="Document code", examples=["221968"])
    act_types: list[ActTypeEnum] = Field(
        default_factory=list, alias="actTypes", description="Act type codes"
    )
    approval_place: str = Field(
        default="", alias="approvalPlace", description="Place of approval", examples=["100051000000"]
    )
    initial_publication_date: FlexDate | None = Field(
        None, alias="initialPublicationDate", description="Initial publication date"
    )  # missing in earlier documents
    portal_publication_date: date | None = Field(
        None, alias="portalPublicationDate", description="Portal publication date"
    )  # missing in earlier documents
    requisites: BilingualText = Field(..., description="Document requisites")
    status: ActStatus = Field(..., description="Document status")
    state_agency_approval_date: date = Field(
        ..., alias="stateAgencyApprovalDate", description="Approval date"
    )
    summary: BilingualText = Field(..., description="Act summary")
    action_date: date | None = Field(None, alias="actionDate", description="Action date")
    judiciary_doc_number: str | None = Field(None, alias="judiciaryDocNumber", description="Judiciary document number")

    @model_validator(mode='after')
    def verify_data(self) -> Self:
        assert self.id == self.code, 'act ID diverge'
        return self


class SearchPage(BaseModel):
    """A page of a search query."""
    page: int = Field(..., description="Page number")
    page_count: int = Field(..., alias="pageCount", description="Total number of pages")
    documents_found: int = Field(..., alias="documentsFound", description="Total number of documents found")
    documents: list[SearchActMetadata] = Field(..., alias="list", description="List of documents")


class ActMetadata(BaseModel):
    """Metadata for a legal document."""
    title: BilingualText = Field(..., description="Document title")
    requisites: BilingualText = Field(..., description="Document requisites")
    state_agency_doc_number: str = Field(
        default="",
        alias="stateAgencyDocNumber",
        description="State agency document number",
    )
    judicial_authority: str = Field(
        default="", alias="judicialAuthority", description="Judicial authority"
    )
    judiciary_doc_number: str = Field(
        default="", alias="judiciaryDocNumber", description="Judiciary document number"
    )
    developing_state_agency: str = Field(
        default="", alias="developingStateAgency", description="Developing state agency"
    )
    approving_state_agencies: list[str] = Field(
        default_factory=list,
        alias="approvingStateAgencies",
        description="List of approving state agencies",
    )
    status: str = Field(default="", description="Document status")
    classified: str = Field(default="", description="Classification status")
    registry_number: str = Field(
        default="", alias="registryNumber", description="Registry number"
    )
    publication: list[Any] = Field(
        default_factory=list, description="Publication information"
    )
    legal_validity: str = Field(
        default="", alias="legalValidity", description="Legal validity code"
    )
    region: list[str] = Field(default_factory=list, description="Applicable regions")
    legislation_areas: list[str] = Field(
        default_factory=list,
        alias="legislationAreas",
        description="Legislation area codes",
    )
    act_types: list[ActTypeEnum] = Field(
        default_factory=list, alias="actTypes", description="Act type codes"
    )
    approval_place: str = Field(
        default="", alias="approvalPlace", description="Place of approval", examples=["100051000000"]
    )
    state_agency_approval_date: date = Field(
        ..., alias="stateAgencyApprovalDate", description="Approval date"
    )
    action_date: date | None = Field(None, alias="actionDate", description="Action date")
    judiciary_approval_date: date | None = Field(None, alias="judiciaryApprovalDate", description="Judiciary approval date")
    effective_date: date | None = Field(None, alias="effectiveDate", description="Effective date")

    @model_validator(mode='after')
    def verify_data(self) -> Self:
        if self.state_agency_doc_number in ("б/н", "н/ж"):
            self.state_agency_doc_number = ""
        return self


class ChangeCause(BaseModel):
    """Information about the cause of document changes."""
    code: str = Field(..., description="Code of the causing document")
    document: str = Field(..., description="Document ID that caused the change")
    title: BilingualText = Field(..., description="Title of the causing document")
    requisites: BilingualText = Field(..., description="Requisites of the causing document")

    @model_validator(mode='after')
    def verify_data(self) -> Self:
        # they diverge sometimes, use code as the source of truth
        # assert self.code == self.document, (f'document/code diverges: {self.document}/{self.code}')
        return self




class Signature(BaseModel):
    """Digital signature information."""

    model_config = ConfigDict(extra="allow")

    container: str = Field(..., description="Signature container (base64 encoded)")
    user_comment: str = Field(
        default="", alias="userComment", description="User comment"
    )
    properties: list[KeyValueProperty] = Field(
        default_factory=list, description="Signature properties"
    )


class ContentElement(BaseModel):
    """A single element in the document content structure."""

    id: str | None = Field(None, description="Element ID")
    type: ContentType = Field(
        ..., description="Element type (doc, title, section, article, etc.)"
    )
    level: int = Field(..., description="Hierarchical level")
    text: str | None = Field(default=None, description="Text content of the element")
    index: str | None = Field(default=None, description="Index/number of the element")
    properties: list[KeyValueProperty] = Field(
        default_factory=list, description="Element properties"
    )
    change_id: str | None = Field(None, alias="changeId", description="Change ID of the element")


class DocumentVersion(BaseModel):
    """Version information for a document."""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Version ID")
    language: str = Field(..., description="Language code (rus/kaz)")
    version_date: date = Field(
        ..., alias="versionDate", description="Version effective date"
    )
    metadata: ActMetadata = Field(..., description="Document metadata")
    references: list[Any] = Field(
        default_factory=list, description="References to other documents"
    )
    changes: list[str] | None = Field(
        default=None, description="List of changes in this version"
    )
    cause: ChangeCause | None = Field(
        default=None, description="Cause of this version (if amended)"
    )
    signature: Signature | None = Field(
        default=None, description="Digital signature information"
    )
    imported: bool | None = Field(None, description="Whether version was imported")


class Document(BaseModel):
    """Complete document with content."""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Document ID")
    code: str = Field(..., description="Document code")
    ngr: str = Field(..., description="NGR identifier")
    version: DocumentVersion = Field(..., description="Current version information")
    language: str = Field(..., description="Document language")
    metadata: ActMetadata = Field(..., description="Document metadata")
    actual_version: bool = Field(
        ..., alias="actualVersion", description="Whether this is the actual version"
    )
    versions_count: int = Field(
        ..., alias="versionsCount", description="Total number of versions"
    )
    version_date: date = Field(
        ..., alias="versionDate", description="Version date"
    )
    has_signature: bool = Field(
        ..., alias="hasSignature", description="Whether document has digital signature"
    )
    imported: bool = Field(..., description="Whether document was imported")
    # content: list[ContentElement] | str = Field(
    #     default=None, description="Document content (either as element list or as HTML string)"
    # )
    content: list[dict] | str = Field(
        default=None, description="Document content (either as element list or as HTML string)"
    )
    initial_publication_date: FlexDate | None = Field(
        None, alias="initialPublicationDate", description="Initial publication date"
    )
    pages_count: int = Field(..., alias="pagesCount", description="Total number of pages")
    index: list[dict] | None = Field(default=None, description="Document index")
    temporary_revoked: bool | None = Field(
        None, alias="temporaryRevoked", description="Whether document was revoked temporarily"
    )

    @model_validator(mode='after')
    def verify_data(self) -> Self:
        if not self.metadata.registry_number:
            self.metadata.registry_number = self.code
        assert self.id == self.code == self.metadata.registry_number, f'Document ID diverges: {self.id}/{self.code}/{self.metadata.registry_number}'
        return self


class VersionInfo(BaseModel):
    """Simplified version information for version listings."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(..., description="Version ID")
    language: str = Field(..., description="Language code (rus/kaz)")
    version_date: date = Field(
        ..., alias="versionDate", description="Version effective date"
    )
    metadata: ActMetadata = Field(..., description="Document metadata")
    cause: ChangeCause | None = Field(
        default=None, description="Cause of this version (if amended)"
    )
    references: list[Any] = Field(
        default_factory=list, description="References to other documents"
    )


class MultiLangAct(BaseModel):
    """A legal document with multiple versions in multiple languages."""
    rus: Document | None = Field(..., description="Document in Russian")
    kaz: Document | None = Field(..., description="Document in Kazakh")

    @property
    def code(self):
        return self.rus.code if self.rus else self.kaz.code

    @property
    def metadata(self):
        return self.rus.metadata if self.rus else self.kaz.metadata

    @property
    def ngr(self):
        return self.rus.ngr if self.rus else self.kaz.ngr

    @property
    def initial_publication_date(self):
        return self.rus.initial_publication_date if self.rus else self.kaz.initial_publication_date

    @model_validator(mode='after')
    def verify_data(self) -> Self:
        if not self.rus and not self.kaz:
            raise ValueError('no documents passed')

        if not self.kaz or not self.rus:
            return self  # only one version, skip comparison between documents

        # comparison between documents
        r, k = self.rus, self.kaz
        assert r.id == k.id, 'act ID diverge'
        assert r.ngr == k.ngr, 'NGR diverge'
        assert r.initial_publication_date == k.initial_publication_date, 'initial publication date diverge'

        if r.metadata.act_types != k.metadata.act_types:
            # combine act types from both documents
            print(f'act types diverge: {r.metadata.act_types} / {k.metadata.act_types}')
            all_types = sorted(set(r.metadata.act_types + k.metadata.act_types))
            r.metadata.act_types = all_types.copy()
            k.metadata.act_types = all_types.copy()

        rm, km = r.metadata, k.metadata
        for field in (
            # "status", # they can diverge, ignore and take a rus version
            # "state_agency_doc_number",
            # "approval_place",
            # "classified",
            # "developing_state_agency",
            # "judicial_authority",
            # "legal_validity",
            "registry_number",
            "judiciary_doc_number",
            # "state_agency_approval_date", # they can diverge, ignore and take a rus version
            # "judiciary_approval_date", # they can diverge, ignore and take a rus version
            "action_date",
            "effective_date",
        ):
            ru, kz = getattr(rm, field), getattr(km, field)
            if ru and kz:
                assert ru == kz, f'metadata.{field} diverge: {ru} / {kz}'
            elif kz and not ru:
                setattr(rm, field, kz)
        return self

from datetime import date

from sqlmodel import SQLModel, Field, create_engine, Relationship, UniqueConstraint, Column
from sqlalchemy.dialects.postgresql import TEXT

from .enums import Language, ActTypeEnum, ActStatus


class ActTypeLink(SQLModel, table=True):
    __tablename__ = "act_type_link"
    act_id: int | None = Field(default=None, foreign_key="act.id", primary_key=True)
    type_id: int | None = Field(default=None, foreign_key="act_type.id", primary_key=True)


class ActType(SQLModel, table=True):
    __tablename__ = "act_type"
    id: int | None = Field(default=None, primary_key=True)
    code: ActTypeEnum = Field(..., unique=True, description="Act type code")
    acts: list["Act"] = Relationship(back_populates="types", link_model=ActTypeLink)


class Act(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    code: str = Field(unique=True)  # same-same id/code/metadata.registry_number
    # document_id: str
    # registry_number: str

    ju_doc_number: str

    # 356-V in "Закон Республики Казахстан от 12 октября 2015 года № 356-V ЗРК"
    # often differ by language (like 23 and 23-I)
    sa_doc_number_ru: str  # can be the same as code, but not everytime
    sa_doc_number_kz: str  # can be the same as code, but not everytime

    ngr: str
    status: ActStatus
    # approval_place: str # '100051000000'
    # classified: str
    # developing_state_agency: str
    # judicial_authority: str
    # legal_validity: str

    # 2015-10-12 in "Закон Республики Казахстан от 12 октября 2015 года № 356-V ЗРК"
    sa_approval_date: date
    # other dates
    ju_approval_date: date | None = Field(None)
    action_date: date | None = Field(None)
    effective_date: date | None = Field(None)
    initial_pub_date: date | None = Field(None)

    # from doc metadata
    title: str
    requisite: str

    # moved to act version
    # imported: bool

    # ignored
    # has_signature: bool

    types: list["ActType"] = Relationship(back_populates="acts", link_model=ActTypeLink)
    versions: list["ActVersion"] = Relationship(back_populates="act", sa_relationship_kwargs={"foreign_keys": "ActVersion.act_id"})
    issued_act_versions: list["ActVersion"] = Relationship(back_populates="cause_act", sa_relationship_kwargs={"foreign_keys": "ActVersion.cause_act_id"})


class ActVersion(SQLModel, table=True):
    __tablename__ = "act_version"
    id: int | None = Field(default=None, primary_key=True)

    act_id: int | None = Field(default=None, foreign_key="act.id")
    act: Act = Relationship(sa_relationship_kwargs={"foreign_keys": "ActVersion.act_id"}, back_populates="versions")

    cause_act_id: int | None = Field(default=None, foreign_key="act.id")
    cause_act: Act | None = Relationship(sa_relationship_kwargs={"foreign_keys": "ActVersion.cause_act_id"}, back_populates="issued_act_versions")

    is_actual: bool  # actual_version

    date: date
    contents: list["ActContent"] = Relationship(back_populates="act_version")


class ActContent(SQLModel, table=True):
    __tablename__ = "act_content"
    __table_args__ = (UniqueConstraint("act_version_id", "language", name="act_content_unique_lang"),)

    id: int | None = Field(default=None, primary_key=True)
    act_version_id: int | None = Field(default=None, foreign_key="act_version.id")
    act_version: ActVersion = Relationship(back_populates="contents")
    language: Language  # main discriminator for the content

    version_id: str  # can be different for the same version but different language
    # markdown: str
    content: str = Field(sa_type=TEXT)


engine = create_engine('postgresql+psycopg://postgres:postgres@localhost:5436/postgres', echo=False)

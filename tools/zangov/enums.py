"""Enums and constants for the Zan.gov.kz API client."""

from enum import Enum


class Language(str, Enum):
    """Supported language codes for document retrieval."""

    RUS = "rus"
    KAZ = "kaz"


class ContentType(str, Enum):
    """Content element types found in documents."""

    DOC = "doc"
    TITLE = "title"
    SECTION = "section"
    ARTICLE = "article"
    HEADING = "heading"
    NOTE = "note"
    POINT = "point"
    SUBPOINT = "subpoint"
    TEXT = "text"
    SIDE_NOTE = "sideNote"
    SIDE_NOTE_GROUP = "sideNoteGroup"
    PRE = "pre"
    PREAMBLE = "preamble"
    SIGNATURE = "signature"
    WORK_POSITION = "workPosition"
    PERSON_NAME = "personName"
    TABLE_CELL = "tableCell"
    CHAPTER = "chapter"
    SUBSECTION = "subsection"
    TALE = "table"
    TABLE_ROW = "tableRow"
    ATTACH = "attach"
    SUBHEADING = "subheading"
    RCPI_NOTICE = "rcpi_notice"
    EXCLUDED = "excluded"
    TOC = "toc"
    PART = "part"
    TABLE_HEADER_ROW = "tableHeaderRow"
    PARAGRAPH = "paragraph"
    SUBATTACH = "subattach"
    IMAGE = "image"
    BUFFER = "buffer"
    DESCRIPTION = "description"


class ActTypeEnum(str, Enum):
    """Types of acts found in documents."""

    DOP = "ДОП"
    ZAK = "ЗАК"
    IZM = "ИЗМ"
    KZAK = "КЗАК"
    KONS = "КОНС"  # Конституция
    POR = "ПОР"
    POST = "ПОСТ"  # Постановление
    PRAV = "ПРАВ"
    PRIK = "ПРИК"
    RESH = "РЕШ"
    SOGL = "СОГЛ"
    UKAZ = "УКАЗ"
    NPOS = "НПОС"
    KOD = "КОД"
    MRP = "МРП"
    POL = "ПОЛ"
    PRCH = "ПРЧ"
    INST = "ИНСТ"
    DOG = "ДОГ"
    RAZ = "РАЗ"
    MET = "МЕТ"
    UST = "УСТ"
    UZAK = "УЗАК"
    UKZN = "УКЗН"
    UKON = "УКОН"
    NORM = "НОРМ"
    REGL = "РЕГЛ"
    PROT = "ПРОТ"
    RASP = "РАСП"
    KONV = "КОНВ"
    TREB = "ТРЕБ"
    PISM = "ПИСМ"
    STND = "СТНД"
    PLAN = "ПЛАН"
    OBRA = "ОБРА"
    PROG = "ПРОГ"
    MEMR = "МЕМР"
    KLAS = "КЛАС"
    NOM = "НОМ"
    SHEM = "СХЕМ"
    PROE = "ПРОЕ"
    OPIS = "ОПИС"
    DEKL = "ДЕКЛ"
    PRES = "ПРЕС"
    KONTS = "КОНЦ"
    USL = "УСЛ"
    KRIT = "КРИТ"
    STRA = "СТРА"
    KONT = "КОНТ"
    SUPR = "СУПР"
    OPOL = "ОПОЛ"
    POPR = "ПОПР"
    ZAYAV = "ЗАЯВ"
    HART = "ХАРТ"


class ActStatus(str, Enum):
    EXE = "exe"
    NEW = "new"
    YTS = "yts"  # lost its power
    TEMPORARY_REVOKED = "temporaryRevoked"
    UPD = "upd"
    BAK = "bak"
    VEXP = "vexp"
    STOP = "stop"


# Default values
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0

# Base URL
BASE_URL = "https://zan.gov.kz/api"

# HTTP Headers
DEFAULT_HEADERS = {
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://zan.gov.kz/client/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

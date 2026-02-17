import re
from pathlib import Path

from .schemas import Document, ContentElement
from .enums import ContentType
from markdownify import markdownify
# from htbuilder import div, h1, h2, p, article, ul, li
#
# CONTENT_TYPE_TO_TAG = {
#     ContentType.TITLE: "h1",
#     ContentType.HEADING: "h2",
#     ContentType.TEXT: "p",
#     ContentType.ARTICLE: "section",
#     ContentType.POINT: "ol",
# }
#
# def content_to_html(content: list[ContentElement]) -> str:
#     root = div(id="container")
#     level = 1
#     for e in content[1:]:
#         if e.type == ContentType.TITLE:
#             root.h1(e.text)


def element_to_md(cel: ContentElement) -> list[str]:
    lines = []
    t = cel.text

    if not t:
        return lines

    # element text is not empty
    t = t.replace("\n", " ")  # clear line breaks
    t = re.sub(r"\s+", " ", t)  # clear extra whitespace
    t = t.strip()  # clear leading/trailing whitespace

    # level 1: DOC, content root
    # level 2: HEADING
    # level 3: SUBHEADING

    if cel.type == ContentType.TITLE:
        lines = ["", f"# {t}", ""]
    elif cel.type == ContentType.HEADING:
        if cel.level == 2:
            lines = ["", f"# {t}", ""]  # let's try same as heading
        elif cel.level == 3:
            lines = ["", f"## {t}", ""]
        elif cel.level >= 4:
            lines = ["", f"### {t}", ""]
        else:
            raise ValueError(f"Unhandled heading level: {cel.level}")
    elif cel.type == ContentType.TEXT:
        lines = [t, ""]
    elif cel.type == ContentType.NOTE:
        lines = [f"**{t}**", ""]
    else:
        lines = [f"**{cel.type.name}:** {t}", ""]
        # raise ValueError(f"Unhandled content type: {cel.type}")
        # highlight other text with strikethrough
        # lines = [f"~~{t}~~", ""]

    return lines


def document_to_md(doc: Document) -> str:
    lines = []
    for el in doc.content:
        lines.extend(element_to_md(el))
    return "\n".join(lines)


def doc_to_file(doc: Document, folder: str | Path) -> None:
    path = Path(folder) / f"{doc.code}_{doc.language}_{doc.version_date.strftime("%Y%m%d")}.md"
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(doc.content, str):
            content = markdownify(doc.content)
        else:
            content = document_to_md(doc)
        f.write(content)

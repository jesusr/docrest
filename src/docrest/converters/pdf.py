"""pdf source converters."""
from __future__ import annotations

from pathlib import Path

from docrest.converters.base import ConversionError
from docrest.converters.registry import register


def _extract_text(source: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ConversionError("pypdf required for pdf reading") from exc
    reader = PdfReader(str(source))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages).strip()


@register("pdf", "txt")
def pdf_to_txt(source: Path, target: Path) -> Path:
    target.write_text(_extract_text(source) + "\n", encoding="utf-8")
    return target


@register("pdf", "md")
def pdf_to_md(source: Path, target: Path) -> Path:
    text = _extract_text(source)
    target.write_text(text + "\n", encoding="utf-8")
    return target

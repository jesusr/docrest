"""txt source converters (md/docx targets covered in their own modules)."""
from __future__ import annotations

from pathlib import Path

from docrest.converters.base import ConversionError
from docrest.converters.registry import register


@register("txt", "pdf")
def txt_to_pdf(source: Path, target: Path) -> Path:
    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise ConversionError("weasyprint required for txt->pdf") from exc
    text = source.read_text(encoding="utf-8")
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    html = f"<html><body><pre style='font-family: monospace; white-space: pre-wrap;'>{escaped}</pre></body></html>"
    HTML(string=html).write_pdf(target)
    return target

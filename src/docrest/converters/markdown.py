"""Markdown source/target converters."""
from __future__ import annotations

from pathlib import Path

from docrest.converters.base import ConversionError
from docrest.converters.registry import register


@register("md", "txt")
def md_to_txt(source: Path, target: Path) -> Path:
    from markdown_it import MarkdownIt

    md = MarkdownIt("commonmark")
    text = source.read_text(encoding="utf-8")
    tokens = md.parse(text)
    out: list[str] = []
    for tok in tokens:
        if tok.type == "inline" and tok.content:
            out.append(tok.content)
        elif tok.type in {"heading_open", "paragraph_open"}:
            continue
        elif tok.type in {"heading_close", "paragraph_close"}:
            out.append("")
    target.write_text("\n".join(out).strip() + "\n", encoding="utf-8")
    return target


@register("txt", "md")
def txt_to_md(source: Path, target: Path) -> Path:
    text = source.read_text(encoding="utf-8")
    target.write_text(text, encoding="utf-8")
    return target


@register("md", "html")
def md_to_html(source: Path, target: Path) -> Path:
    from markdown_it import MarkdownIt

    md = MarkdownIt("commonmark", {"html": False, "linkify": True}).enable("table")
    html = md.render(source.read_text(encoding="utf-8"))
    target.write_text(html, encoding="utf-8")
    return target


@register("md", "docx")
def md_to_docx(source: Path, target: Path) -> Path:
    try:
        import pypandoc
    except ImportError as exc:
        raise ConversionError("pypandoc required for md->docx") from exc
    try:
        pypandoc.convert_file(str(source), "docx", outputfile=str(target))
    except OSError as exc:
        raise ConversionError(f"pandoc invocation failed: {exc}") from exc
    return target


@register("md", "pdf")
def md_to_pdf(source: Path, target: Path) -> Path:
    html_path = target.with_suffix(".intermediate.html")
    md_to_html(source, html_path)
    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise ConversionError("weasyprint required for md->pdf") from exc
    try:
        HTML(string=html_path.read_text(encoding="utf-8")).write_pdf(target)
    finally:
        if html_path.exists():
            html_path.unlink()
    return target

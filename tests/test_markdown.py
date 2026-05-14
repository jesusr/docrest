from pathlib import Path

from docrest.converters import convert


def test_md_to_txt_strips_markup(tmp_path: Path) -> None:
    src = tmp_path / "doc.md"
    src.write_text("# Title\n\nHello **world**.\n", encoding="utf-8")
    out = convert(src, tmp_path / "doc.txt")
    text = out.read_text(encoding="utf-8")
    assert "Title" in text
    assert "Hello" in text
    assert "#" not in text


def test_md_to_html_renders(tmp_path: Path) -> None:
    src = tmp_path / "doc.md"
    src.write_text("# Title\n", encoding="utf-8")
    out = convert(src, tmp_path / "doc.html")
    html = out.read_text(encoding="utf-8")
    assert "<h1>Title</h1>" in html

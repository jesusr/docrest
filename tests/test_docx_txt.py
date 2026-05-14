from pathlib import Path

import pytest

pytest.importorskip("docx")

from docrest.converters import convert


def test_txt_to_docx_roundtrip(tmp_path: Path) -> None:
    src = tmp_path / "input.txt"
    src.write_text("line one\nline two\n", encoding="utf-8")
    docx_out = convert(src, tmp_path / "out.docx")
    assert docx_out.exists() and docx_out.stat().st_size > 0

    txt_back = convert(docx_out, tmp_path / "back.txt")
    text = txt_back.read_text(encoding="utf-8")
    assert "line one" in text
    assert "line two" in text

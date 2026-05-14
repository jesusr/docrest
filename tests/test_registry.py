from pathlib import Path

import pytest

from docrest.converters import ConversionError, convert, supported_pairs


def test_supported_pairs_contains_core_routes() -> None:
    pairs = set(supported_pairs())
    expected = {
        ("md", "txt"),
        ("md", "html"),
        ("md", "docx"),
        ("md", "pdf"),
        ("txt", "md"),
        ("txt", "docx"),
        ("txt", "pdf"),
        ("docx", "md"),
        ("docx", "txt"),
        ("docx", "pdf"),
        ("pdf", "txt"),
        ("pdf", "md"),
        ("mmd", "svg"),
        ("puml", "svg"),
    }
    missing = expected - pairs
    assert not missing, f"missing converter routes: {missing}"


def test_convert_rejects_identical_formats(tmp_path: Path) -> None:
    src = tmp_path / "a.md"
    src.write_text("# hi\n", encoding="utf-8")
    with pytest.raises(ConversionError):
        convert(src, tmp_path / "b.md")


def test_convert_rejects_unsupported_pair(tmp_path: Path) -> None:
    src = tmp_path / "a.pdf"
    src.write_bytes(b"%PDF-1.4\n")
    with pytest.raises(ConversionError):
        convert(src, tmp_path / "a.docx")

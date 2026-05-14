from pathlib import Path

from typer.testing import CliRunner

from docrest.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "docrest" in result.stdout


def test_formats_lists_pairs() -> None:
    result = runner.invoke(app, ["formats"])
    assert result.exit_code == 0
    assert "md" in result.stdout
    assert "html" in result.stdout


def test_convert_md_to_txt(tmp_path: Path) -> None:
    src = tmp_path / "doc.md"
    dst = tmp_path / "doc.txt"
    src.write_text("# Hi\n\nbody\n", encoding="utf-8")
    result = runner.invoke(app, ["convert", str(src), str(dst)])
    assert result.exit_code == 0, result.stdout
    assert dst.exists()


def test_convert_reports_error_for_unsupported(tmp_path: Path) -> None:
    src = tmp_path / "a.pdf"
    src.write_bytes(b"%PDF-1.4\n")
    result = runner.invoke(app, ["convert", str(src), str(tmp_path / "a.docx")])
    assert result.exit_code == 1
    assert "error" in result.stdout.lower()

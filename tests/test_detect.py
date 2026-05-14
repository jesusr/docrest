from pathlib import Path

import pytest

from docrest.core.detect import format_from_path


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("README.md", "md"),
        ("notes.markdown", "md"),
        ("plain.txt", "txt"),
        ("report.docx", "docx"),
        ("paper.pdf", "pdf"),
        ("flow.mmd", "mmd"),
        ("graph.puml", "puml"),
        ("page.html", "html"),
    ],
)
def test_format_from_path(filename: str, expected: str) -> None:
    assert format_from_path(Path(filename)) == expected


def test_format_from_path_unknown() -> None:
    with pytest.raises(ValueError):
        format_from_path(Path("data.xyz"))

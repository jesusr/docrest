"""Detect optional external tools and infer formats from file paths."""
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

EXTENSION_FORMAT: dict[str, str] = {
    ".md": "md",
    ".markdown": "md",
    ".txt": "txt",
    ".text": "txt",
    ".docx": "docx",
    ".pdf": "pdf",
    ".html": "html",
    ".htm": "html",
    ".mmd": "mmd",
    ".mermaid": "mmd",
    ".puml": "puml",
    ".plantuml": "puml",
    ".svg": "svg",
    ".png": "png",
}


def format_from_path(path: Path) -> str:
    suffix = path.suffix.lower()
    fmt = EXTENSION_FORMAT.get(suffix)
    if fmt is None:
        raise ValueError(f"unknown format for extension: {suffix or '(none)'}")
    return fmt


@dataclass(frozen=True)
class ToolStatus:
    name: str
    path: str | None
    version: str | None

    @property
    def available(self) -> bool:
        return self.path is not None


def _probe(binary: str, version_args: tuple[str, ...] = ("--version",)) -> ToolStatus:
    path = shutil.which(binary)
    if not path:
        return ToolStatus(name=binary, path=None, version=None)
    try:
        out = subprocess.run(
            [path, *version_args],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        version = (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr) else None
    except (OSError, subprocess.SubprocessError):
        version = None
    return ToolStatus(name=binary, path=path, version=version)


def detect_tools() -> dict[str, ToolStatus]:
    return {
        "pandoc": _probe("pandoc"),
        "mmdc": _probe("mmdc", ("--version",)),
        "plantuml": _probe("plantuml", ("-version",)),
        "weasyprint": _probe("weasyprint"),
    }

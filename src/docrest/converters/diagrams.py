"""Diagram converters: mermaid/plantuml source -> svg/png/pdf."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from docrest.converters.base import ConversionError
from docrest.converters.registry import register


def _require(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise ConversionError(f"required binary not found on PATH: {binary}")
    return path


def _run(cmd: list[str]) -> None:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except OSError as exc:
        raise ConversionError(f"failed to invoke {cmd[0]}: {exc}") from exc
    if result.returncode != 0:
        raise ConversionError(
            f"{cmd[0]} exited with {result.returncode}: {result.stderr.strip() or result.stdout.strip()}"
        )


def _mermaid(source: Path, target: Path) -> Path:
    mmdc = _require("mmdc")
    _run([mmdc, "-i", str(source), "-o", str(target)])
    return target


@register("mmd", "svg")
def mmd_to_svg(source: Path, target: Path) -> Path:
    return _mermaid(source, target)


@register("mmd", "png")
def mmd_to_png(source: Path, target: Path) -> Path:
    return _mermaid(source, target)


@register("mmd", "pdf")
def mmd_to_pdf(source: Path, target: Path) -> Path:
    return _mermaid(source, target)


def _plantuml(source: Path, target: Path, fmt: str) -> Path:
    plantuml = _require("plantuml")
    out_dir = target.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    _run([plantuml, f"-t{fmt}", "-o", str(out_dir.resolve()), str(source)])
    produced = out_dir / f"{source.stem}.{fmt}"
    if produced != target:
        if target.exists():
            target.unlink()
        produced.rename(target)
    return target


@register("puml", "svg")
def puml_to_svg(source: Path, target: Path) -> Path:
    return _plantuml(source, target, "svg")


@register("puml", "png")
def puml_to_png(source: Path, target: Path) -> Path:
    return _plantuml(source, target, "png")


@register("puml", "pdf")
def puml_to_pdf(source: Path, target: Path) -> Path:
    return _plantuml(source, target, "pdf")

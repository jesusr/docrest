"""Converter registry — maps (src, dst) format pairs to converter callables."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, Tuple

from docrest.converters.base import ConversionError

ConvertFn = Callable[[Path, Path], Path]

registry: Dict[Tuple[str, str], ConvertFn] = {}


def register(src: str, dst: str) -> Callable[[ConvertFn], ConvertFn]:
    def decorator(fn: ConvertFn) -> ConvertFn:
        registry[(src.lower(), dst.lower())] = fn
        return fn

    return decorator


def supported_pairs() -> list[tuple[str, str]]:
    return sorted(registry.keys())


def convert(source: Path, target: Path, *, src_fmt: str | None = None, dst_fmt: str | None = None) -> Path:
    from docrest.core.detect import format_from_path

    src = (src_fmt or format_from_path(source)).lower()
    dst = (dst_fmt or format_from_path(target)).lower()

    if src == dst:
        raise ConversionError(f"source and target formats are identical: {src}")

    fn = registry.get((src, dst))
    if fn is None:
        raise ConversionError(f"no converter registered for {src} -> {dst}")

    target.parent.mkdir(parents=True, exist_ok=True)
    return fn(source, target)


def _load_builtins() -> None:
    # Import side effects register converters.
    from docrest.converters import diagrams, docx, markdown, pdf, txt  # noqa: F401


_load_builtins()

"""Converter protocol and shared error type."""
from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable


class ConversionError(RuntimeError):
    """Raised when a conversion cannot be completed."""


@runtime_checkable
class Converter(Protocol):
    src: str
    dst: str

    def convert(self, source: Path, target: Path) -> Path: ...

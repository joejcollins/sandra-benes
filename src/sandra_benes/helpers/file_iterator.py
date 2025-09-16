"""Testable file iterator."""

from pathlib import Path
from typing import Iterator


def file_contents(directory: Path, pattern: str = "*") -> Iterator[str]:
    """Yield full contents of each file in a directory (sorted by name)."""
    for path in sorted(directory.glob(pattern)):
        if path.is_file():
            yield path.read_text(encoding="utf-8")

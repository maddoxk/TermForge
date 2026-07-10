"""Terminal capability detection — pure functions, no Rich imports.

Detects color depth, terminal size, and Unicode support from environment
variables and system calls.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from termforge.core.types import ColorDepth, Size


def detect_color_depth() -> ColorDepth:
    """Detect the terminal's color depth from environment variables.

    Check order:
    1. COLORTERM == 'truecolor' or '24bit' → TRUECOLOR
    2. COLORTERM == '256color' or TERM contains '256color' → COLOR_256
    3. TERM is set and not 'dumb' → COLOR_16
    4. Fallback → MONOCHROME
    """
    colorterm = os.environ.get("COLORTERM", "").lower()
    if colorterm in ("truecolor", "24bit"):
        return ColorDepth.TRUECOLOR

    term = os.environ.get("TERM", "").lower()
    if colorterm == "256color" or "256color" in term:
        return ColorDepth.COLOR_256

    if term and term != "dumb":
        return ColorDepth.COLOR_16

    return ColorDepth.MONOCHROME


def detect_terminal_size() -> Size:
    """Return the current terminal size, falling back to 80×24."""
    try:
        cols, rows = os.get_terminal_size()
        return Size(width=cols, height=rows)
    except (ValueError, OSError):
        return Size(width=80, height=24)


def detect_unicode_support() -> bool:
    """Check whether the terminal likely supports Unicode (UTF-8).

    Inspects LC_ALL, LANG, and LC_CTYPE for 'utf' (case-insensitive).
    """
    for var in ("LC_ALL", "LANG", "LC_CTYPE"):
        val = os.environ.get(var, "")
        if "utf" in val.lower():
            return True
    return False


@dataclass
class TerminalCapabilities:
    """Aggregated terminal capabilities."""

    color_depth: ColorDepth
    size: Size
    unicode_support: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "color_depth": self.color_depth.value,
            "size": self.size.to_dict(),
            "unicode_support": self.unicode_support,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TerminalCapabilities:
        return cls(
            color_depth=ColorDepth(d["color_depth"]),
            size=Size.from_dict(d["size"]),
            unicode_support=d["unicode_support"],
        )


def detect_capabilities() -> TerminalCapabilities:
    """Run all capability detections and return the result."""
    return TerminalCapabilities(
        color_depth=detect_color_depth(),
        size=detect_terminal_size(),
        unicode_support=detect_unicode_support(),
    )

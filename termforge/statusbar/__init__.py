"""TermForge status bar component module."""
from __future__ import annotations

from termforge.statusbar.types import StatusBarSpec, StatusSectionSpec
from termforge.statusbar.render import render_status_bar

__all__ = [
    "StatusBarSpec",
    "StatusSectionSpec",
    "render_status_bar",
]

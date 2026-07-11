"""TermForge search input and filter bar component module."""
from __future__ import annotations

from termforge.search.types import SearchBarSpec
from termforge.search.render import render_search_bar, highlight_matches

__all__ = [
    "SearchBarSpec",
    "render_search_bar",
    "highlight_matches",
]

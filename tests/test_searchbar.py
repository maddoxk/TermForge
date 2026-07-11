"""Tests for Issue #181: SearchBar Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.search.types import SearchBarSpec
from termforge.search.render import render_search_bar, highlight_matches


def test_searchbar_serialization():
    search = SearchBarSpec(
        query="git",
        candidates=["git status", "subversion"],
        placeholder="Type here...",
        match_style="colors.warning",
        input_style="colors.primary",
        width=40,
        height=5
    )

    d = search.to_dict()
    assert d["spec_type"] == "search_bar"
    assert d["query"] == "git"
    assert d["candidates"] == ["git status", "subversion"]
    assert d["placeholder"] == "Type here..."

    restored = SearchBarSpec.from_dict(d)
    assert restored.query == "git"
    assert restored.placeholder == "Type here..."
    assert restored.candidates == ["git status", "subversion"]


def test_searchbar_render_placeholder():
    search = SearchBarSpec(
        query="",
        placeholder="Type query...",
        placeholder_style="colors.secondary"
    )

    theme = ThemeTokens(
        colors={"secondary": ColorValue(100, 100, 100, name="colors.secondary")}
    )

    # Output Line 0: "🔍 Search: Type query..."
    lines = render_search_bar(search, Size(30, 2), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 2
    assert "\033[38;2;100;100;100mType query...\033[0m" in lines[0]


def test_searchbar_render_filtering():
    search = SearchBarSpec(
        query="git",
        candidates=["github", "subversion", "Gitlab", "git commit"]
    )

    # "subversion" doesn't contain "git" case-insensitively, so it should be omitted.
    # Lines:
    # 0: Search input line
    # 1: github
    # 2: Gitlab
    # 3: git commit
    lines = render_search_bar(search, Size(20, 5))
    assert len(lines) == 5
    assert "github" in lines[1]
    assert "Gitlab" in lines[2]
    assert "git commit" in lines[3]
    # Blank filler
    assert lines[4] == "                    "


def test_highlight_matches_case_insensitive():
    theme = ThemeTokens(
        colors={"warning": ColorValue(255, 255, 0, name="colors.warning")}
    )

    res = highlight_matches("Gitlab", "git", "colors.warning", theme, ColorDepth.TRUECOLOR)
    # The output should contain the original case "Git" styled
    assert res == "\033[38;2;255;255;0mGit\033[0mlab"

"""Story: search/search_bar_demo — showcase query search input and filter list.

Demonstrates placeholders, filtering list candidates, case-insensitive substring
matching highlights, and theme styling.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.search.types import SearchBarSpec
from termforge.search.render import render_search_bar


def main() -> None:
    print("=== TermForge SearchBar Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Candidates list
    candidates = [
        "github",
        "gitlab",
        "git commit",
        "subversion",
        "mercurial",
        "digital ocean",
        "Git LFS"
    ]

    # 1. Empty Query (show placeholder)
    search_empty = SearchBarSpec(
        query="",
        candidates=candidates,
        placeholder="Type search terms here...",
        placeholder_style="colors.secondary"
    )
    rendered_empty = render_search_bar(search_empty, Size(40, 6), theme=theme)
    print("--- 1. Search Bar Empty Input (Width = 40, Height = 6) ---")
    for line in rendered_empty:
        print(line)
    print()

    # 2. Filter match (query = "git")
    search_match = SearchBarSpec(
        query="git",
        candidates=candidates,
        match_style="colors.warning",
        input_style="colors.primary"
    )
    rendered_match = render_search_bar(search_match, Size(40, 6), theme=theme)
    print("--- 2. Search Bar Filtered matches for 'git' (Width = 40, Height = 6) ---")
    for line in rendered_match:
        print(line)
    print()

    # 3. Portability check
    d = search_match.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = SearchBarSpec.from_dict(d)
    assert restored.query == "git"
    print("Portability check: OK")


if __name__ == "__main__":
    main()

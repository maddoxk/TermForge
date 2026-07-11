"""Story: navigation/breadcrumbs_demo — showcase path trail navigation.

Demonstrates full path rendering, automatic intermediate collapsing, tail-only fallback,
and theme styling of trail components.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.navigation.types import BreadcrumbsSpec
from termforge.navigation.render import render_breadcrumbs


def main() -> None:
    print("=== TermForge Breadcrumbs Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Path segments
    items = ["Root", "Users", "maddoxk", "TermForge", "termforge", "navigation"]

    # 1. Full fit trail (width = 60)
    nav_full = BreadcrumbsSpec(
        items=items,
        delimiter=" › ",
        item_style="colors.secondary",
        delimiter_style="colors.border",
        active_item_style="colors.primary"
    )
    rendered_full = render_breadcrumbs(nav_full, Size(60, 1), theme=theme)
    print("--- 1. Full Path Fit (Width = 60) ---")
    print(rendered_full[0])
    print()

    # 2. Collapsed intermediates (width = 30)
    # Expected: "Root › ... › navigation"
    rendered_coll = render_breadcrumbs(nav_full, Size(30, 1), theme=theme)
    print("--- 2. Collapsed Intermediate Paths (Width = 30) ---")
    print(rendered_coll[0])
    print()

    # 3. Collapsed tail only (width = 18)
    # Expected: "... › navigation"
    rendered_tail = render_breadcrumbs(nav_full, Size(18, 1), theme=theme)
    print("--- 3. Collapsed Tail Only Path (Width = 18) ---")
    print(rendered_tail[0])
    print()

    # 4. Truncated leaf (width = 8)
    # Expected: "navigat…"
    rendered_trunc = render_breadcrumbs(nav_full, Size(8, 1), theme=theme)
    print("--- 4. Truncated Active Leaf Path (Width = 8) ---")
    print(rendered_trunc[0])
    print()

    # 5. Portability check
    d = nav_full.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = BreadcrumbsSpec.from_dict(d)
    print(f"Restored delimiter: {restored.delimiter}")
    print("Portability check: OK")


if __name__ == "__main__":
    main()

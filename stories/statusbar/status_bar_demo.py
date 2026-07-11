"""Story: statusbar/status_bar_demo — showcase metadata information footer bar.

Demonstrates left, center, right alignments, status segments highlight styling,
custom separators, and viewport size overflow/truncation math.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.statusbar.types import StatusBarSpec, StatusSectionSpec
from termforge.statusbar.render import render_status_bar


def main() -> None:
    print("=== TermForge StatusBar Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Setup status sections
    status = StatusBarSpec(
        left=[
            StatusSectionSpec(text=" NORMAL ", style="colors.success"),
            StatusSectionSpec(text="main.py", style="colors.secondary"),
        ],
        center=[
            StatusSectionSpec(text="Line: 12 Col: 5"),
        ],
        right=[
            StatusSectionSpec(text="UTF-8", style="colors.border"),
            StatusSectionSpec(text=" 95% ", style="colors.primary"),
        ],
        separator=" │ ",
        separator_style="colors.border"
    )

    # 1. Full size status bar (width = 60)
    rendered_full = render_status_bar(status, Size(60, 1), theme=theme)
    print("--- 1. Full Width Fit (Width = 60) ---")
    print(rendered_full[0])
    print()

    # 2. Narrow width (width = 34, center is omitted!)
    # Left (17 chars) + Right (13 chars) = 30 chars. Spaces = 4.
    rendered_narrow = render_status_bar(status, Size(34, 1), theme=theme)
    print("--- 2. Narrow Width, Center Omitted (Width = 34) ---")
    print(rendered_narrow[0])
    print()

    # 3. Extremely narrow (width = 22, right truncated!)
    rendered_trunc = render_status_bar(status, Size(22, 1), theme=theme)
    print("--- 3. Extremely Narrow, Right Truncated (Width = 22) ---")
    print(rendered_trunc[0])
    print()

    # 4. Portability check
    d = status.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = StatusBarSpec.from_dict(d)
    assert len(restored.left) == 2
    print("Portability check: OK")


if __name__ == "__main__":
    main()

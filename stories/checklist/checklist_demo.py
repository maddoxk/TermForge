"""Story: checklist/checklist_demo — showcase checkable list option toggles.

Demonstrates checklist choices rendering, checkbox custom checked/unchecked
indicators (like ☐ vs ☑), active focus highlights, and styling configurations.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.checklist.types import ChecklistSpec, ChecklistItemSpec
from termforge.checklist.render import render_checklist


def main() -> None:
    print("=== TermForge Checklist Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Checklist options
    items = [
        ChecklistItemSpec(label="Install Core Dependencies", checked=True),
        ChecklistItemSpec(label="Download Asset Resource Bundles", checked=False),
        ChecklistItemSpec(label="Compile Binary Releases", checked=True),
        ChecklistItemSpec(label="Run Local Verification Tests", checked=False)
    ]

    # 1. Custom indicators (☑ / ☐) with active selection focused on item 1
    checklist_custom = ChecklistSpec(
        items=items,
        selected_idx=1,
        checked_indicator="☑ ",
        unchecked_indicator="☐ ",
        checked_style="colors.success",
        selected_style="colors.primary",
        unchecked_style="colors.secondary"
    )
    rendered_custom = render_checklist(checklist_custom, Size(40, 5), theme=theme)
    print("--- 1. Custom Checkbox Indicators & Selection focused on Item 1 ---")
    for line in rendered_custom:
        print(line)
    print()

    # 2. Standard indicator brackets ([x] / [ ]) with selection focused on item 2
    checklist_std = ChecklistSpec(
        items=items,
        selected_idx=2,
        checked_indicator="[x] ",
        unchecked_indicator="[ ] ",
        checked_style="colors.success",
        selected_style="colors.warning"
    )
    rendered_std = render_checklist(checklist_std, Size(40, 5), theme=theme)
    print("--- 2. Standard Indicator Brackets & Selection focused on Item 2 ---")
    for line in rendered_std:
        print(line)
    print()

    # 3. Portability check
    d = checklist_custom.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = ChecklistSpec.from_dict(d)
    assert len(restored.items) == 4
    print("Portability check: OK")


if __name__ == "__main__":
    main()

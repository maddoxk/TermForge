"""Story: spinnerbox/spinner_box_demo — showcase numeric spinner box inputs.

Demonstrates number settings controls, decrement/increment carets, description
labels, spacing alignments, and serialization.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.spinnerbox.types import SpinnerBoxSpec
from termforge.spinnerbox.render import render_spinner_box


def main() -> None:
    print("=== TermForge SpinnerBox Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # 1. Standard caret spinner box
    spinner_std = SpinnerBoxSpec(
        label="Background Thread Workers Count",
        value=4,
        min_val=0,
        max_val=16,
        left_caret="◀",
        right_caret="▶",
        caret_style="colors.primary",
        value_style="colors.warning",
        label_style="colors.secondary"
    )
    rendered_std = render_spinner_box(spinner_std, Size(45, 2), theme=theme)
    print("--- 1. Spinner Box with Arrow Carets (Width = 45, Height = 2) ---")
    for line in rendered_std:
        print(line)
    print()

    # 2. Text button spinner box
    spinner_btn = SpinnerBoxSpec(
        label="Diagnostic Logging API Level",
        value=8,
        min_val=0,
        max_val=10,
        left_caret="[ - ]",
        right_caret="[ + ]",
        caret_style="colors.success",
        value_style="colors.warning",
        label_style="colors.secondary"
    )
    rendered_btn = render_spinner_box(spinner_btn, Size(45, 2), theme=theme)
    print("--- 2. Spinner Box with Button Carets (Width = 45, Height = 2) ---")
    for line in rendered_btn:
        print(line)
    print()

    # 3. Portability check
    d = spinner_std.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = SpinnerBoxSpec.from_dict(d)
    assert restored.value == 4
    print("Portability check: OK")


if __name__ == "__main__":
    main()

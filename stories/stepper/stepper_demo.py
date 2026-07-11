"""Story: stepper/stepper_demo — showcase wizard progress steppers.

Demonstrates sequential installation/setup titles, connecting arrow separators
(e.g., ->), active step highlights inside square brackets, and serialization.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.stepper.types import StepperSpec
from termforge.stepper.render import render_stepper


def main() -> None:
    print("=== TermForge Stepper Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Step titles list
    steps = ["Choose Directory", "Select Core Specs", "Install Bundles", "Launch Application"]

    # 1. Custom arrow connector ( -> ) with active step focused on index 1
    stepper_arrow = StepperSpec(
        steps=steps,
        active_idx=1,
        connector=" -> ",
        active_style="colors.primary",
        inactive_style="colors.secondary",
        connector_style="border"
    )
    rendered_arrow = render_stepper(stepper_arrow, Size(80, 2), theme=theme)
    print("--- 1. Arrow Connector & Selection focused on Step 1 (Configure) ---")
    for line in rendered_arrow:
        print(line)
    print()

    # 2. Custom heavy connector ( » ) with active step focused on index 2
    stepper_heavy = StepperSpec(
        steps=steps,
        active_idx=2,
        connector=" » ",
        active_style="colors.success",
        inactive_style="colors.secondary",
        connector_style="border"
    )
    rendered_heavy = render_stepper(stepper_heavy, Size(80, 2), theme=theme)
    print("--- 2. Heavy Connector & Selection focused on Step 2 (Install) ---")
    for line in rendered_heavy:
        print(line)
    print()

    # 3. Portability check
    d = stepper_arrow.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = StepperSpec.from_dict(d)
    assert restored.active_idx == 1
    print("Portability check: OK")


if __name__ == "__main__":
    main()

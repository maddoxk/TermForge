"""Story: toast/toast_demo — showcase temporary pop-up notification alerts.

Demonstrates different corners position stacking, severity coloring, border styles
(rounded, double, single), and serialization.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.toast.types import ToastSpec
from termforge.toast.render import render_toast


def main() -> None:
    print("=== TermForge Toast Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # 1. Top-Right Success Toast (Rounded border)
    toast_success = ToastSpec(
        text="Build compiled in 1.45s",
        toast_type="success",
        position="top-right",
        border_style="rounded"
    )
    rendered_tr = render_toast(toast_success, Size(40, 5), theme=theme)
    print("--- 1. Success Toast (Top-Right, Rounded) ---")
    for line in rendered_tr:
        print(line)
    print()

    # 2. Bottom-Left Error Toast (Double border)
    toast_error = ToastSpec(
        text="Disk write permission denied",
        toast_type="error",
        position="bottom-left",
        border_style="double"
    )
    rendered_bl = render_toast(toast_error, Size(40, 5), theme=theme)
    print("--- 2. Error Toast (Bottom-Left, Double) ---")
    for line in rendered_bl:
        print(line)
    print()

    # 3. Top-Left Warning Toast (Single border)
    toast_warning = ToastSpec(
        text="Workspace latency is high",
        toast_type="warning",
        position="top-left",
        border_style="single"
    )
    rendered_tl = render_toast(toast_warning, Size(40, 5), theme=theme)
    print("--- 3. Warning Toast (Top-Left, Single) ---")
    for line in rendered_tl:
        print(line)
    print()

    # 4. Portability check
    d = toast_success.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = ToastSpec.from_dict(d)
    assert restored.toast_type == "success"
    print("Portability check: OK")


if __name__ == "__main__":
    main()

"""Story: card/card_demo — showcase bordered cards for layout groupings.

Demonstrates headers title/subtitle embeds, multiline body content padding/truncation,
single/double/heavy/rounded border styles, and serialization.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.card.types import CardSpec
from termforge.card.render import render_card


def main() -> None:
    print("=== TermForge Card Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    content = (
        "CPU Load: 45.8%\n"
        "RAM Usage: 8.2 GB / 16.0 GB\n"
        "IO operations: Normal\n"
        "Temperature: 42 C"
    )

    # 1. Single border card with header
    card_single = CardSpec(
        title="Host Statistics",
        subtitle="Node-01",
        content=content,
        border_style="single",
        title_style="colors.primary",
        subtitle_style="colors.secondary",
        content_style="colors.success",
        border_style_token="border"
    )
    rendered_single = render_card(card_single, Size(40, 7), theme=theme)
    print("--- 1. Card with Header & Single Borders (Width = 40, Height = 7) ---")
    for line in rendered_single:
        print(line)
    print()

    # 2. Rounded border card with content only (no title)
    card_rounded = CardSpec(
        content=content,
        border_style="rounded",
        content_style="colors.warning",
        border_style_token="border"
    )
    rendered_rounded = render_card(card_rounded, Size(40, 7), theme=theme)
    print("--- 2. Card with Rounded Borders & No Header (Width = 40, Height = 7) ---")
    for line in rendered_rounded:
        print(line)
    print()

    # 3. Portability check
    d = card_single.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = CardSpec.from_dict(d)
    assert restored.title == "Host Statistics"
    print("Portability check: OK")


if __name__ == "__main__":
    main()

"""Tests for Issue #195: Card Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.card.types import CardSpec
from termforge.card.render import render_card


def test_card_serialization():
    card = CardSpec(
        title="Stats",
        subtitle="Node",
        content="RAM: 8GB",
        border_style="double",
        title_style="colors.primary",
        subtitle_style="colors.secondary",
        content_style="colors.success",
        border_style_token="colors.warning",
        width=30,
        height=6
    )

    d = card.to_dict()
    assert d["spec_type"] == "card"
    assert d["title"] == "Stats"
    assert d["subtitle"] == "Node"
    assert d["content"] == "RAM: 8GB"
    assert d["border_style"] == "double"
    assert d["title_style"] == "colors.primary"

    restored = CardSpec.from_dict(d)
    assert restored.title == "Stats"
    assert restored.subtitle == "Node"
    assert restored.content == "RAM: 8GB"
    assert restored.border_style == "double"


def test_card_render_borders_header():
    card = CardSpec(
        title="Sys",
        subtitle="V1",
        content="CPU: 5%",
        border_style="single"
    )

    # Viewport size: width=15, height=4.
    # Inner width = 13, Inner height = 2.
    # Label text: " Sys (V1) " (length 10).
    # Top line format: s_tl (┌) + s_h * 1 (─) + title + s_h * (13 - 1 - 10) (─ * 2) + s_tr (┐)
    # -> "┌─ Sys (V1) ──┐" (length 15).
    # Body line 0: "│CPU: 5%      │" (length 15).
    # Body line 1: "│             │" (length 15).
    # Bottom line: "└─────────────┘" (length 15).
    lines = render_card(card, Size(15, 4))
    assert len(lines) == 4
    assert lines[0] == "┌─ Sys (V1) ──┐"
    assert lines[1] == "│CPU: 5%      │"
    assert lines[2] == "│             │"
    assert lines[3] == "└─────────────┘"


def test_card_render_ansi_styling():
    card = CardSpec(
        title="Sys",
        title_style="colors.primary",
        content_style="colors.success"
    )

    theme = ThemeTokens(
        colors={
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "success": ColorValue(0, 255, 0, name="colors.success")
        }
    )

    lines = render_card(card, Size(12, 3), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 3
    # Title styled red (255, 0, 0)
    assert "\033[38;2;255;0;0m Sys \033[0m" in lines[0]
    # Body content line styled green (0, 255, 0)
    assert "\033[38;2;0;255;0m          \033[0m" in lines[1]

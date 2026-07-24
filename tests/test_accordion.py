"""Tests for Issue #197: Accordion Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.accordion.types import AccordionSpec, AccordionItemSpec
from termforge.accordion.render import render_accordion


def test_accordion_serialization():
    accordion = AccordionSpec(
        items=[
            AccordionItemSpec(title="Info", details="Help text", is_expanded=True),
            AccordionItemSpec(title="Auth", details="Login settings", is_expanded=False)
        ],
        selected_idx=0,
        collapsed_caret="+ ",
        expanded_caret="- ",
        active_style="colors.success",
        selected_style="colors.warning",
        details_style="colors.secondary",
        width=35,
        height=5
    )

    d = accordion.to_dict()
    assert d["spec_type"] == "accordion"
    assert d["selected_idx"] == 0
    assert d["collapsed_caret"] == "+ "
    assert d["expanded_caret"] == "- "
    assert len(d["items"]) == 2
    assert d["items"][0]["title"] == "Info"
    assert d["items"][0]["is_expanded"] is True

    restored = AccordionSpec.from_dict(d)
    assert restored.selected_idx == 0
    assert restored.collapsed_caret == "+ "
    assert len(restored.items) == 2
    assert restored.items[0].title == "Info"
    assert restored.items[0].is_expanded is True


def test_accordion_render_caret_details():
    accordion = AccordionSpec(
        items=[
            AccordionItemSpec(title="A", details="Help A", is_expanded=True),
            AccordionItemSpec(title="B", details="Help B", is_expanded=False)
        ],
        selected_idx=0,
        collapsed_caret="> ",
        expanded_caret="v "
    )

    # Viewport: width=15, height=5.
    # Lines:
    # 0: "v A            "
    # 1: "    Help A     "
    # 2: "> B            "
    # 3: "               "
    # 4: "               "
    lines = render_accordion(accordion, Size(15, 5))
    assert len(lines) == 5
    assert lines[0] == "v A            "
    assert lines[1] == "    Help A     "
    assert lines[2] == "> B            "
    assert lines[3] == "               "


def test_accordion_render_ansi_styling():
    accordion = AccordionSpec(
        items=[
            AccordionItemSpec(title="A", details="Help", is_expanded=True)
        ],
        selected_idx=0,
        selected_style="colors.warning",
        details_style="colors.secondary"
    )

    theme = ThemeTokens(
        colors={
            "warning": ColorValue(255, 255, 0, name="colors.warning"),
            "secondary": ColorValue(0, 0, 255, name="colors.secondary")
        }
    )

    lines = render_accordion(accordion, Size(15, 2), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 2
    # Selected header styled yellow (255, 255, 0)
    assert "\033[38;2;255;255;0mv \033[0m" in lines[0]
    assert "\033[38;2;255;255;0mA\033[0m" in lines[0]
    # Indented details styled blue (0, 0, 255)
    assert "\033[38;2;0;0;255m    Help\033[0m" in lines[1]

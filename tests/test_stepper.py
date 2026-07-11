"""Tests for Issue #194: Stepper Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.stepper.types import StepperSpec
from termforge.stepper.render import render_stepper


def test_stepper_serialization():
    stepper = StepperSpec(
        steps=["Select", "Configure", "Build"],
        active_idx=1,
        connector=" >> ",
        active_style="colors.success",
        inactive_style="colors.secondary",
        connector_style="colors.primary",
        width=40,
        height=1
    )

    d = stepper.to_dict()
    assert d["spec_type"] == "stepper"
    assert d["active_idx"] == 1
    assert d["connector"] == " >> "
    assert d["steps"] == ["Select", "Configure", "Build"]

    restored = StepperSpec.from_dict(d)
    assert restored.active_idx == 1
    assert restored.connector == " >> "
    assert restored.steps == ["Select", "Configure", "Build"]


def test_stepper_render_connectors():
    stepper = StepperSpec(
        steps=["A", "B", "C"],
        active_idx=1,
        connector=" -> "
    )

    # Output format: "A -> [B] -> C"
    # Lengths: A (1) + " -> " (4) + "[B]" (3) + " -> " (4) + C (1) = 13 characters.
    # Viewport size: width=18, height=2.
    # Output line 0: "A -> [B] -> C     "
    lines = render_stepper(stepper, Size(18, 2))
    assert len(lines) == 2
    assert lines[0] == "A -> [B] -> C     "
    assert lines[1] == "                  "


def test_stepper_render_ansi_styling():
    stepper = StepperSpec(
        steps=["A", "B"],
        active_idx=0,
        connector=" | ",
        active_style="colors.success",
        connector_style="colors.primary",
        inactive_style="colors.secondary"
    )

    theme = ThemeTokens(
        colors={
            "success": ColorValue(0, 255, 0, name="colors.success"),
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "secondary": ColorValue(0, 0, 255, name="colors.secondary")
        }
    )

    lines = render_stepper(stepper, Size(15, 1), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    # Active step styled green (0, 255, 0)
    assert "\033[38;2;0;255;0m[A]\033[0m" in lines[0]
    # Connector styled red (255, 0, 0)
    assert "\033[38;2;255;0;0m | \033[0m" in lines[0]
    # Inactive step styled blue (0, 0, 255)
    assert "\033[38;2;0;0;255mB\033[0m" in lines[0]

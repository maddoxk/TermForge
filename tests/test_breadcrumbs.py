"""Tests for Issue #172: Breadcrumbs Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.navigation.types import BreadcrumbsSpec
from termforge.navigation.render import render_breadcrumbs


def test_breadcrumbs_serialization():
    nav = BreadcrumbsSpec(
        items=["Home", "Settings", "Profile"],
        delimiter=" › ",
        item_style="colors.secondary",
        delimiter_style="colors.border",
        active_item_style="colors.primary",
        width=40,
        height=1
    )

    d = nav.to_dict()
    assert d["spec_type"] == "breadcrumbs"
    assert d["items"] == ["Home", "Settings", "Profile"]
    assert d["delimiter"] == " › "
    assert d["item_style"] == "colors.secondary"
    assert d["active_item_style"] == "colors.primary"

    restored = BreadcrumbsSpec.from_dict(d)
    assert restored.items == ["Home", "Settings", "Profile"]
    assert restored.delimiter == " › "
    assert restored.active_item_style == "colors.primary"


def test_breadcrumbs_render_fits():
    nav = BreadcrumbsSpec(
        items=["Home", "Settings", "Profile"],
        delimiter=" > "
    )

    # Expected: "Home > Settings > Profile" (24 chars)
    lines = render_breadcrumbs(nav, Size(30, 2))
    assert len(lines) == 1
    assert lines[0] == "Home > Settings > Profile"


def test_breadcrumbs_render_collapsed():
    nav = BreadcrumbsSpec(
        items=["Home", "System", "Network", "Advanced", "Profile"],
        delimiter=" > "
    )

    # Raw string: "Home > System > Network > Advanced > Profile" (44 chars)
    # Viewport width: 30 chars
    # Collapsed to: "Home > ... > Profile" (20 chars)
    lines = render_breadcrumbs(nav, Size(30, 2))
    assert len(lines) == 1
    assert lines[0] == "Home > ... > Profile"


def test_breadcrumbs_render_tail_only():
    nav = BreadcrumbsSpec(
        items=["Home", "AdvancedSystemSettingsProfile"],
        delimiter=" > "
    )

    # Raw string: "Home > AdvancedSystemSettingsProfile" (37 chars)
    # Viewport width: 30 chars
    # Collapsed to: "... > AdvancedSystemSettingsProfile" (length 35) -> exceeds 30
    # Collapsed to just active item: "AdvancedSystemSettingsProfile" (length 29) <= 30
    lines = render_breadcrumbs(nav, Size(30, 2))
    assert len(lines) == 1
    assert lines[0] == "AdvancedSystemSettingsProfile"


def test_breadcrumbs_render_truncated_leaf():
    nav = BreadcrumbsSpec(
        items=["AdvancedSystemSettingsProfileLongText"],
        delimiter=" > "
    )

    # Viewport width: 20 chars
    # Active item is too long: "AdvancedSystemSettingsProfileLongText" (37 chars) -> exceeds 20
    # Expected: "AdvancedSystemSett…" (20 chars)
    lines = render_breadcrumbs(nav, Size(20, 2))
    assert len(lines) == 1
    assert len(lines[0]) == 20
    assert lines[0] == "AdvancedSystemSetti…"



def test_breadcrumbs_render_ansi_styling():
    nav = BreadcrumbsSpec(
        items=["Home", "Profile"],
        delimiter=" > ",
        item_style="colors.secondary",
        delimiter_style="colors.border",
        active_item_style="colors.primary"
    )

    theme = ThemeTokens(
        colors={
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "secondary": ColorValue(0, 255, 0, name="colors.secondary"),
            "border": ColorValue(0, 0, 255, name="colors.border")
        }
    )

    lines = render_breadcrumbs(nav, Size(40, 2), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    # Check intermediate item color (green: 0, 255, 0)
    assert "\033[38;2;0;255;0mHome\033[0m" in lines[0]
    # Check delimiter color (blue: 0, 0, 255)
    assert "\033[38;2;0;0;255m > \033[0m" in lines[0]
    # Check active item color (red: 255, 0, 0)
    assert "\033[38;2;255;0;0mProfile\033[0m" in lines[0]

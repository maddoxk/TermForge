"""Tests for termforge divider component."""
from termforge.divider.types import DividerSpec
from termforge.divider.render import render_divider
from termforge.core.types import Size, ColorDepth


def test_divider_spec_to_from_dict():
    spec = DividerSpec(
        label="OPTIONS",
        alignment="center",
        line_char="═",
        label_style="colors.primary",
        line_style="border",
    )
    d = spec.to_dict()
    assert d["spec_type"] == "divider"
    assert d["label"] == "OPTIONS"
    assert d["alignment"] == "center"
    assert d["line_char"] == "═"

    spec2 = DividerSpec.from_dict(d)
    assert spec2.label == "OPTIONS"
    assert spec2.alignment == "center"
    assert spec2.line_char == "═"


def test_divider_render_center():
    spec = DividerSpec(label="OPTIONS", alignment="center", line_char="═")
    lines = render_divider(spec, Size(width=20, height=1), depth=ColorDepth.MONOCHROME)
    assert len(lines) == 1
    assert lines[0] == "═════ OPTIONS ══════"


def test_divider_render_left():
    spec = DividerSpec(label="OPTIONS", alignment="left", line_char="═")
    lines = render_divider(spec, Size(width=20, height=1), depth=ColorDepth.MONOCHROME)
    assert lines[0] == "══ OPTIONS ═════════"


def test_divider_render_no_label():
    spec = DividerSpec(line_char="─")
    lines = render_divider(spec, Size(width=10, height=1), depth=ColorDepth.MONOCHROME)
    assert lines[0] == "──────────"

"""Tests for termforge.core — serialization round-trips, capability detection,
color resolution, layout computation, scheduler ticks, and theme tokens.
"""
from __future__ import annotations

import json
import os
from unittest import mock

import pytest

from termforge.core.types import (
    BoxConstraints,
    ColorDepth,
    ColorValue,
    LayoutResult,
    Position,
    RenderableSpec,
    Size,
    Spacing,
    StyleSpec,
)
from termforge.core.capability import (
    TerminalCapabilities,
    detect_capabilities,
    detect_color_depth,
    detect_terminal_size,
    detect_unicode_support,
)
from termforge.core.color import (
    ANSI_16_COLORS,
    color_distance,
    interpolate_color,
    resolve_color,
)
from termforge.core.theme import (
    CATPPUCCIN_MOCHA,
    DRACULA,
    HIGH_CONTRAST,
    TOKYO_NIGHT,
    ThemeTokens,
    load_theme_from_dict,
    resolve_token,
    theme_to_dict,
)
from termforge.core.layout import (
    BoxModel,
    FlexContainer,
    FlexDirection,
    LayoutNode,
    compute_layout,
)
from termforge.core.scheduler import (
    AnimationSpec,
    SchedulerState,
    create_scheduler,
    is_animation_complete,
    register_animation,
    tick,
    unregister_animation,
)


# ===================================================================
# JSON serialization round-trip tests
# ===================================================================

class TestSerializationRoundTrip:
    """Every dataclass must survive to_dict → JSON → from_dict."""

    def _roundtrip(self, obj, cls):
        d = obj.to_dict()
        json_str = json.dumps(d)
        d2 = json.loads(json_str)
        restored = cls.from_dict(d2)
        assert obj == restored, f"{obj} != {restored}"

    def test_color_value(self):
        self._roundtrip(ColorValue(r=137, g=180, b=250, name="blue"), ColorValue)
        self._roundtrip(ColorValue(r=0, g=0, b=0), ColorValue)

    def test_size(self):
        self._roundtrip(Size(width=80, height=24), Size)

    def test_position(self):
        self._roundtrip(Position(x=10, y=5), Position)

    def test_spacing(self):
        self._roundtrip(Spacing(top=1, right=2, bottom=3, left=4), Spacing)
        self._roundtrip(Spacing(), Spacing)

    def test_box_constraints(self):
        self._roundtrip(BoxConstraints(min_width=0, max_width=80, min_height=0, max_height=24), BoxConstraints)

    def test_layout_result(self):
        lr = LayoutResult(
            position=Position(x=0, y=0),
            size=Size(width=80, height=24),
            children=[
                LayoutResult(position=Position(x=5, y=5), size=Size(width=20, height=10)),
            ],
        )
        self._roundtrip(lr, LayoutResult)

    def test_renderable_spec(self):
        self._roundtrip(RenderableSpec(spec_type="text"), RenderableSpec)

    def test_style_spec(self):
        ss = StyleSpec(
            fg=ColorValue(r=255, g=0, b=0),
            bg=ColorValue(r=0, g=0, b=0),
            bold=True,
            italic=True,
        )
        self._roundtrip(ss, StyleSpec)

    def test_style_spec_no_colors(self):
        ss = StyleSpec(bold=True)
        self._roundtrip(ss, StyleSpec)

    def test_terminal_capabilities(self):
        tc = TerminalCapabilities(
            color_depth=ColorDepth.TRUECOLOR,
            size=Size(width=120, height=40),
            unicode_support=True,
        )
        self._roundtrip(tc, TerminalCapabilities)

    def test_box_model(self):
        bm = BoxModel(
            margin=Spacing(top=1, right=1, bottom=1, left=1),
            padding=Spacing(top=2, right=2, bottom=2, left=2),
            width=40,
            height=20,
            flex_grow=1.0,
            flex_shrink=0.5,
        )
        self._roundtrip(bm, BoxModel)

    def test_flex_container(self):
        fc = FlexContainer(direction=FlexDirection.COLUMN, gap=2, wrap=True)
        self._roundtrip(fc, FlexContainer)

    def test_layout_node(self):
        node = LayoutNode(
            spec=RenderableSpec(spec_type="box"),
            box=BoxModel(width=40),
            flex=FlexContainer(direction=FlexDirection.ROW),
            children=[
                LayoutNode(spec=RenderableSpec(spec_type="text"), box=BoxModel(width=20)),
            ],
        )
        self._roundtrip(node, LayoutNode)

    def test_animation_spec(self):
        a = AnimationSpec(fps=30.0, duration_ms=1000.0, callback_id="spinner")
        self._roundtrip(a, AnimationSpec)

    def test_animation_spec_infinite(self):
        a = AnimationSpec(fps=60.0, duration_ms=None, callback_id="loop")
        self._roundtrip(a, AnimationSpec)

    def test_scheduler_state(self):
        s = SchedulerState(
            animations={"a": AnimationSpec(fps=10, duration_ms=500, callback_id="a")},
            frame_counts={"a": 3},
            start_times={"a": 100.0},
        )
        self._roundtrip(s, SchedulerState)

    def test_theme_tokens(self):
        t = load_theme_from_dict(CATPPUCCIN_MOCHA)
        self._roundtrip(t, ThemeTokens)


# ===================================================================
# Capability detection tests
# ===================================================================

class TestCapabilityDetection:
    def test_detect_truecolor(self):
        with mock.patch.dict(os.environ, {"COLORTERM": "truecolor"}, clear=False):
            assert detect_color_depth() == ColorDepth.TRUECOLOR

    def test_detect_24bit(self):
        with mock.patch.dict(os.environ, {"COLORTERM": "24bit"}, clear=False):
            assert detect_color_depth() == ColorDepth.TRUECOLOR

    def test_detect_256(self):
        env = {"COLORTERM": "", "TERM": "xterm-256color"}
        with mock.patch.dict(os.environ, env, clear=False):
            assert detect_color_depth() == ColorDepth.COLOR_256

    def test_detect_16(self):
        env = {"COLORTERM": "", "TERM": "xterm"}
        with mock.patch.dict(os.environ, env, clear=False):
            assert detect_color_depth() == ColorDepth.COLOR_16

    def test_detect_monochrome(self):
        env = {"COLORTERM": "", "TERM": "dumb"}
        with mock.patch.dict(os.environ, env, clear=False):
            assert detect_color_depth() == ColorDepth.MONOCHROME

    def test_detect_terminal_size_fallback(self):
        with mock.patch("os.get_terminal_size", side_effect=OSError):
            size = detect_terminal_size()
            assert size == Size(width=80, height=24)

    def test_detect_unicode_support_utf8(self):
        with mock.patch.dict(os.environ, {"LANG": "en_US.UTF-8"}, clear=False):
            assert detect_unicode_support() is True

    def test_detect_unicode_support_none(self):
        env = {"LANG": "", "LC_ALL": "", "LC_CTYPE": ""}
        with mock.patch.dict(os.environ, env, clear=False):
            assert detect_unicode_support() is False


# ===================================================================
# Color resolution tests
# ===================================================================

class TestColorResolution:
    def test_truecolor_passthrough(self):
        c = ColorValue(r=137, g=180, b=250)
        assert resolve_color(c, ColorDepth.TRUECOLOR) == (137, 180, 250)

    def test_256_resolution(self):
        c = ColorValue(r=137, g=180, b=250)
        result = resolve_color(c, ColorDepth.COLOR_256)
        assert result is not None
        assert len(result) == 3
        # Should be close to the original
        assert color_distance(result, (137, 180, 250)) < 60

    def test_16_resolution(self):
        c = ColorValue(r=255, g=0, b=0)
        result = resolve_color(c, ColorDepth.COLOR_16)
        assert result is not None
        assert result in ANSI_16_COLORS

    def test_monochrome_returns_none(self):
        c = ColorValue(r=100, g=200, b=50)
        assert resolve_color(c, ColorDepth.MONOCHROME) is None

    def test_exact_ansi_match(self):
        # Pure red should map to ANSI bright red (255,0,0)
        c = ColorValue(r=255, g=0, b=0)
        result = resolve_color(c, ColorDepth.COLOR_16)
        assert result == (255, 0, 0)

    def test_color_distance_zero(self):
        assert color_distance((0, 0, 0), (0, 0, 0)) == 0.0

    def test_color_distance_known(self):
        # Distance from black to white
        d = color_distance((0, 0, 0), (255, 255, 255))
        assert abs(d - 441.67) < 1.0  # sqrt(3 * 255^2) ≈ 441.67

    def test_interpolate_color_endpoints(self):
        c1 = ColorValue(r=0, g=0, b=0)
        c2 = ColorValue(r=255, g=255, b=255)
        assert interpolate_color(c1, c2, 0.0) == c1
        assert interpolate_color(c1, c2, 1.0) == c2

    def test_interpolate_color_midpoint(self):
        c1 = ColorValue(r=0, g=0, b=0)
        c2 = ColorValue(r=200, g=100, b=50)
        mid = interpolate_color(c1, c2, 0.5)
        assert mid.r == 100
        assert mid.g == 50
        assert mid.b == 25

    def test_interpolate_color_clamp(self):
        c1 = ColorValue(r=0, g=0, b=0)
        c2 = ColorValue(r=255, g=255, b=255)
        # t beyond [0,1] should be clamped
        assert interpolate_color(c1, c2, -0.5) == c1
        assert interpolate_color(c1, c2, 1.5) == c2


# ===================================================================
# Layout computation tests
# ===================================================================

class TestLayoutComputation:
    def test_leaf_node(self):
        node = LayoutNode(
            spec=RenderableSpec(spec_type="box"),
            box=BoxModel(width=20, height=10),
        )
        constraints = BoxConstraints(min_width=0, max_width=80, min_height=0, max_height=24)
        result = compute_layout(node, constraints)
        assert result.size.width == 20
        assert result.size.height == 10
        assert result.position.x == 0
        assert result.position.y == 0

    def test_leaf_with_margin(self):
        node = LayoutNode(
            spec=RenderableSpec(spec_type="box"),
            box=BoxModel(width=20, height=10, margin=Spacing(left=5, top=3)),
        )
        constraints = BoxConstraints(min_width=0, max_width=80, min_height=0, max_height=24)
        result = compute_layout(node, constraints)
        assert result.position.x == 5
        assert result.position.y == 3

    def test_flex_row(self):
        """Three children in a flex row should be laid out horizontally."""
        children = [
            LayoutNode(
                spec=RenderableSpec(spec_type="box"),
                box=BoxModel(width=20, height=10, flex_grow=1.0),
            )
            for _ in range(3)
        ]
        node = LayoutNode(
            spec=RenderableSpec(spec_type="container"),
            box=BoxModel(width=80, height=24),
            flex=FlexContainer(direction=FlexDirection.ROW, gap=0),
            children=children,
        )
        constraints = BoxConstraints(min_width=0, max_width=80, min_height=0, max_height=24)
        result = compute_layout(node, constraints)

        # Should have 3 children
        assert len(result.children) == 3
        # Children should be at different x positions
        xs = [c.position.x for c in result.children]
        assert xs[0] < xs[1] < xs[2]

    def test_flex_column(self):
        """Two children in a flex column should be laid out vertically."""
        children = [
            LayoutNode(
                spec=RenderableSpec(spec_type="box"),
                box=BoxModel(width=40, height=8, flex_grow=1.0),
            )
            for _ in range(2)
        ]
        node = LayoutNode(
            spec=RenderableSpec(spec_type="container"),
            box=BoxModel(width=80, height=24),
            flex=FlexContainer(direction=FlexDirection.COLUMN, gap=0),
            children=children,
        )
        constraints = BoxConstraints(min_width=0, max_width=80, min_height=0, max_height=24)
        result = compute_layout(node, constraints)

        assert len(result.children) == 2
        ys = [c.position.y for c in result.children]
        assert ys[0] < ys[1]

    def test_flex_row_with_gap(self):
        """Gap should add spacing between children."""
        children = [
            LayoutNode(
                spec=RenderableSpec(spec_type="box"),
                box=BoxModel(width=10, height=5),
            )
            for _ in range(3)
        ]
        node = LayoutNode(
            spec=RenderableSpec(spec_type="container"),
            box=BoxModel(width=80, height=24),
            flex=FlexContainer(direction=FlexDirection.ROW, gap=2),
            children=children,
        )
        constraints = BoxConstraints(min_width=0, max_width=80, min_height=0, max_height=24)
        result = compute_layout(node, constraints)

        # gap=2 between each child
        assert result.children[1].position.x >= result.children[0].position.x + 10 + 2


# ===================================================================
# Scheduler tests
# ===================================================================

class TestScheduler:
    def test_create_scheduler(self):
        s = create_scheduler()
        assert len(s.animations) == 0

    def test_register_animation(self):
        s = create_scheduler()
        spec = AnimationSpec(fps=10, duration_ms=1000, callback_id="test")
        s2 = register_animation(s, spec)
        assert "test" in s2.animations
        # Original unchanged (immutable)
        assert "test" not in s.animations

    def test_unregister_animation(self):
        s = create_scheduler()
        spec = AnimationSpec(fps=10, duration_ms=1000, callback_id="test")
        s2 = register_animation(s, spec)
        s3 = unregister_animation(s2, "test")
        assert "test" not in s3.animations

    def test_tick_fires_callback(self):
        s = create_scheduler()
        spec = AnimationSpec(fps=10, duration_ms=5000, callback_id="spin")
        s = register_animation(s, spec)

        # First tick at t=0 initializes start time, no frame fires yet
        s, fired = tick(s, 0.0)
        assert fired == []

        # Tick at t=100ms: expected_frame = floor(100 * 10 / 1000) = 1 > 0
        s, fired = tick(s, 100.0)
        assert "spin" in fired

    def test_tick_respects_fps(self):
        s = create_scheduler()
        spec = AnimationSpec(fps=10, duration_ms=None, callback_id="x")
        s = register_animation(s, spec)

        s, _ = tick(s, 0.0)  # init
        s, fired = tick(s, 50.0)  # too early for frame 1 at 10fps (100ms interval)
        assert fired == []

    def test_tick_removes_completed(self):
        s = create_scheduler()
        spec = AnimationSpec(fps=10, duration_ms=100, callback_id="short")
        s = register_animation(s, spec)

        s, _ = tick(s, 0.0)
        s, _ = tick(s, 200.0)  # past duration
        assert "short" not in s.animations

    def test_is_animation_complete(self):
        s = create_scheduler()
        spec = AnimationSpec(fps=10, duration_ms=500, callback_id="c")
        s = register_animation(s, spec)
        s, _ = tick(s, 0.0)  # start

        assert is_animation_complete(s, "c", 200.0) is False
        assert is_animation_complete(s, "c", 600.0) is True

    def test_is_animation_complete_unregistered(self):
        s = create_scheduler()
        assert is_animation_complete(s, "nonexistent", 0.0) is True

    def test_infinite_animation(self):
        s = create_scheduler()
        spec = AnimationSpec(fps=10, duration_ms=None, callback_id="inf")
        s = register_animation(s, spec)
        s, _ = tick(s, 0.0)

        assert is_animation_complete(s, "inf", 999999.0) is False


# ===================================================================
# Theme tests
# ===================================================================

class TestTheme:
    def test_load_catppuccin(self):
        t = load_theme_from_dict(CATPPUCCIN_MOCHA)
        assert "primary" in t.colors
        assert t.colors["primary"].r == 137

    def test_load_dracula(self):
        t = load_theme_from_dict(DRACULA)
        assert "primary" in t.colors

    def test_load_tokyo_night(self):
        t = load_theme_from_dict(TOKYO_NIGHT)
        assert "primary" in t.colors

    def test_load_high_contrast(self):
        t = load_theme_from_dict(HIGH_CONTRAST)
        assert "primary" in t.colors

    def test_roundtrip_all_themes(self):
        for theme_dict in [CATPPUCCIN_MOCHA, DRACULA, TOKYO_NIGHT, HIGH_CONTRAST]:
            t = load_theme_from_dict(theme_dict)
            d = theme_to_dict(t)
            t2 = load_theme_from_dict(d)
            assert t == t2

    def test_resolve_token_color(self):
        t = load_theme_from_dict(CATPPUCCIN_MOCHA)
        c = resolve_token(t, "colors.primary")
        assert isinstance(c, ColorValue)
        assert c.r == 137

    def test_resolve_token_spacing(self):
        t = load_theme_from_dict(CATPPUCCIN_MOCHA)
        assert resolve_token(t, "spacing.md") == 4

    def test_resolve_token_border_glyph(self):
        t = load_theme_from_dict(CATPPUCCIN_MOCHA)
        assert resolve_token(t, "border_glyphs.rounded.tl") == "╭"

    def test_resolve_token_typography(self):
        t = load_theme_from_dict(CATPPUCCIN_MOCHA)
        assert resolve_token(t, "typography.bold_supported") is True

    def test_resolve_token_bad_path(self):
        t = load_theme_from_dict(CATPPUCCIN_MOCHA)
        with pytest.raises(KeyError):
            resolve_token(t, "colors.nonexistent")

    def test_resolve_token_short_path(self):
        t = load_theme_from_dict(CATPPUCCIN_MOCHA)
        with pytest.raises(KeyError):
            resolve_token(t, "colors")

    def test_all_themes_json_serializable(self):
        """All built-in theme dicts must survive JSON round-trip."""
        for name, theme_dict in [
            ("catppuccin_mocha", CATPPUCCIN_MOCHA),
            ("dracula", DRACULA),
            ("tokyo_night", TOKYO_NIGHT),
            ("high_contrast", HIGH_CONTRAST),
        ]:
            json_str = json.dumps(theme_dict)
            restored = json.loads(json_str)
            t1 = load_theme_from_dict(theme_dict)
            t2 = load_theme_from_dict(restored)
            assert t1 == t2, f"Theme {name} failed JSON round-trip"

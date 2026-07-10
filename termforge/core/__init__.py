"""TermForge core — layout, capability detection, theming, scheduler, Renderable protocol.

Re-exports all public types and functions from core submodules.
"""
from __future__ import annotations

# --- types ---
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

# --- capability ---
from termforge.core.capability import (
    TerminalCapabilities,
    detect_capabilities,
    detect_color_depth,
    detect_terminal_size,
    detect_unicode_support,
)

# --- color ---
from termforge.core.color import (
    ANSI_16_COLORS,
    color_distance,
    interpolate_color,
    resolve_color,
)

# --- theme ---
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

# --- layout ---
from termforge.core.layout import (
    BoxModel,
    FlexContainer,
    FlexDirection,
    LayoutNode,
    compute_layout,
)

# --- scheduler ---
from termforge.core.scheduler import (
    AnimationSpec,
    FrameCallback,
    SchedulerState,
    create_scheduler,
    is_animation_complete,
    register_animation,
    tick,
    unregister_animation,
)

__all__ = [
    # types
    "BoxConstraints",
    "ColorDepth",
    "ColorValue",
    "LayoutResult",
    "Position",
    "RenderableSpec",
    "Size",
    "Spacing",
    "StyleSpec",
    # capability
    "TerminalCapabilities",
    "detect_capabilities",
    "detect_color_depth",
    "detect_terminal_size",
    "detect_unicode_support",
    # color
    "ANSI_16_COLORS",
    "color_distance",
    "interpolate_color",
    "resolve_color",
    # theme
    "CATPPUCCIN_MOCHA",
    "DRACULA",
    "HIGH_CONTRAST",
    "TOKYO_NIGHT",
    "ThemeTokens",
    "load_theme_from_dict",
    "resolve_token",
    "theme_to_dict",
    # layout
    "BoxModel",
    "FlexContainer",
    "FlexDirection",
    "LayoutNode",
    "compute_layout",
    # scheduler
    "AnimationSpec",
    "FrameCallback",
    "SchedulerState",
    "create_scheduler",
    "is_animation_complete",
    "register_animation",
    "tick",
    "unregister_animation",
]

"""TermForge layout presets — common named UI patterns as RenderableSpec instances.

Each preset is a factory function that returns a fully-configured, JSON-serializable
RenderableSpec. Presets accept keyword arguments to parameterize dimensions, titles,
and content. All returned specs follow the portability contract: pure data, no
Rich/Textual types.

Usage::

    from termforge.config.presets import get_preset, list_presets

    spec = get_preset("dashboard", title="My App", width=120, height=40)
    spec = get_preset("split-pane", ratios=[1, 2], gap=1)
    spec = get_preset("modal-dialog", message="Are you sure?")
    spec = get_preset("log-viewer", title="Logs", width=80, height=20)
"""
from __future__ import annotations
from typing import Any
from termforge.core.types import RenderableSpec
from termforge.windows.types import WindowSpec, PaneSpec
from termforge.borders.types import BorderStyle
from termforge.core import FlexDirection
from termforge.text.types import TextSpec, TextOverflow


# Registry: name -> (factory_fn, description)
_PRESET_REGISTRY: dict[str, tuple[Any, str]] = {}


def _register(name: str, description: str):
    """Decorator to register a preset factory function."""
    def decorator(fn):
        _PRESET_REGISTRY[name] = (fn, description)
        return fn
    return decorator


# ---------------------------------------------------------------------------
# Preset: dashboard
# ---------------------------------------------------------------------------

@_register(
    "dashboard",
    "Bordered window with a header, scrollable body pane, and a status-bar footer."
)
def _preset_dashboard(
    title: str = "Dashboard",
    width: int = 120,
    height: int = 40,
    header_text: str = "",
    footer_text: str = "",
    border_style: str = "single",
    **kwargs: Any,
) -> RenderableSpec:
    """Three-row vertical pane: header (3 rows) / body (rest) / footer (3 rows)."""
    header_h = 3
    footer_h = 3
    body_h = max(4, height - header_h - footer_h)
    total_h = header_h + body_h + footer_h

    # Ratios relative to total
    header_ratio = header_h / total_h
    body_ratio = body_h / total_h
    footer_ratio = footer_h / total_h

    header_spec = WindowSpec(
        title=header_text or f"── {title} ──",
        border_style=BorderStyle(border_style),
        width=width,
        height=header_h,
    )
    body_spec = WindowSpec(
        title="",
        border_style=BorderStyle(border_style),
        width=width,
        height=body_h,
        scroll_y=0,
    )
    footer_spec = WindowSpec(
        title=footer_text or "Status",
        border_style=BorderStyle(border_style),
        width=width,
        height=footer_h,
    )

    return PaneSpec(
        direction=FlexDirection.COLUMN,
        children=[header_spec, body_spec, footer_spec],
        ratios=[header_ratio, body_ratio, footer_ratio],
        gap=0,
    )


# ---------------------------------------------------------------------------
# Preset: split-pane (horizontal)
# ---------------------------------------------------------------------------

@_register(
    "split-pane",
    "Two horizontal panes side-by-side with configurable ratios and gap."
)
def _preset_split_pane(
    ratios: list[float] | None = None,
    gap: int = 1,
    border_style: str = "single",
    left_title: str = "Left",
    right_title: str = "Right",
    width: int = 120,
    height: int = 30,
    **kwargs: Any,
) -> RenderableSpec:
    r = ratios or [1.0, 1.0]
    left = WindowSpec(
        title=left_title,
        border_style=BorderStyle(border_style),
        width=None,
        height=height,
    )
    right = WindowSpec(
        title=right_title,
        border_style=BorderStyle(border_style),
        width=None,
        height=height,
    )
    return PaneSpec(
        direction=FlexDirection.ROW,
        children=[left, right],
        ratios=r,
        gap=gap,
    )


# ---------------------------------------------------------------------------
# Preset: split-pane-v (vertical)
# ---------------------------------------------------------------------------

@_register(
    "split-pane-v",
    "Two vertical panes stacked top-and-bottom with configurable ratios and gap."
)
def _preset_split_pane_v(
    ratios: list[float] | None = None,
    gap: int = 0,
    border_style: str = "single",
    top_title: str = "Top",
    bottom_title: str = "Bottom",
    width: int = 80,
    height: int = 30,
    **kwargs: Any,
) -> RenderableSpec:
    r = ratios or [1.0, 1.0]
    top = WindowSpec(
        title=top_title,
        border_style=BorderStyle(border_style),
        width=width,
        height=None,
    )
    bottom = WindowSpec(
        title=bottom_title,
        border_style=BorderStyle(border_style),
        width=width,
        height=None,
    )
    return PaneSpec(
        direction=FlexDirection.COLUMN,
        children=[top, bottom],
        ratios=r,
        gap=gap,
    )


# ---------------------------------------------------------------------------
# Preset: modal-dialog
# ---------------------------------------------------------------------------

@_register(
    "modal-dialog",
    "Centered modal window with a title, message body, and a rounded border."
)
def _preset_modal_dialog(
    title: str = "Dialog",
    message: str = "",
    width: int = 50,
    height: int = 10,
    border_style: str = "rounded",
    buttons: list[str] | None = None,
    **kwargs: Any,
) -> RenderableSpec:
    # Compose message + optional button row into the window title/tags
    tag_list = buttons or ["OK"]
    return WindowSpec(
        title=title,
        border_style=BorderStyle(border_style),
        width=width,
        height=height,
        tags=tag_list,
        padding=1,
    )


# ---------------------------------------------------------------------------
# Preset: log-viewer
# ---------------------------------------------------------------------------

@_register(
    "log-viewer",
    "Scrollable bordered text window optimised for log / output display."
)
def _preset_log_viewer(
    title: str = "Logs",
    width: int = 80,
    height: int = 20,
    border_style: str = "single",
    scroll_y: int = 0,
    text_overflow: str = "truncate",
    **kwargs: Any,
) -> RenderableSpec:
    from termforge.text.types import TextOverflow as TO
    overflow = TO(text_overflow) if text_overflow else TO.TRUNCATE
    return WindowSpec(
        title=title,
        border_style=BorderStyle(border_style),
        width=width,
        height=height,
        scroll_y=scroll_y,
        text_overflow=overflow,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def list_presets() -> list[dict[str, str]]:
    """Return a list of available preset names and their descriptions.

    Returns:
        List of dicts with keys ``"name"`` and ``"description"``.

    Example::

        >>> from termforge.config.presets import list_presets
        >>> for p in list_presets():
        ...     print(p["name"], "-", p["description"])
    """
    return [
        {"name": name, "description": desc}
        for name, (_, desc) in sorted(_PRESET_REGISTRY.items())
    ]


def get_preset(name: str, **kwargs: Any) -> RenderableSpec:
    """Instantiate a named layout preset with optional parameter overrides.

    Args:
        name: Preset name (see :func:`list_presets` for available names).
        **kwargs: Parameters forwarded to the preset factory.  Each preset
            documents its own accepted keyword arguments.

    Returns:
        A fully-configured :class:`~termforge.core.types.RenderableSpec`
        instance.  The returned spec is JSON-serializable (portability
        contract: call ``spec.to_dict()`` to verify).

    Raises:
        ValueError: If ``name`` is not a registered preset.

    Example::

        >>> from termforge.config.presets import get_preset
        >>> spec = get_preset("dashboard", title="My App", width=120, height=40)
        >>> d = spec.to_dict()          # portability contract — must not raise
        >>> assert d["spec_type"] == "pane"
    """
    if name not in _PRESET_REGISTRY:
        available = ", ".join(sorted(_PRESET_REGISTRY))
        raise ValueError(
            f"Unknown preset {name!r}. Available presets: {available}"
        )
    factory, _ = _PRESET_REGISTRY[name]
    return factory(**kwargs)

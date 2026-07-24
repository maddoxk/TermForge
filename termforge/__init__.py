"""TermForge v2.0.0 — A Universal Terminal UI/UX Design System.

Top-level developer-friendly API: render components, layouts, themes, and interactive displays effortlessly.
"""
from __future__ import annotations

__version__ = "2.0.0"

from termforge.core.types import Size, ColorDepth, RenderableSpec
from termforge.core.capability import detect_capabilities
from termforge.core.theme import ThemeTokens, load_theme_from_dict, TOKYO_NIGHT
from termforge.config.input import InputBindingSpec, InputRouter
from termforge.reactive import State, View, stream, animate_val



# Import specs from config/modules
from termforge.accordion.types import AccordionSpec, AccordionItemSpec
from termforge.animation.types import SpinnerSpec
from termforge.badge.types import BadgeSpec
from termforge.borders.types import BorderStyle
from termforge.buttongroup.types import ButtonGroupSpec
from termforge.card.types import CardSpec
from termforge.charts.types import ChartSpec, ChartType, OHLCSeries
from termforge.checklist.types import ChecklistSpec, ChecklistItemSpec
from termforge.combobox.types import ComboboxSpec
from termforge.dialog.types import DialogSpec
from termforge.divider.types import DividerSpec
from termforge.image.types import ImageSpec
from termforge.keylegend.types import KeyLegendSpec
from termforge.keyvalue.types import KeyValueGridSpec, KeyValueItemSpec
from termforge.logging.types import LogStreamerSpec
from termforge.logos.types import LogoSpec
from termforge.menu.types import MenuBarSpec, MenuItemSpec
from termforge.navigation.types import BreadcrumbsSpec
from termforge.progress.types import ProgressSpec
from termforge.radio.types import RadioButtonSpec, RadioButtonItemSpec
from termforge.search.types import SearchBarSpec
from termforge.selection.types import SelectionListSpec, SelectionItemSpec
from termforge.slider.types import SliderSpec
from termforge.spinnerbox.types import SpinnerBoxSpec
from termforge.statusbar.types import StatusBarSpec, StatusSectionSpec
from termforge.stepper.types import StepperSpec
from termforge.tables.types import TableSpec, ColumnSpec
from termforge.tabs.types import TabSpec
from termforge.text.types import TextSpec
from termforge.toast.types import ToastSpec
from termforge.toggle.types import ToggleSwitchSpec
from termforge.tooltip.types import TooltipSpec
from termforge.tree.types import TreeSpec, TreeNodeSpec
from termforge.windows.types import WindowSpec, PaneSpec

# Renderers
from termforge.accordion.render import render_accordion
from termforge.animation.spinners import render_spinner
from termforge.badge.render import render_badge
from termforge.buttongroup.render import render_buttongroup
from termforge.card.render import render_card
from termforge.charts.chart import render_chart
from termforge.checklist.render import render_checklist
from termforge.combobox.render import render_combobox
from termforge.dialog.render import render_dialog
from termforge.divider.render import render_divider
from termforge.image.render import render_image
from termforge.keylegend.render import render_key_legend
from termforge.keyvalue.render import render_keyvalue_grid
from termforge.logging.render import render_log_streamer
from termforge.logos.render import render_logo
from termforge.menu.render import render_menu_bar
from termforge.navigation.render import render_breadcrumbs
from termforge.progress.render import render_progress
from termforge.radio.render import render_radio_button
from termforge.search.render import render_search_bar
from termforge.selection.render import render_selection_list
from termforge.slider.render import render_slider
from termforge.spinnerbox.render import render_spinner_box
from termforge.statusbar.render import render_status_bar
from termforge.stepper.render import render_stepper
from termforge.tables.render import render_table
from termforge.tabs.render import render_tabs
from termforge.text.render import render_text
from termforge.toast.render import render_toast
from termforge.toggle.render import render_toggle_switch
from termforge.tooltip.render import render_tooltip
from termforge.tree.render import render_tree
from termforge.windows.compositor import render_window, compose_panes

def _adapt_text(spec: Any, size: Size, theme: Any, depth: Any) -> list[str]:
    return render_text(spec, theme=theme, depth=depth, available_width=size.width)

def _adapt_spinner(spec: Any, size: Size, theme: Any, depth: Any) -> list[str]:
    res = render_spinner(spec, frame_number=0, theme=theme, depth=depth)
    return [res]

def _adapt_window(spec: Any, size: Size, theme: Any, depth: Any) -> list[str]:
    content_str = spec.content if isinstance(spec.content, str) else ""
    content_lines = content_str.split("\n") if content_str else []
    return render_window(spec, content_lines=content_lines, theme=theme, depth=depth)

# Standard registry of specs -> renderers
_RENDERER_MAP = {
    "accordion": render_accordion,
    "spinner": _adapt_spinner,
    "badge": render_badge,
    "buttongroup": render_buttongroup,
    "card": render_card,
    "chart": render_chart,
    "checklist": render_checklist,
    "combobox": render_combobox,
    "dialog": render_dialog,
    "divider": render_divider,
    "image": render_image,
    "key_legend": render_key_legend,
    "keyvalue_grid": render_keyvalue_grid,
    "log_streamer": render_log_streamer,
    "logo": render_logo,
    "menu_bar": render_menu_bar,
    "breadcrumbs": render_breadcrumbs,
    "progress": render_progress,
    "radio": render_radio_button,
    "searchbar": render_search_bar,
    "selection": render_selection_list,
    "slider": render_slider,
    "spinnerbox": render_spinner_box,
    "status_bar": render_status_bar,
    "stepper": render_stepper,
    "table": render_table,
    "tabs": render_tabs,
    "text": _adapt_text,
    "toast": render_toast,
    "toggle": render_toggle_switch,
    "tooltip": render_tooltip,
    "tree": render_tree,
    "window": _adapt_window,
}


def render(
    spec: RenderableSpec,
    width: int = 80,
    height: int = 24,
    theme: ThemeTokens | None = None,
    depth: ColorDepth | None = None,
) -> list[str]:
    """Universal high-level render function for any TermForge component spec.

    Args:
        spec: Any component specification instance (e.g. CardSpec, ProgressSpec, TableSpec).
        width: Viewport rendering width in character columns (default 80).
        height: Viewport rendering height in character rows (default 24).
        theme: Optional theme tokens (defaults to Tokyo Night theme if None).
        depth: Optional color depth (defaults to auto-detected terminal capability).

    Returns:
        List of formatted string lines for terminal output.

    Example:
        >>> import termforge as tf
        >>> print(tf.draw(tf.CardSpec(title="System Status", content="All systems nominal")))
    """
    if depth is None:
        depth = detect_capabilities().color_depth
    if theme is None:
        theme = load_theme_from_dict(TOKYO_NIGHT)

    size = Size(width, height)
    spec_type = getattr(spec, "spec_type", None)

    if spec_type == "pane" and isinstance(spec, PaneSpec):
        return compose_panes(spec, size, theme=theme, depth=depth)
    
    renderer = _RENDERER_MAP.get(str(spec_type))
    if renderer:
        return renderer(spec, size, theme=theme, depth=depth) # type: ignore

    raise ValueError(f"No renderer registered for spec_type '{spec_type}'")


def draw(
    spec: RenderableSpec,
    width: int = 80,
    height: int = 24,
    theme: ThemeTokens | None = None,
    depth: ColorDepth | None = None,
) -> str:
    """Render a component spec directly into a multi-line string ready to print().

    Args:
        spec: Any component specification instance.
        width: Canvas width (default 80).
        height: Canvas height (default 24).
        theme: Theme tokens.
        depth: Color depth tier.

    Returns:
        Newlines-joined formatted string.

    Example:
        >>> import termforge as tf
        >>> print(tf.draw(tf.BadgeSpec(text="SUCCESS", severity="success")))
    """
    lines = render(spec, width=width, height=height, theme=theme, depth=depth)
    return "\n".join(lines)


__all__ = [
    "__version__",
    "render",
    "draw",
    "State",
    "View",
    "stream",
    "animate_val",
    "InputBindingSpec",
    "InputRouter",
    "Size",
    "ColorDepth",
    "RenderableSpec",
    "ThemeTokens",
    # Specs
    "AccordionSpec",
    "AccordionItemSpec",
    "SpinnerSpec",
    "BadgeSpec",
    "BorderStyle",
    "ButtonGroupSpec",
    "CardSpec",
    "ChartSpec",
    "ChartType",
    "OHLCSeries",
    "ChecklistSpec",
    "ChecklistItemSpec",
    "ComboboxSpec",
    "DialogSpec",
    "DividerSpec",
    "ImageSpec",
    "KeyLegendSpec",
    "KeyValueGridSpec",
    "KeyValueItemSpec",
    "LogStreamerSpec",
    "LogoSpec",
    "MenuBarSpec",
    "MenuItemSpec",
    "BreadcrumbsSpec",
    "ProgressSpec",
    "RadioButtonSpec",
    "RadioButtonItemSpec",
    "SearchBarSpec",
    "SelectionListSpec",
    "SelectionItemSpec",
    "SliderSpec",
    "SpinnerBoxSpec",
    "StatusBarSpec",
    "StatusSectionSpec",
    "StepperSpec",
    "TableSpec",
    "ColumnSpec",
    "TabSpec",
    "TextSpec",
    "ToastSpec",
    "ToggleSwitchSpec",
    "TooltipSpec",
    "TreeSpec",
    "TreeNodeSpec",
    "WindowSpec",
    "PaneSpec",
]

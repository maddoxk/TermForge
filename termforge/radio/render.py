"""TermForge radio button component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.radio.types import RadioButtonSpec, RadioButtonItemSpec


def _style_part(text: str, token: str | None, theme: ThemeTokens | None, depth: ColorDepth) -> str:
    if not token or not theme or depth == ColorDepth.MONOCHROME:
        return text
    token_path = token if token.startswith("colors.") else f"colors.{token}"
    try:
        res = resolve_token(theme, token_path)
        if isinstance(res, ColorValue):
            style = StyleSpec(fg=ColorValue(res.r, res.g, res.b, name=None))
            start, end = style_to_ansi(style, theme, depth)
            return f"{start}{text}{end}"
    except KeyError:
        pass
    return text


def render_radio_button(
    spec: RadioButtonSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the RadioButton component to layout lines.

    Args:
        spec: RadioButtonSpec containing radio choices.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0:
        return []

    lines = []
    for idx, item in enumerate(spec.items):
        # 1. Indicator
        ind = spec.active_indicator if item.active else spec.inactive_indicator
        
        # 2. Styling decision
        is_selected = (idx == spec.selected_idx)
        if is_selected:
            style_token = spec.selected_style
        else:
            style_token = spec.active_style if item.active else spec.inactive_style
            
        styled_ind = _style_part(ind, style_token, theme, depth)
        styled_label = _style_part(item.label, style_token, theme, depth)
        
        line = f"{styled_ind}{styled_label}"
        
        # Padding spaces
        raw_len = len(ind) + len(item.label)
        if raw_len < max_size.width:
            line += " " * (max_size.width - raw_len)
            
        lines.append(line)

    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

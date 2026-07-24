"""TermForge button group component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.buttongroup.types import ButtonGroupSpec


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


def render_buttongroup(
    spec: ButtonGroupSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the ButtonGroup component to layout lines.

    Args:
        spec: ButtonGroupSpec containing list of buttons and selected index.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if not spec.buttons or max_size.height <= 0 or max_size.width <= 0:
        return []

    styled_segments = []
    raw_lens = []

    for idx, lbl in enumerate(spec.buttons):
        raw_btn = f"[ {lbl} ]"
        is_selected = (idx == spec.selected_idx)
        token = spec.selected_style if is_selected else spec.unselected_style
        
        styled_btn = _style_part(raw_btn, token, theme, depth)
        styled_segments.append(styled_btn)
        raw_lens.append(len(raw_btn))

    sep = spec.separator if spec.separator is not None else "   "
    line = sep.join(styled_segments)

    total_raw_len = sum(raw_lens) + len(sep) * (len(spec.buttons) - 1)
    if total_raw_len < max_size.width:
        line += " " * (max_size.width - total_raw_len)

    lines = [line]
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

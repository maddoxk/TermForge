"""TermForge accordion component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.accordion.types import AccordionSpec, AccordionItemSpec


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


def render_accordion(
    spec: AccordionSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the Accordion component to layout lines.

    Args:
        spec: AccordionSpec containing sections stack and styles.
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
        # 1. Format section header title line
        caret = spec.expanded_caret if item.is_expanded else spec.collapsed_caret
        
        is_selected = (idx == spec.selected_idx)
        if is_selected:
            style_token = spec.selected_style
        else:
            style_token = spec.active_style if item.is_expanded else spec.inactive_style
            
        styled_caret = _style_part(caret, style_token, theme, depth)
        styled_title = _style_part(item.title, style_token, theme, depth)
        
        hdr_line = f"{styled_caret}{styled_title}"
        hdr_raw_len = len(caret) + len(item.title)
        if hdr_raw_len < max_size.width:
            hdr_line += " " * (max_size.width - hdr_raw_len)
            
        lines.append(hdr_line)

        # 2. Format details indented block
        if item.is_expanded and item.details:
            details_lines = item.details.split("\n")
            for det in details_lines:
                raw_det = f"    {det}"
                styled_det = _style_part(raw_det, spec.details_style, theme, depth)
                det_raw_len = len(raw_det)
                if det_raw_len < max_size.width:
                    styled_det += " " * (max_size.width - det_raw_len)
                lines.append(styled_det)

    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

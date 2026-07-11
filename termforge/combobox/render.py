"""TermForge combobox component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.combobox.types import ComboboxSpec


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


def render_combobox(
    spec: ComboboxSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the Combobox component to layout lines.

    Args:
        spec: ComboboxSpec containing options list and status parameters.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if not spec.options or max_size.height <= 0 or max_size.width <= 0:
        return [" " * max_size.width] * max_size.height

    # 1. Format closed input field (Line 0)
    selected_opt = spec.options[spec.selected_idx]
    max_opt_len = max(len(opt) for opt in spec.options)
    padded_opt = selected_opt.ljust(max_opt_len)
    
    raw_field = f"[ {padded_opt} ] {spec.caret}"
    styled_field = _style_part(raw_field, spec.field_style, theme, depth)
    
    field_len = len(raw_field)
    line0 = styled_field
    if field_len < max_size.width:
        line0 += " " * (max_size.width - field_len)
        
    lines = [line0]

    # 2. Render Open Dropdown list (Lines 1..H)
    if spec.is_open:
        inner_w = max_opt_len + 2
        box_w = inner_w + 2
        box_h = len(spec.options) + 2
        
        # Build box lines
        box_lines = []
        
        border_style_token = "border"
        s_tl = _style_part("┌", border_style_token, theme, depth)
        s_tr = _style_part("┐", border_style_token, theme, depth)
        s_bl = _style_part("└", border_style_token, theme, depth)
        s_br = _style_part("┘", border_style_token, theme, depth)
        s_h = _style_part("─", border_style_token, theme, depth)
        s_v = _style_part("│", border_style_token, theme, depth)
        
        box_lines.append(s_tl + s_h * inner_w + s_tr)
        
        for idx, option in enumerate(spec.options):
            padded_option = f" {option.ljust(max_opt_len)} "
            
            is_hover = (idx == spec.active_hover_idx)
            opt_token = spec.hover_style if is_hover else spec.dropdown_style
            
            styled_option = _style_part(padded_option, opt_token, theme, depth)
            box_lines.append(f"{s_v}{styled_option}{s_v}")
            
        box_lines.append(s_bl + s_h * inner_w + s_br)

        # Overlay box lines below input field
        start_x = 0
        for r in range(1, max_size.height):
            box_idx = r - 1
            if box_idx < len(box_lines):
                box_line = box_lines[box_idx]
                
                left_space = " " * start_x
                right_space = " " * max(0, max_size.width - start_x - box_w)
                line = f"{left_space}{box_line}{right_space}"
                lines.append(line)
            else:
                lines.append(" " * max_size.width)
    else:
        # Fill remaining lines with background space
        while len(lines) < max_size.height:
            lines.append(" " * max_size.width)

    return lines[:max_size.height]

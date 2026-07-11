"""TermForge status menu bar trail renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.menu.types import MenuBarSpec


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


def render_menu_bar(
    spec: MenuBarSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the MenuBar component to status lines.

    Args:
        spec: MenuBarSpec containing top-level menus and open dropdown index.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens for style resolution.
        depth: Color depth tier to simulate.

    Returns:
        List of rendered lines.
    """
    if not spec.menus or max_size.height <= 0 or max_size.width <= 0:
        return []

    # 1. Render Top Menu Bar (Line 0)
    top_parts = []
    col_offsets = []
    current_col = 0
    sep = " " * spec.spacing

    for idx, menu in enumerate(spec.menus):
        label_text = f" {menu.label} "
        
        # Style active selection
        is_selected = (idx == spec.selected_idx)
        style_token = spec.selected_style if is_selected else spec.menu_style
        
        styled_label = _style_part(label_text, style_token, theme, depth)
        
        if idx > 0:
            top_parts.append(sep)
            current_col += len(sep)
            
        col_offsets.append(current_col)
        top_parts.append(styled_label)
        current_col += len(label_text)

    # Pad top line to full width
    raw_top_len = sum(len(f" {m.label} ") for m in spec.menus) + spec.spacing * (len(spec.menus) - 1)
    pad_len = max(0, max_size.width - raw_top_len)
    top_parts.append(" " * pad_len)
    top_line = "".join(top_parts)

    lines = [top_line]

    # 2. Render Dropdown Overlay if active
    if spec.active_menu_idx is not None and spec.active_menu_idx < len(spec.menus):
        active_menu = spec.menus[spec.active_menu_idx]
        if active_menu.children:
            # Determine dropdown dimensions
            inner_w = max(len(child) for child in active_menu.children)
            box_w = inner_w + 2
            
            # Get starting column offset
            start_col = col_offsets[spec.active_menu_idx]
            
            # Prevent clipping on the right edge: shift left if it overflows max_size.width
            if start_col + box_w > max_size.width:
                start_col = max(0, max_size.width - box_w)

            # Build dropdown box lines
            box_lines = []
            
            # Top Border
            box_lines.append("┌" + "─" * inner_w + "┐")
            
            # Children rows
            for c_idx, child in enumerate(active_menu.children):
                if child == "-":
                    box_lines.append("├" + "─" * inner_w + "┤")
                else:
                    padded = child.ljust(inner_w)
                    
                    # Style child selection
                    is_child_selected = (c_idx == spec.selected_child_idx)
                    child_token = spec.dropdown_selected_style if is_child_selected else spec.dropdown_style
                    
                    styled_child = _style_part(padded, child_token, theme, depth)
                    box_lines.append(f"│{styled_child}│")
                    
            # Bottom Border
            box_lines.append("└" + "─" * inner_w + "┘")

            # Overlay box lines below the menu bar
            for r in range(1, max_size.height):
                box_idx = r - 1
                if box_idx < len(box_lines):
                    box_line = box_lines[box_idx]
                    
                    # Sandwich styled dropdown line inside left/right spacers
                    left_space = " " * start_col
                    right_space = " " * max(0, max_size.width - start_col - box_w)
                    
                    line = f"{left_space}{box_line}{right_space}"
                    lines.append(line)

                else:
                    # Fill background lines with space
                    lines.append(" " * max_size.width)

    # 3. Fill remaining lines to match requested height
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

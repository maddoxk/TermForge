from __future__ import annotations
from termforge.core.types import Size, Position, ColorDepth, StyleSpec, ColorValue, RenderableSpec
from termforge.core.theme import ThemeTokens, resolve_state_token
from termforge.core import FlexDirection
from termforge.windows.types import WindowSpec, PaneSpec, ModalSpec
from termforge.borders.types import BorderSpec, BorderSide, BorderStyle
from termforge.borders.render import render_border, strip_ansi
from termforge.text.render import style_to_ansi

def compose_panes(spec: PaneSpec, available: Size) -> list[tuple[Position, Size, RenderableSpec]]:
    if not spec.children:
        return []
        
    num_children = len(spec.children)
    ratios = spec.ratios
    if ratios is None or len(ratios) != num_children:
        ratios = [1.0] * num_children
        
    total_ratio = sum(ratios)
    gaps_space = spec.gap * (num_children - 1)
    
    results = []
    
    if spec.direction == FlexDirection.ROW:
        rem_w = max(0, available.width - gaps_space)
        curr_x = 0
        for i, child in enumerate(spec.children):
            w = int((ratios[i] / total_ratio) * rem_w)
            # Adjust last child to prevent rounding gaps
            if i == num_children - 1:
                w = available.width - curr_x
            child_size = Size(width=max(1, w), height=available.height)
            child_pos = Position(x=curr_x, y=0)
            results.append((child_pos, child_size, child))
            curr_x += w + spec.gap
            
    else: # FlexDirection.COLUMN
        rem_h = max(0, available.height - gaps_space)
        curr_y = 0
        for i, child in enumerate(spec.children):
            h = int((ratios[i] / total_ratio) * rem_h)
            if i == num_children - 1:
                h = available.height - curr_y
            child_size = Size(width=available.width, height=max(1, h))
            child_pos = Position(x=0, y=curr_y)
            results.append((child_pos, child_size, child))
            curr_y += h + spec.gap
            
    return results

def apply_scroll(lines: list[str], scroll_y: int, viewport_height: int) -> list[str]:
    if len(lines) <= viewport_height:
        return lines + [""] * (viewport_height - len(lines))
    start = max(0, min(scroll_y, len(lines) - viewport_height))
    return lines[start : start + viewport_height]

def z_sort(windows: list[WindowSpec]) -> list[WindowSpec]:
    return sorted(windows, key=lambda w: w.z_index)

def render_window(
    spec: WindowSpec,
    content_lines: list[str],
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR
) -> list[str]:
    # Determine window dimensions
    width = spec.width if spec.width is not None else 80
    height = spec.height if spec.height is not None else 24

    padding = max(0, spec.padding)  # inner padding (horizontal pad applied as left/right spaces)
    margin = max(0, spec.margin)    # outer margin (blank rows/cols around the whole result)

    # Inner dimensions: border takes 2 (1 per side) + padding takes 2*padding per axis
    inner_w = max(0, width - 2 - 2 * padding)
    inner_h = max(0, height - 2 - 2 * padding)

    # 1. Apply scroll to content lines
    scrolled_lines = apply_scroll(content_lines, spec.scroll_y, inner_h)

    # 1b. Apply inner padding (indent each content line and pad to inner_w)
    if padding > 0:
        pad_str = " " * padding
        padded_lines: list[str] = []
        # top padding rows
        for _ in range(padding):
            padded_lines.append(" " * (inner_w + 2 * padding))
        for line in scrolled_lines:
            # Strip trailing so we can safely pad
            padded_lines.append(pad_str + line[:inner_w].ljust(inner_w) + pad_str)
        # bottom padding rows
        for _ in range(padding):
            padded_lines.append(" " * (inner_w + 2 * padding))
        scrolled_lines = padded_lines

    border_spec = BorderSpec(
        style=spec.border_style,
        title=spec.title,
        content=spec.content,
        tags=spec.tags,
        title_align=spec.title_align,
        title_pad=spec.title_pad,
    )
    
    # 3. Render the border
    bordered = render_border(border_spec, scrolled_lines, width=width, theme=theme, unicode_supported=True)
    
    # 4. Apply highlight styling to border if focused/stateful
    state = "disabled" if getattr(spec, "disabled", False) else ("focused" if spec.focused else None)

    border_color = None
    if theme:
        try:
            border_color = resolve_state_token(theme, "colors.border", state=state)
        except KeyError:
            pass

    if isinstance(border_color, ColorValue):
        # Strip name to bypass re-resolution in style_to_ansi
        border_color = ColorValue(border_color.r, border_color.g, border_color.b, name=None)
    else:
        # Fallback to hardcoded names mapping to default colors
        border_color_token = "primary" if spec.focused else "border"
        border_color = ColorValue(0, 0, 0, name=f"colors.{border_color_token}")

    style = StyleSpec(fg=border_color)

    start_ansi, end_ansi = style_to_ansi(style, theme, depth)
    
    # 3b. Compute scrollbar lines if active
    scrollbar_lines = None
    if spec.show_scrollbar and len(content_lines) > inner_h and inner_h > 0:
        from termforge.borders.scrollbar import render_scrollbar
        scrollbar_style = spec.scrollbar_style if spec.scrollbar_style else "border"
        scrollbar_lines = render_scrollbar(
            viewport_h=inner_h,
            content_h=len(content_lines),
            scroll_y=spec.scroll_y,
            theme=theme,
            depth=depth,
            style_token=scrollbar_style,
        )

    final_lines = []
    if len(bordered) > 0:
        # Top line
        final_lines.append(f"{start_ansi}{bordered[0]}{end_ansi}")
        
        # Body lines (each has side borders)
        for line_idx, line in enumerate(bordered[1:-1]):
            if len(line) >= 2:
                left_border = line[0]
                right_border = line[-1]
                content = line[1:-1]
                
                if scrollbar_lines is not None and line_idx < len(scrollbar_lines):
                    # Replace right border character with styled scrollbar character
                    r_border_styled = scrollbar_lines[line_idx]
                    final_lines.append(f"{start_ansi}{left_border}{end_ansi}{content}{r_border_styled}")
                else:
                    final_lines.append(f"{start_ansi}{left_border}{end_ansi}{content}{start_ansi}{right_border}{end_ansi}")
            else:
                final_lines.append(line)
                
        # Bottom line
        if len(bordered) > 1:
            final_lines.append(f"{start_ansi}{bordered[-1]}{end_ansi}")

        
    if spec.shadow:
        shadow_style = StyleSpec(fg=ColorValue(80, 80, 80), dim=True)
        s_shad, e_shad = style_to_ansi(shadow_style, theme, depth)
        shadow_block = "█"
        
        shadowed_result = []
        # Row 0 has no side shadow, pad with 2 spaces
        shadowed_result.append(final_lines[0] + "  ")
        
        # Rows 1 to height-1 get 2 columns side shadow
        for line in final_lines[1:]:
            shadowed_result.append(line + f"{s_shad}{shadow_block * 2}{e_shad}")
            
        # Row height gets bottom shadow shifted by 2 columns
        bottom_row = "  " + f"{s_shad}{shadow_block * width}{e_shad}"
        shadowed_result.append(bottom_row)
        
        final_lines = shadowed_result

    # 5. Apply outer margin: blank rows top/bottom, blank cols left/right
    if margin > 0:
        blank_row = " " * (width + 2 * margin)
        margin_col = " " * margin
        margined: list[str] = []
        for _ in range(margin):
            margined.append(blank_row)
        for line in final_lines:
            margined.append(margin_col + line + margin_col)
        for _ in range(margin):
            margined.append(blank_row)
        final_lines = margined

    return final_lines

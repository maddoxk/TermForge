"""TermForge card component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.borders.types import BorderStyle
from termforge.borders.glyphs import resolve_border_glyphs
from termforge.borders.render import strip_ansi
from termforge.card.types import CardSpec


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


def render_card(
    spec: CardSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the Card component to layout lines.

    Args:
        spec: CardSpec containing headers and body content.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0:
        return []

    # 1. Fetch border glyphs
    style_enum = BorderStyle(spec.border_style)
    glyphs = resolve_border_glyphs(style_enum, theme)
    
    border_token = spec.border_style_token or "border"
    s_tl = _style_part(glyphs.tl, border_token, theme, depth)
    s_tr = _style_part(glyphs.tr, border_token, theme, depth)
    s_bl = _style_part(glyphs.bl, border_token, theme, depth)
    s_br = _style_part(glyphs.br, border_token, theme, depth)
    s_h = _style_part(glyphs.h, border_token, theme, depth)
    s_v = _style_part(glyphs.v, border_token, theme, depth)


    inner_w = max_size.width - 2
    inner_h = max_size.height - 2

    # 2. Form top header line
    if spec.title:
        # Format label text
        if spec.subtitle:
            raw_title = f" {spec.title} "
            raw_sub = f"({spec.subtitle}) "
            styled_title = _style_part(raw_title, spec.title_style, theme, depth)
            styled_sub = _style_part(raw_sub, spec.subtitle_style, theme, depth)
            styled_lbl = f"{styled_title}{styled_sub}"
            lbl_len = len(raw_title) + len(raw_sub)
        else:
            raw_title = f" {spec.title} "
            styled_lbl = _style_part(raw_title, spec.title_style, theme, depth)
            lbl_len = len(raw_title)

        # Truncate if title overflows inner width
        if lbl_len > inner_w - 2:
            styled_lbl = _style_part(spec.title[:inner_w - 4] + "..", spec.title_style, theme, depth)
            lbl_len = len(spec.title[:inner_w - 4]) + 2

        left_h_len = 1
        right_h_len = inner_w - left_h_len - lbl_len
        if right_h_len < 0:
            right_h_len = 0
            
        line0 = f"{s_tl}{s_h * left_h_len}{styled_lbl}{s_h * right_h_len}{s_tr}"
    else:
        line0 = f"{s_tl}{s_h * inner_w}{s_tr}"

    lines = [line0]

    # 3. Form body lines
    content_lines = spec.content.split("\n") if spec.content else []
    for r in range(inner_h):
        if r < len(content_lines):
            raw_line = content_lines[r]
            vis_len = len(strip_ansi(raw_line))
            # Truncate or pad based on visible character length
            if vis_len > inner_w:
                # If unstyled line is too long
                raw_line = raw_line[:inner_w]
                vis_len = inner_w
            pad_needed = max(0, inner_w - vis_len)
            padded_line = raw_line + (" " * pad_needed)
            styled_line = _style_part(padded_line, spec.content_style, theme, depth)
            lines.append(f"{s_v}{styled_line}{s_v}")
        else:
            # Empty filler
            styled_line = _style_part(" " * inner_w, spec.content_style, theme, depth)
            lines.append(f"{s_v}{styled_line}{s_v}")

    # 4. Form bottom line
    line_last = f"{s_bl}{s_h * inner_w}{s_br}"
    lines.append(line_last)

    return lines[:max_size.height]

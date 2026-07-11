"""TermForge status bar component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.statusbar.types import StatusBarSpec, StatusSectionSpec


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


def _render_group(
    sections: list[StatusSectionSpec],
    separator: str,
    theme: ThemeTokens | None,
    depth: ColorDepth,
    separator_style: str | None = None,
) -> tuple[str, str]:
    if not sections:
        return "", ""

    raw_items = [s.text for s in sections]
    styled_items = [_style_part(s.text, s.style, theme, depth) for s in sections]
    styled_delim = _style_part(separator, separator_style, theme, depth)

    raw_text = separator.join(raw_items)
    styled_text = styled_delim.join(styled_items)
    return raw_text, styled_text


def render_status_bar(
    spec: StatusBarSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the StatusBar component to formatted, styled lines.

    Args:
        spec: StatusBarSpec containing left/center/right section lists.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens for style resolution.
        depth: Color depth tier to simulate.

    Returns:
        List of rendered lines (typically length 1).
    """
    if max_size.height <= 0 or max_size.width <= 0:
        return []

    # 1. Render each group
    raw_l, styled_l = _render_group(spec.left, spec.separator, theme, depth, spec.separator_style)
    raw_c, styled_c = _render_group(spec.center, spec.separator, theme, depth, spec.separator_style)
    raw_r, styled_r = _render_group(spec.right, spec.separator, theme, depth, spec.separator_style)

    l_len = len(raw_l)
    c_len = len(raw_c)
    r_len = len(raw_r)

    # 2. Alignment coordinates math
    if l_len + c_len + r_len <= max_size.width:
        # Fits completely
        pos_l = 0
        pos_c = (max_size.width - c_len) // 2
        
        # Ensure center starts after left ends
        if pos_c < l_len:
            pos_c = l_len
            
        pos_r = max_size.width - r_len
        # Ensure right starts after center ends
        if pos_r < pos_c + c_len:
            pos_r = pos_c + c_len

        space1 = " " * (pos_c - l_len)
        space2 = " " * (pos_r - (pos_c + c_len))
        
        line = f"{styled_l}{space1}{styled_c}{space2}{styled_r}"
    else:
        # Overlaps: omit center group
        if l_len + r_len <= max_size.width:
            space = " " * (max_size.width - l_len - r_len)
            line = f"{styled_l}{space}{styled_r}"
        else:
            # Even left and right combined overflows: truncate right
            avail_r = max_size.width - l_len
            if avail_r > 1:
                # Truncate right group
                # For simplicity, slice the raw right text and apply a single styling block (or intermediate style)
                trunc_r_raw = raw_r[:avail_r - 1] + "…"
                style_token = spec.right[-1].style if spec.right else None
                styled_r_trunc = _style_part(trunc_r_raw, style_token, theme, depth)
                line = f"{styled_l}{styled_r_trunc}"
            else:
                # Avail for right is <= 1: omit right, truncate left
                trunc_l_raw = raw_l[:max_size.width - 1] + "…"
                style_token = spec.left[0].style if spec.left else None
                styled_l_trunc = _style_part(trunc_l_raw, style_token, theme, depth)
                line = styled_l_trunc

    # 3. Padding alignment backup
    from termforge.borders import strip_ansi
    raw_w = len(strip_ansi(line))
    if raw_w < max_size.width:
        line += " " * (max_size.width - raw_w)

    lines = [line]
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

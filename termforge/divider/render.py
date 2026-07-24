"""TermForge divider component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.divider.types import DividerSpec


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


def render_divider(
    spec: DividerSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the Divider component to layout lines.

    Args:
        spec: DividerSpec containing label, alignment, and line_char.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0:
        return []

    w = max_size.width
    char = spec.line_char if spec.line_char else "─"

    if not spec.label:
        line_raw = char * w
        line = _style_part(line_raw, spec.line_style, theme, depth)
    else:
        label_raw = f" {spec.label} "
        label_len = len(label_raw)
        
        if label_len >= w:
            # Label fills/exceeds width
            label_styled = _style_part(spec.label[:w], spec.label_style, theme, depth)
            line = label_styled
        else:
            remaining = w - label_len
            if spec.alignment == "left":
                left_len = 2 if remaining >= 2 else remaining
                right_len = remaining - left_len
            elif spec.alignment == "right":
                right_len = 2 if remaining >= 2 else remaining
                left_len = remaining - right_len
            else:  # center
                left_len = remaining // 2
                right_len = remaining - left_len

            s_left = _style_part(char * left_len, spec.line_style, theme, depth)
            s_label = _style_part(label_raw, spec.label_style, theme, depth)
            s_right = _style_part(char * right_len, spec.line_style, theme, depth)
            line = f"{s_left}{s_label}{s_right}"

    lines = [line]
    while len(lines) < max_size.height:
        lines.append(" " * w)

    return lines[:max_size.height]

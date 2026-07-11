"""TermForge spinner box component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.spinnerbox.types import SpinnerBoxSpec


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


def render_spinner_box(
    spec: SpinnerBoxSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the SpinnerBox component to layout lines.

    Args:
        spec: SpinnerBoxSpec containing value settings and customized carets.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0:
        return []

    # Calculate padding size for value field
    if spec.min_val is not None and spec.max_val is not None:
        max_val_len = max(len(str(spec.min_val)), len(str(spec.max_val)))
    else:
        max_val_len = 3

    padded_val = str(spec.value).center(max_val_len)
    
    # 1. Build spinner block segments
    styled_left = _style_part(spec.left_caret, spec.caret_style, theme, depth)
    styled_right = _style_part(spec.right_caret, spec.caret_style, theme, depth)
    styled_val = _style_part(padded_val, spec.value_style, theme, depth)

    # Spinner widget block raw length: len(left) + 2 + max_val_len + 2 + len(right)
    spinner_len = len(spec.left_caret) + 2 + max_val_len + 2 + len(spec.right_caret)
    lbl_len = len(spec.label)

    styled_label = _style_part(spec.label, spec.label_style, theme, depth)

    # 2. Form horizontal layout
    if lbl_len > 0:
        # Determine separating spaces
        avail_space = max_size.width - lbl_len - spinner_len
        if avail_space >= 2:
            sep = " " * avail_space
        else:
            sep = "  "
            
        line = f"{styled_label}{sep}{styled_left}  {styled_val}  {styled_right}"
        raw_len = lbl_len + len(sep) + spinner_len
    else:
        line = f"{styled_left}  {styled_val}  {styled_right}"
        raw_len = spinner_len

    if raw_len < max_size.width:
        line += " " * (max_size.width - raw_len)

    lines = [line]
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

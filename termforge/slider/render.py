"""TermForge slider component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.slider.types import SliderSpec


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


def render_slider(
    spec: SliderSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the Slider component to layout lines.

    Args:
        spec: SliderSpec containing progress metrics and custom indicators.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0:
        return []

    # 1. Format numeric value string
    val_disp = int(spec.value) if spec.value.is_integer() else spec.value
    formatted_val = spec.value_format.replace("{val}", str(val_disp))

    lbl_len = len(spec.label)
    val_len = len(formatted_val)

    # 2. Layout space math
    # Formula: {label} + {separator} + "[" + {track} + "]" + " " + {value}
    # separator = 2 spaces if label exists, else 0
    # brackets = 2
    # space before value = 1
    # total non-track chars = lbl_len + sep_len + 2 + 1 + val_len
    sep_len = 2 if lbl_len > 0 else 0
    fixed_len = lbl_len + sep_len + 2 + 1 + val_len

    track_w = max_size.width - fixed_len
    if track_w < 5:
        track_w = 5 # Force minimum size to prevent crashes

    # 3. Calculate handle offset inside track
    denom = spec.max_val - spec.min_val
    if denom > 0:
        ratio = (spec.value - spec.min_val) / denom
    else:
        ratio = 0.0
    ratio = max(0.0, min(1.0, ratio))

    pos = int(ratio * (track_w - 1))
    pos = max(0, min(track_w - 1, pos))

    # Build tracks
    left_fill = spec.track_fill_char * pos
    right_empty = spec.track_empty_char * (track_w - 1 - pos)

    styled_left = _style_part(left_fill, spec.track_fill_style, theme, depth)
    styled_handle = _style_part(spec.handle_char, spec.handle_style, theme, depth)
    styled_right = _style_part(right_empty, spec.track_empty_style, theme, depth)

    border_token = "border"
    s_l = _style_part("[", border_token, theme, depth)
    s_r = _style_part("]", border_token, theme, depth)
    styled_track = f"{s_l}{styled_left}{styled_handle}{styled_right}{s_r}"

    # Combine parts
    styled_lbl = _style_part(spec.label, spec.label_style, theme, depth)
    styled_val = _style_part(formatted_val, spec.value_style, theme, depth)

    if lbl_len > 0:
        line = f"{styled_lbl}{' ' * sep_len}{styled_track} {styled_val}"
    else:
        line = f"{styled_track} {styled_val}"

    # Calculate actual raw text length
    actual_len = lbl_len + sep_len + 2 + track_w + 1 + val_len
    if actual_len < max_size.width:
        line += " " * (max_size.width - actual_len)

    lines = [line]
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

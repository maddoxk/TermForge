"""TermForge stepper component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.stepper.types import StepperSpec


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


def render_stepper(
    spec: StepperSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the Stepper component to layout lines.

    Args:
        spec: StepperSpec containing list of step titles.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if not spec.steps or max_size.height <= 0 or max_size.width <= 0:
        return []

    # 1. Build styled segments
    styled_segments = []
    raw_lens = []
    
    for idx, title in enumerate(spec.steps):
        is_active = (idx == spec.active_idx)
        if is_active:
            raw_text = f"[{title}]"
            styled_text = _style_part(raw_text, spec.active_style, theme, depth)
        else:
            raw_text = title
            styled_text = _style_part(raw_text, spec.inactive_style, theme, depth)
            
        styled_segments.append(styled_text)
        raw_lens.append(len(raw_text))

    # 2. Join segments using connectors
    styled_conn = _style_part(spec.connector, spec.connector_style, theme, depth)
    line = styled_conn.join(styled_segments)

    # 3. Calculate raw length and pad spacing
    total_raw_len = sum(raw_lens) + len(spec.connector) * (len(spec.steps) - 1)
    if total_raw_len < max_size.width:
        line += " " * (max_size.width - total_raw_len)

    lines = [line]
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

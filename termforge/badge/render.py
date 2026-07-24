"""TermForge badge component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.badge.types import BadgeSpec


DEFAULT_SEVERITY_STYLES = {
    "info": "colors.info",
    "success": "colors.success",
    "warning": "colors.warning",
    "error": "colors.danger",
}


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


def render_badge(
    spec: BadgeSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the Badge component to layout lines.

    Args:
        spec: BadgeSpec containing text, severity, and brackets.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0:
        return []

    # Parse open and close brackets
    if len(spec.brackets) >= 2:
        parts = spec.brackets.split()
        if len(parts) == 2:
            open_b, close_b = parts[0], parts[1]
        else:
            open_b, close_b = spec.brackets[0], spec.brackets[-1]
    elif len(spec.brackets) == 1:
        open_b = close_b = spec.brackets
    else:
        open_b, close_b = "[", "]"

    raw_text = f"{open_b} {spec.text} {close_b}" if spec.text else f"{open_b}{close_b}"
    raw_len = len(raw_text)

    # Determine style token
    style_token = spec.text_style
    if not style_token:
        if spec.severity_styles and spec.severity in spec.severity_styles:
            style_token = spec.severity_styles[spec.severity]
        else:
            style_token = DEFAULT_SEVERITY_STYLES.get(spec.severity, "colors.primary")

    line = _style_part(raw_text, style_token, theme, depth)
    if raw_len < max_size.width:
        line += " " * (max_size.width - raw_len)

    lines = [line]
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

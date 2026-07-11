"""TermForge log streamer renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.logging.types import LogStreamerSpec


def _style_level(level: str, token: str | None, theme: ThemeTokens | None, depth: ColorDepth) -> str:
    text = f"[{level}]"
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


def render_log_streamer(
    spec: LogStreamerSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the log streamer component to a list of lines.

    Args:
        spec: LogStreamerSpec containing buffers and format configs.
        max_size: Size constraints for the rendered viewport.
        theme: Optional theme tokens for style resolution.
        depth: Color depth tier to use.

    Returns:
        List of formatted log lines.
    """
    if not spec.buffer:
        return []

    lines: list[str] = []

    for entry in spec.buffer:
        ts = entry.get("timestamp", "")
        level = entry.get("level", "")
        msg = entry.get("message", "")

        ts_part = f"[{ts}] " if ts else ""
        level_part = f"[{level}]"
        
        prefix_len = len(ts_part) + len(level_part) + 1  # prefix plus separating space

        # Truncate message if it exceeds width boundaries
        raw_len = prefix_len + len(msg)
        disp_msg = msg
        if raw_len > max_size.width:
            allowed_msg_w = max_size.width - prefix_len
            if allowed_msg_w > 1:
                disp_msg = msg[:allowed_msg_w - 1] + "…"
            else:
                # If prefix itself exceeds or takes all space, slice overall raw
                raw_full = f"{ts_part}{level_part} {msg}"
                disp_msg = ""
                ts_part = ""
                level_part = raw_full[:max(0, max_size.width - 1)] + "…"

        # Apply styling to level if token is mapped
        style_token = spec.level_colors.get(level)
        styled_level = _style_level(level, style_token, theme, depth) if level_part else ""

        if level_part:
            line = f"{ts_part}{styled_level} {disp_msg}" if ts_part else f"{styled_level} {disp_msg}"
        else:
            line = level_part  # was truncated fully

        lines.append(line)

    # Apply auto scroll or static viewport slicing
    if spec.auto_scroll:
        # Take the most recent items (at the end of the buffer)
        return lines[-max_size.height:] if len(lines) > max_size.height else lines
    else:
        return lines[:max_size.height]

"""TermForge scrollbar component — visual vertical scroll indicators."""
from __future__ import annotations

from termforge.core.types import ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi


def render_scrollbar(
    viewport_h: int,
    content_h: int,
    scroll_y: int,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
    style_token: str | None = None,
    track_char: str = "░",
    thumb_char: str = "█",
) -> list[str]:
    """Compute and render a vertical scrollbar track.

    Args:
        viewport_h: Height of the scrolling viewport window.
        content_h: Total height of all content items.
        scroll_y: Current vertical scroll offset (0-indexed).
        theme: Optional theme tokens for styling.
        depth: Color depth tier to use.
        style_token: Style token name for the scrollbar.
        track_char: Character for the scrollbar track (default ░).
        thumb_char: Character for the scrollbar thumb (default █).

    Returns:
        List of strings of length `viewport_h` representing the scrollbar.
    """
    if viewport_h <= 0:
        return []

    # 1. Base track setup
    track = [track_char] * viewport_h

    # 2. Compute thumb position and size if content overflows
    if content_h > viewport_h:
        thumb_len = max(1, int((viewport_h / content_h) * viewport_h))
        max_scroll = content_h - viewport_h
        if max_scroll > 0:
            ratio = max(0.0, min(1.0, scroll_y / max_scroll))
            rem_track = viewport_h - thumb_len
            thumb_start = int(ratio * rem_track)
        else:
            thumb_start = 0

        # Clamp bounds
        thumb_start = max(0, min(thumb_start, viewport_h - thumb_len))

        # Fill thumb region
        for i in range(thumb_start, thumb_start + thumb_len):
            if i < len(track):
                track[i] = thumb_char
    else:
        # Content completely fits, draw full thumb or full track depending on preference.
        # Let's fill the entire track with the thumb character.
        track = [thumb_char] * viewport_h

    # 3. Apply style if token is provided
    start_ansi, end_ansi = "", ""
    if theme and style_token and depth != ColorDepth.MONOCHROME:
        token_path = style_token if style_token.startswith("colors.") else f"colors.{style_token}"
        try:
            res = resolve_token(theme, token_path)
            if isinstance(res, ColorValue):
                style = StyleSpec(fg=ColorValue(res.r, res.g, res.b, name=None))
                start_ansi, end_ansi = style_to_ansi(style, theme, depth)
        except KeyError:
            pass

    if start_ansi:
        return [f"{start_ansi}{c}{end_ansi}" for c in track]
    return track

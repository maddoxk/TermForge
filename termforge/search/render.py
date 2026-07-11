"""TermForge search input and filter bar component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.borders import strip_ansi
from termforge.search.types import SearchBarSpec


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


def highlight_matches(
    text: str,
    query: str,
    match_style: str | None,
    theme: ThemeTokens | None,
    depth: ColorDepth,
) -> str:
    """Highlight all case-insensitive occurrences of query inside text.

    Args:
        text: Candidate text string.
        query: Substring query string to highlight.
        match_style: Style token for highlights.
        theme: Theme tokens.
        depth: Color depth tier.

    Returns:
        Formatted candidate text string.
    """
    if not query or depth == ColorDepth.MONOCHROME:
        return text

    q_len = len(query)
    q_lower = query.lower()
    text_lower = text.lower()

    parts = []
    start = 0
    idx = text_lower.find(q_lower, start)

    while idx != -1:
        # Add preceding segment
        parts.append(text[start:idx])
        # Add styled match segment
        match_str = text[idx:idx + q_len]
        styled_match = _style_part(match_str, match_style, theme, depth)
        parts.append(styled_match)
        start = idx + q_len
        idx = text_lower.find(q_lower, start)

    # Add remainder
    parts.append(text[start:])
    return "".join(parts)


def render_search_bar(
    spec: SearchBarSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the SearchBar component to layout lines.

    Args:
        spec: SearchBarSpec containing query and candidates.
        max_size: Size constraints of the canvas.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0:
        return []

    # 1. Renders Line 0: input query line
    prefix = "🔍 Search: "
    if not spec.query:
        styled_input = _style_part(spec.placeholder, spec.placeholder_style, theme, depth)
        raw_len = len(prefix) + len(spec.placeholder)
    else:
        styled_input = _style_part(spec.query, spec.input_style, theme, depth)
        raw_len = len(prefix) + len(spec.query)

    input_line = f"{prefix}{styled_input}"
    if raw_len < max_size.width:
        input_line += " " * (max_size.width - raw_len)
    
    lines = [input_line]

    # 2. Renders matching candidates
    q_lower = spec.query.lower()
    for candidate in spec.candidates:
        if q_lower in candidate.lower():
            # Apply matching highlights
            styled_cand = highlight_matches(candidate, spec.query, spec.match_style, theme, depth)
            
            # Pad line to full width
            cand_raw_w = len(candidate)
            line = styled_cand
            if cand_raw_w < max_size.width:
                line += " " * (max_size.width - cand_raw_w)
            
            lines.append(line)

    # 3. Fill remaining lines to match requested height
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

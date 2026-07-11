"""TermForge breadcrumbs navigation trail renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.navigation.types import BreadcrumbsSpec


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


def _collapse_breadcrumbs(items: list[str], delimiter: str, max_w: int) -> list[str]:
    if not items:
        return []

    delim_w = len(delimiter)
    
    def get_len(lst: list[str]) -> int:
        if not lst:
            return 0
        return sum(len(x) for x in lst) + delim_w * (len(lst) - 1)

    # 1. Fits completely
    if get_len(items) <= max_w:
        return list(items)

    # 2. Collapse middle items to "..."
    if len(items) > 2:
        collapsed = [items[0], "...", items[-1]]
        if get_len(collapsed) <= max_w:
            return collapsed

    # 3. Collapse to tail only with "..."
    if len(items) >= 2:
        collapsed = ["...", items[-1]]
        if get_len(collapsed) <= max_w:
            return collapsed

    # 4. Collapse to just active item
    collapsed = [items[-1]]
    if get_len(collapsed) <= max_w:
        return collapsed

    # 5. Active item is too long: truncate active item itself
    active_item = items[-1]
    if len(active_item) > max_w:
        return [active_item[:max(0, max_w - 1)] + "…"]
    return [active_item]


def render_breadcrumbs(
    spec: BreadcrumbsSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the breadcrumbs component to styled trail lines.

    Args:
        spec: BreadcrumbsSpec defining items, delimiter and styles.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens for style resolution.
        depth: Color depth tier to use.

    Returns:
        List of rendered lines (containing 1 line).
    """
    if not spec.items or max_size.height <= 0 or max_size.width <= 0:
        return []

    # 1. Compute collapsed breadcrumbs items
    collapsed_items = _collapse_breadcrumbs(spec.items, spec.delimiter, max_size.width)

    # 2. Style individual items
    styled_items = []
    num_items = len(collapsed_items)
    
    for idx, item in enumerate(collapsed_items):
        is_active = (idx == num_items - 1)
        
        # Style resolution
        if is_active:
            style_token = spec.active_item_style
        else:
            style_token = spec.item_style
            
        styled_item = _style_part(item, style_token, theme, depth)
        styled_items.append(styled_item)

    # 3. Style delimiter
    styled_delim = _style_part(spec.delimiter, spec.delimiter_style, theme, depth)

    # 4. Join and return single line
    line = styled_delim.join(styled_items)
    return [line]

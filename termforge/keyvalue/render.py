"""TermForge key-value grid renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.borders.render import strip_ansi
from termforge.keyvalue.types import KeyValueGridSpec


def render_keyvalue_grid(
    spec: KeyValueGridSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render a aligned key-value grid to a list of lines.

    Args:
        spec: KeyValueGridSpec defining the items and formatting.
        max_size: Size constraints for the rendered output.
        theme: Optional theme tokens for styling.
        depth: Color depth tier to use.

    Returns:
        List of formatted and optionally ANSI-styled line strings.
    """
    if not spec.items:
        return []

    # 1. Determine key column width
    if spec.key_width is not None:
        key_col_w = spec.key_width
    else:
        key_col_w = max(len(item.key) for item in spec.items) if spec.items else 0

    lines: list[str] = []

    # 2. Render each item row
    for item in spec.items:
        # Pad key to column width
        padded_key = f"{item.key:<{key_col_w}}"

        vis_val_len = len(strip_ansi(item.value))
        raw_line_len = len(padded_key) + len(spec.separator) + vis_val_len
        
        # Determine if we need to truncate
        val_str = item.value
        if raw_line_len > max_size.width:
            allowed_val_w = max_size.width - len(padded_key) - len(spec.separator)
            if allowed_val_w > 1:
                val_str = val_str[:allowed_val_w - 1] + "…"
            else:
                val_str = "…"[:max(0, allowed_val_w)]

        # Apply styling if theme and depth are provided
        styled_key = padded_key
        styled_val = val_str

        if theme and depth != ColorDepth.MONOCHROME:
            # Render Key Style
            if item.key_style:
                token_path = item.key_style
                if not token_path.startswith("colors."):
                    token_path = f"colors.{token_path}"
                try:
                    res_val = resolve_token(theme, token_path)
                    if isinstance(res_val, ColorValue):
                        style = StyleSpec(fg=res_val)
                        start, end = style_to_ansi(style, theme, depth)
                        styled_key = f"{start}{padded_key}{end}"
                except KeyError:
                    pass

            # Render Value Style
            if item.value_style:
                token_path = item.value_style
                if not token_path.startswith("colors."):
                    token_path = f"colors.{token_path}"
                try:
                    res_val = resolve_token(theme, token_path)
                    if isinstance(res_val, ColorValue):
                        style = StyleSpec(fg=res_val)
                        start, end = style_to_ansi(style, theme, depth)
                        styled_val = f"{start}{val_str}{end}"
                except KeyError:
                    pass

        line = f"{styled_key}{spec.separator}{styled_val}"
        lines.append(line)

    return lines[:max_size.height]

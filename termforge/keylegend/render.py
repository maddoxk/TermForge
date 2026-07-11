"""TermForge keybinding shortcut legend renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.keylegend.types import KeyLegendSpec


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


def _truncate_legend_item(
    key: str,
    action: str,
    format_template: str,
    avail_width: int,
) -> tuple[str, str]:
    static_len = len(format_template.replace("{key}", "").replace("{description}", ""))
    max_len = avail_width - static_len

    if max_len <= 0:
        return "…", ""

    if max_len > len(key):
        # Keep key intact, truncate description
        desc_avail = max_len - len(key)
        if len(action) > desc_avail:
            trunc_desc = action[:max(0, desc_avail - 1)] + "…"
        else:
            trunc_desc = action
        return key, trunc_desc
    else:
        # Key exceeds space, clear description and truncate key
        if len(key) > max_len:
            trunc_key = key[:max(0, max_len - 1)] + "…"
        else:
            trunc_key = key
        return trunc_key, ""


def render_key_legend(
    spec: KeyLegendSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the key legend component to formatted and styled strings.

    Args:
        spec: KeyLegendSpec defining bindings, orientation, and styling.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens for style resolution.
        depth: Color depth tier to simulate.

    Returns:
        List of rendered lines.
    """
    if not spec.bindings:
        return []

    # 1. Horizontal rendering layout
    if spec.orientation == "horizontal":
        raw_items = []
        for b in spec.bindings:
            raw_items.append(spec.format.format(key=b.key, description=b.action))

        sep = " " * spec.spacing
        current_len = 0
        styled_parts = []

        for i, b in enumerate(spec.bindings):
            raw_item = raw_items[i]
            prefix_len = len(sep) if i > 0 else 0
            
            if current_len + prefix_len + len(raw_item) > max_size.width:
                # Truncate this item to fit remainder
                avail = max_size.width - current_len - prefix_len
                if avail > 0:
                    trunc_key, trunc_desc = _truncate_legend_item(b.key, b.action, spec.format, avail)
                    sk = _style_part(trunc_key, spec.key_style, theme, depth)
                    sd = _style_part(trunc_desc, spec.desc_style, theme, depth)
                    styled_rendered = spec.format.format(key=sk, description=sd)
                    
                    if i > 0:
                        styled_parts.append(sep)
                    styled_parts.append(styled_rendered)
                break

            # Fully fit item
            sk = _style_part(b.key, spec.key_style, theme, depth)
            sd = _style_part(b.action, spec.desc_style, theme, depth)
            styled_item = spec.format.format(key=sk, description=sd)

            if i > 0:
                styled_parts.append(sep)
            styled_parts.append(styled_item)
            current_len += prefix_len + len(raw_item)

        line = "".join(styled_parts)
        return [line] if max_size.height > 0 else []

    # 2. Vertical rendering layout
    else:
        lines = []
        for b in spec.bindings:
            raw_item = spec.format.format(key=b.key, description=b.action)
            
            if len(raw_item) > max_size.width:
                trunc_key, trunc_desc = _truncate_legend_item(b.key, b.action, spec.format, max_size.width)
                sk = _style_part(trunc_key, spec.key_style, theme, depth)
                sd = _style_part(trunc_desc, spec.desc_style, theme, depth)
                line = spec.format.format(key=sk, description=sd)
            else:
                sk = _style_part(b.key, spec.key_style, theme, depth)
                sd = _style_part(b.action, spec.desc_style, theme, depth)
                line = spec.format.format(key=sk, description=sd)
                
            lines.append(line)

        return lines[:max_size.height]

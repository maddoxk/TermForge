"""TermForge toggle switch component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.toggle.types import ToggleSwitchSpec


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


def render_toggle_switch(
    spec: ToggleSwitchSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the ToggleSwitch component to layout lines.

    Args:
        spec: ToggleSwitchSpec containing labels and toggle values.
        max_size: Size constraints for the rendering viewport.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0:
        return []

    # 1. Build switch block
    max_lbl_len = max(len(spec.active_label), len(spec.inactive_label))
    if spec.state:
        body = f"{spec.active_indicator} {spec.active_label.ljust(max_lbl_len)}"
        switch_style = spec.active_style
    else:
        body = f"{spec.inactive_indicator} {spec.inactive_label.ljust(max_lbl_len)}"
        switch_style = spec.inactive_style

    raw_switch = f"[{body}]"
    styled_switch = _style_part(raw_switch, switch_style, theme, depth)
    styled_label = _style_part(spec.label, spec.label_style, theme, depth)

    # 2. Form line layout
    switch_len = len(raw_switch)
    label_len = len(spec.label)

    if label_len > 0:
        # Determine separating spaces
        avail_space = max_size.width - label_len - switch_len
        if avail_space >= 2:
            sep = " " * avail_space
        else:
            sep = "  "
            
        line = f"{styled_label}{sep}{styled_switch}"
        raw_len = label_len + len(sep) + switch_len
    else:
        line = styled_switch
        raw_len = switch_len

    # Trailing pad if necessary
    if raw_len < max_size.width:
        line += " " * (max_size.width - raw_len)

    lines = [line]
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)

    return lines[:max_size.height]

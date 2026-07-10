from __future__ import annotations
from termforge.core.types import Size, StyleSpec, ColorValue, ColorDepth
from termforge.core.theme import ThemeTokens
from termforge.text.render import style_to_ansi
from termforge.progress.types import ProgressSpec
import math

def render_progress(spec: ProgressSpec, max_size: Size, theme: ThemeTokens, depth: ColorDepth = ColorDepth.TRUECOLOR) -> list[str]:
    width = spec.width if spec.width is not None else max_size.width
    if width <= 0:
        return []
    
    text = ""
    if spec.show_text:
        percent = int(max(0.0, min(1.0, spec.progress)) * 100)
        text = spec.text_format.replace("{percent}", str(percent))
        
    bar_width = width - len(text) - (1 if text else 0)
    if bar_width < 1:
        # Not enough space for bar, just text
        return [text[:width]]
        
    filled_len = int(math.floor(max(0.0, min(1.0, spec.progress)) * bar_width))
    empty_len = bar_width - filled_len
    
    # Resolve custom color configurations
    filled_role = "primary"
    empty_role = "border"
    if spec.color_config:
        filled_role = spec.color_config.get("filled", "primary")
        empty_role = spec.color_config.get("empty", "border")
        
    f_style = StyleSpec(fg=ColorValue(0, 0, 0, name=f"colors.{filled_role}"))
    e_style = StyleSpec(fg=ColorValue(0, 0, 0, name=f"colors.{empty_role}"))
    
    s_fill, e_fill = style_to_ansi(f_style, theme, depth)
    s_empty, e_empty = style_to_ansi(e_style, theme, depth)
    
    filled_str = spec.filled_char * filled_len
    if spec.head_char and empty_len > 0 and filled_len > 0:
        filled_str = filled_str[:-1] + spec.head_char
        
    empty_str = spec.empty_char * empty_len
    
    # Wrap in ANSI codes if resolved
    if s_fill:
        filled_str = f"{s_fill}{filled_str}{e_fill}"
    if s_empty:
        empty_str = f"{s_empty}{empty_str}{e_empty}"
        
    bar = filled_str + empty_str
    
    result = bar + (" " + text if text else "")
    return [result]

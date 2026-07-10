from __future__ import annotations
from termforge.core.types import Size
from termforge.core.theme import ThemeTokens
from termforge.progress.types import ProgressSpec
import math

def render_progress(spec: ProgressSpec, max_size: Size, theme: ThemeTokens) -> list[str]:
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
    
    bar = spec.filled_char * filled_len
    if spec.head_char and empty_len > 0 and filled_len > 0:
        bar = bar[:-1] + spec.head_char
    bar += spec.empty_char * empty_len
    
    result = bar + (" " + text if text else "")
    return [result]

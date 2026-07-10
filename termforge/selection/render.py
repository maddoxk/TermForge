from __future__ import annotations
from termforge.core.types import Size
from termforge.core.theme import ThemeTokens
from termforge.selection.types import SelectionListSpec

def render_selection_list(spec: SelectionListSpec, max_size: Size, theme: ThemeTokens) -> list[str]:
    lines = []
    for i, item in enumerate(spec.items):
        is_focused = (i == spec.focused_index)
        box = "[x]" if item.selected else "[ ]"
        
        pointer = "> " if is_focused else "  "
        line = f"{pointer}{box} {item.label}"
        
        if len(line) > max_size.width:
            line = line[:max_size.width - 1] + "…"
        lines.append(line)
        
    return lines[:max_size.height]

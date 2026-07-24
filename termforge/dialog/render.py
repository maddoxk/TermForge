from __future__ import annotations
from termforge.core.types import Size
from termforge.core.theme import ThemeTokens
from termforge.borders.types import BorderSpec
from termforge.borders.render import render_border
from termforge.core.types import Size, ColorDepth
from termforge.dialog.types import DialogSpec

def render_dialog(spec: DialogSpec, max_size: Size, theme: ThemeTokens | None = None, depth: ColorDepth = ColorDepth.TRUECOLOR) -> list[str]:
    # Construct inner body lines
    content = [spec.body]
    
    # Render buttons: [ OK ]  [ Cancel ]
    btn_row = ""
    for i, btn in enumerate(spec.buttons):
        is_focused = (i == spec.focused_button_index)
        btn_str = f"<{btn}>" if is_focused else f"[{btn}]"
        btn_row += btn_str + "  "
    
    content.append("")
    content.append(btn_row.strip())
    
    border_spec = BorderSpec(
        title=spec.title
    )
    
    # Dialog takes up the full width/height or fits the content
    lines = render_border(border_spec, content, width=max_size.width, theme=theme)
    
    # Pad to max_size.height
    while len(lines) < max_size.height:
        lines.append(" " * max_size.width)
        
    return lines[:max_size.height]

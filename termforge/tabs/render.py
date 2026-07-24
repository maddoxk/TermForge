from __future__ import annotations
from termforge.core.types import Size
from termforge.core.theme import ThemeTokens
from termforge.tabs.types import TabSpec
from termforge.core.types import Size, ColorDepth

def render_tabs(spec: TabSpec, max_size: Size, theme: ThemeTokens | None = None, depth: ColorDepth = ColorDepth.TRUECOLOR) -> list[str]:
    # Render tab headers as:
    # ┌──────┐ ┌──────┐
    # │ Tab1 │ │*Tab2*│
    # └──────┴─┴──────┴───────...
    if not spec.titles:
        return [""] * max_size.height

    if max_size.height == 1:
        tab_strs = []
        for i, title in enumerate(spec.titles):
            if i == spec.active_index:
                tab_strs.append(f"[{title}]")
            else:
                tab_strs.append(f" {title} ")
        line = "  ".join(tab_strs)
        if len(line) > max_size.width:
            line = line[:max_size.width - 1] + "…"
        else:
            line = line + " " * (max_size.width - len(line))
        return [line]

    top = ""
    mid = ""
    bot = ""

    for i, title in enumerate(spec.titles):
        is_active = (i == spec.active_index)
        display = f"*{title}*" if is_active else f" {title} "
        w = len(display)

        if is_active:
            top += "┌" + "─" * w + "┐ "
            mid += "│" + display + "│ "
            bot += "└" + "─" * w + "┘ "
        else:
            top += "┌" + "─" * w + "┐ "
            mid += "│" + display + "│ "
            bot += "└" + "─" * w + "┘ "

    lines = [top, mid, bot]
    # pad/truncate width
    result = []
    for line in lines:
        if len(line) > max_size.width:
            line = line[:max_size.width - 1] + "…"
        else:
            line = line + " " * (max_size.width - len(line))
        result.append(line)

    while len(result) < max_size.height:
        result.append(" " * max_size.width)

    return result[:max_size.height]

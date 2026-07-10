from __future__ import annotations
from termforge.core.types import LayoutResult, Size, StyleSpec
from termforge.core.theme import ThemeTokens
from termforge.tables.types import TableSpec, ColumnSpec
from termforge.text.types import TextSpec, TextAlign
from termforge.text.render import render_text

def render_table(spec: TableSpec, max_size: Size, theme: ThemeTokens) -> list[str]:
    # 1. Calculate column widths
    col_widths = []
    for i, col in enumerate(spec.columns):
        if col.width is not None:
            col_widths.append(col.width)
        else:
            # find max width of data or title
            w = len(col.title)
            for row in spec.rows:
                if i < len(row):
                    w = max(w, len(str(row[i])))
            col_widths.append(w)
            
    # 2. Render header
    lines = []
    header_parts = []
    for col, width in zip(spec.columns, col_widths):
        ts = TextSpec(content=col.title, align=col.align, max_width=width)
        res = render_text(ts, theme=theme, available_width=width)
        content = res[0] if res else " " * width
        header_parts.append(content)
        
    header_line = " │ ".join(header_parts)
    lines.append(header_line)
    lines.append("─┼─".join("─" * w for w in col_widths))
    
    # 3. Render rows
    for r_idx, row in enumerate(spec.rows):
        row_parts = []
        for i, (col, width) in enumerate(zip(spec.columns, col_widths)):
            text = str(row[i]) if i < len(row) else ""
            ts = TextSpec(content=text, align=col.align, max_width=width)
            res = render_text(ts, theme=theme, available_width=width)
            content = res[0] if res else " " * width
            row_parts.append(content)
        lines.append(" │ ".join(row_parts))
        
    return lines

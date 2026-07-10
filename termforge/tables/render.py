from __future__ import annotations
from termforge.core.types import LayoutResult, Size, StyleSpec
from termforge.core.theme import ThemeTokens
from termforge.tables.types import TableSpec, ColumnSpec
from termforge.text.types import TextSpec, TextAlign
from termforge.text.render import render_text

def render_table(spec: TableSpec, max_size: Size, theme: ThemeTokens) -> list[str]:
    # 1. Calculate column widths and inner content widths
    col_widths = []
    col_inner_widths = []
    for i, col in enumerate(spec.columns):
        if col.width is not None:
            inner_w = col.width
        else:
            w = len(col.title)
            for row in spec.rows:
                if i < len(row):
                    w = max(w, len(str(row[i])))
            inner_w = w
        col_inner_widths.append(inner_w)
        col_widths.append(inner_w + col.padding_left + col.padding_right)
            
    # 2. Render header
    lines = []
    header_parts = []
    for col, width, inner_w in zip(spec.columns, col_widths, col_inner_widths):
        ts = TextSpec(content=col.title, align=col.align, max_width=inner_w)
        res = render_text(ts, theme=theme, available_width=inner_w)
        content = res[0] if res else " " * inner_w
        padded_content = " " * col.padding_left + content + " " * col.padding_right
        header_parts.append(padded_content)
        
    header_line = " │ ".join(header_parts)
    lines.append(header_line)
    lines.append("─┼─".join("─" * w for w in col_widths))
    
    # 3. Render rows
    for r_idx, row in enumerate(spec.rows):
        row_parts = []
        for i, (col, width, inner_w) in enumerate(zip(spec.columns, col_widths, col_inner_widths)):
            text = str(row[i]) if i < len(row) else ""
            ts = TextSpec(content=text, align=col.align, max_width=inner_w)
            res = render_text(ts, theme=theme, available_width=inner_w)
            content = res[0] if res else " " * inner_w
            padded_content = " " * col.padding_left + content + " " * col.padding_right
            row_parts.append(padded_content)
        lines.append(" │ ".join(row_parts))
        
    return lines

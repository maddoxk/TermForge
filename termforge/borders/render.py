from __future__ import annotations
import re
from termforge.borders.types import BorderSpec, BorderStyle
from termforge.borders.glyphs import resolve_border_glyphs
from termforge.text.wrap import get_string_width
from termforge.text.types import TextAlign
from termforge.core.theme import ThemeTokens

def strip_ansi(text: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def render_border(
    spec: BorderSpec,
    content_lines: list[str],
    width: int | None = None,
    theme: ThemeTokens | None = None,
    unicode_supported: bool = True
) -> list[str]:
    glyphs = resolve_border_glyphs(spec.style, theme, unicode_supported)
    
    # 1. Determine inner width
    left_w = 1 if spec.left.visible else 0
    right_w = 1 if spec.right.visible else 0
    top_h = 1 if spec.top.visible else 0
    bottom_h = 1 if spec.bottom.visible else 0
    
    if width is not None:
        inner_w = max(0, width - left_w - right_w)
    else:
        inner_w = max(get_string_width(strip_ansi(line)) for line in content_lines) if content_lines else 0
        width = inner_w + left_w + right_w
        
    lines = []
    
    # 2. Render Top Border
    if spec.top.visible:
        top_line = ""
        if spec.left.visible:
            top_line += glyphs.tl
        
        # Determine top center content (title and tags)
        title_text = f" {spec.title} " if spec.title else ""
        title_w = get_string_width(title_text)
        
        tags_text = ""
        if spec.tags:
            tags_str = " ".join(f"[{t}]" for t in spec.tags)
            tags_text = f" {tags_str} "
        tags_w = get_string_width(tags_text)
        
        if title_w > 0 and tags_w > 0 and (title_w + tags_w + 2) <= inner_w:
            # Render both title (left) and tags (right)
            filler_w = inner_w - title_w - tags_w - 2
            top_line += glyphs.h + title_text + glyphs.h * filler_w + tags_text + glyphs.h
        elif title_w > 0 and title_w <= inner_w:
            # Fallback: only title fits
            rem_space = inner_w - title_w
            if spec.title_align == TextAlign.CENTER:
                left_pad = rem_space // 2
                right_pad = rem_space - left_pad
                top_line += glyphs.h * left_pad + title_text + glyphs.h * right_pad
            elif spec.title_align == TextAlign.RIGHT:
                top_line += glyphs.h * (rem_space - 1) + title_text + glyphs.h
            else: # LEFT
                top_line += glyphs.h + title_text + glyphs.h * (rem_space - 1)
        elif tags_w > 0 and tags_w <= inner_w:
            # Fallback: only tags fit
            rem_space = inner_w - tags_w
            top_line += glyphs.h * (rem_space - 1) + tags_text + glyphs.h
        else:
            top_line += glyphs.h * inner_w
            
        if spec.right.visible:
            top_line += glyphs.tr
        lines.append(top_line)
        
    # 3. Render Body Lines
    for line in content_lines:
        line_strip = strip_ansi(line)
        line_w = get_string_width(line_strip)
        
        # Pad or truncate to inner_w
        if line_w < inner_w:
            padded_line = line + " " * (inner_w - line_w)
        else:
            # Simple truncate (in real world we would respect ANSI codes, but for standard strings it is fine)
            # Or if it is already wrapped, it fits.
            padded_line = line
            
        body_line = ""
        if spec.left.visible:
            body_line += glyphs.v
        body_line += padded_line
        if spec.right.visible:
            body_line += glyphs.v
        lines.append(body_line)
        
    # 4. Render Bottom Border
    if spec.bottom.visible:
        bot_line = ""
        if spec.left.visible:
            bot_line += glyphs.bl
            
        # Subtitle support
        sub_text = f" {spec.subtitle} " if spec.subtitle else ""
        sub_w = get_string_width(sub_text)
        if sub_w > 0 and sub_w <= inner_w:
            rem_space = inner_w - sub_w
            # default bottom subtitle centered or left-aligned
            bot_line += glyphs.h + sub_text + glyphs.h * (rem_space - 1)
        else:
            bot_line += glyphs.h * inner_w
            
        if spec.right.visible:
            bot_line += glyphs.br
        lines.append(bot_line)
        
    return lines

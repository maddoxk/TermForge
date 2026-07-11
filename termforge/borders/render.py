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
    if spec.glyphs:
        from termforge.borders.glyphs import BorderGlyphs
        glyphs = BorderGlyphs(
            tl=spec.glyphs.get("tl", glyphs.tl),
            tr=spec.glyphs.get("tr", glyphs.tr),
            bl=spec.glyphs.get("bl", glyphs.bl),
            br=spec.glyphs.get("br", glyphs.br),
            h=spec.glyphs.get("h", glyphs.h),
            v=spec.glyphs.get("v", glyphs.v),
            t_down=spec.glyphs.get("t_down", glyphs.t_down),
            t_up=spec.glyphs.get("t_up", glyphs.t_up),
            t_right=spec.glyphs.get("t_right", glyphs.t_right),
            t_left=spec.glyphs.get("t_left", glyphs.t_left),
            cross=spec.glyphs.get("cross", glyphs.cross)
        )
    
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
        _pad = " " * max(0, spec.title_pad)
        title_text = f"{_pad}{spec.title}{_pad}" if spec.title else ""
        title_w = get_string_width(title_text)
        
        tags_text = ""
        if spec.tags:
            tags_str = " ".join(f"[{t}]" for t in spec.tags)
            tags_text = f" {tags_str} "
        tags_w = get_string_width(tags_text)
        
        # Build default background array of dashes
        chars = [glyphs.h] * inner_w
        
        if inner_w > 0:
            # 1. Compute positions
            # Title alignment
            if spec.title_align == TextAlign.LEFT:
                title_pos = 1 if inner_w > 2 and title_w > 0 else 0
            elif spec.title_align == TextAlign.RIGHT:
                title_pos = max(0, inner_w - title_w - (1 if inner_w > 2 and title_w > 0 else 0))
            else: # CENTER
                title_pos = max(0, (inner_w - title_w) // 2)
                
            # Tag alignment
            if spec.tag_align == TextAlign.LEFT:
                if spec.title_align == TextAlign.LEFT and title_w > 0:
                    tag_pos = title_pos + title_w
                else:
                    tag_pos = 1 if inner_w > 2 and tags_w > 0 else 0
            elif spec.tag_align == TextAlign.RIGHT:
                tag_pos = max(0, inner_w - tags_w - (1 if inner_w > 2 and tags_w > 0 else 0))
                if spec.title_align == TextAlign.RIGHT and title_w > 0:
                    tag_pos = max(0, title_pos - tags_w)
            else: # CENTER
                tag_pos = max(0, (inner_w - tags_w) // 2)
                if spec.title_align == TextAlign.CENTER and title_w > 0:
                    tag_pos = title_pos + title_w
                    
            # 2. Write content into array
            # Write tags first (title has priority/overwrites tags if they overlap)
            if tags_w > 0 and tag_pos + tags_w <= inner_w:
                for idx in range(tags_w):
                    chars[tag_pos + idx] = tags_text[idx]
            if title_w > 0 and title_pos + title_w <= inner_w:
                for idx in range(title_w):
                    chars[title_pos + idx] = title_text[idx]
                    
        top_line += "".join(chars)
            
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

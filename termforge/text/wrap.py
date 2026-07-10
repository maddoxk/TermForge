from __future__ import annotations
import unicodedata
from termforge.core.types import StyleSpec
from termforge.text.types import TextSpan, TextRun

def char_width(char: str) -> int:
    if char == "\n" or char == "\r":
        return 0
    w = unicodedata.east_asian_width(char)
    if w in ("W", "F"):
        return 2
    return 1

def get_string_width(text: str) -> int:
    return sum(char_width(c) for c in text)

def measure_text(run: TextRun) -> int:
    return sum(get_string_width(span.text) for span in run.spans)

def wrap_text(text: str, width: int) -> list[str]:
    if width <= 0:
        return [text]
    lines = []
    for paragraph in text.split("\n"):
        current_line = []
        current_width = 0
        words = paragraph.split(" ")
        i = 0
        while i < len(words):
            word = words[i]
            word_w = get_string_width(word)
            
            if word_w > width:
                # Split long word character-by-character
                sub_word = ""
                sub_w = 0
                for char in word:
                    c_w = char_width(char)
                    if sub_w + c_w > width:
                        lines.append(sub_word)
                        sub_word = char
                        sub_w = c_w
                    else:
                        sub_word += char
                        sub_w += c_w
                if sub_word:
                    words[i] = sub_word
                    continue
            
            space_w = 1 if current_line else 0
            if current_width + space_w + word_w > width:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_w
            else:
                if space_w:
                    current_line.append(word)
                else:
                    current_line = [word]
                current_width += space_w + word_w
            i += 1
            
        if current_line:
            lines.append(" ".join(current_line))
        elif not paragraph:
            lines.append("")
    return lines

def truncate_text(text: str, width: int, suffix: str = "…") -> str:
    suffix_w = get_string_width(suffix)
    if width <= suffix_w:
        # If target width is extremely small, just truncate the suffix
        current_w = 0
        result = ""
        for c in suffix:
            c_w = char_width(c)
            if current_w + c_w > width:
                break
            result += c
            current_w += c_w
        return result
        
    current_w = 0
    result = ""
    for c in text:
        c_w = char_width(c)
        if current_w + c_w + suffix_w > width:
            return result + suffix
        result += c
        current_w += c_w
    return result

def wrap_run(run: TextRun, width: int) -> list[TextRun]:
    if width <= 0:
        return [run]
        
    chars: list[tuple[str, StyleSpec | None]] = []
    for span in run.spans:
        for c in span.text:
            chars.append((c, span.style))
            
    lines: list[list[tuple[str, StyleSpec | None]]] = []
    current_line = []
    current_w = 0
    
    i = 0
    while i < len(chars):
        c, style = chars[i]
        c_w = char_width(c)
        
        if c == "\n":
            lines.append(current_line)
            current_line = []
            current_w = 0
            i += 1
            continue
            
        if current_w + c_w > width:
            # Word boundary search
            split_idx = -1
            for j in range(len(current_line) - 1, -1, -1):
                if current_line[j][0] == " ":
                    split_idx = j
                    break
                    
            if split_idx != -1 and split_idx > 0:
                word_part = current_line[split_idx+1:]
                current_line = current_line[:split_idx]
                lines.append(current_line)
                current_line = []
                current_w = 0
                i -= len(word_part)
            else:
                # Force wrap at character boundary
                if current_line:
                    lines.append(current_line)
                    current_line = []
                    current_w = 0
                else:
                    # Single character is wider than line, put it anyway to prevent infinite loop
                    current_line.append((c, style))
                    lines.append(current_line)
                    current_line = []
                    current_w = 0
                    i += 1
        else:
            current_line.append((c, style))
            current_w += c_w
            i += 1
            
    if current_line or not lines:
        lines.append(current_line)
        
    run_lines = []
    for line in lines:
        spans = []
        current_span_text = ""
        current_span_style = None
        
        for c, style in line:
            if style == current_span_style:
                current_span_text += c
            else:
                if current_span_text:
                    spans.append(TextSpan(text=current_span_text, style=current_span_style))
                current_span_text = c
                current_span_style = style
                
        if current_span_text:
            spans.append(TextSpan(text=current_span_text, style=current_span_style))
        run_lines.append(TextRun(spans=spans))
        
    return run_lines

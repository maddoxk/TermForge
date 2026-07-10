from __future__ import annotations
import re
from termforge.core.types import StyleSpec, ColorValue
from termforge.text.types import TextSpan, TextRun

def parse_color_string(color_str: str) -> ColorValue:
    color_str = color_str.strip().lower()
    if color_str.startswith("#"):
        h = color_str.lstrip("#")
        try:
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            return ColorValue(r, g, b, name=color_str)
        except ValueError:
            pass
    colors_map = {
        "black": (0, 0, 0), "red": (205, 0, 0), "green": (0, 205, 0), "yellow": (205, 205, 0),
        "blue": (0, 0, 238), "magenta": (205, 0, 205), "cyan": (0, 205, 205), "white": (229, 229, 229),
        "bright_black": (127, 127, 127), "bright_red": (255, 0, 0), "bright_green": (0, 255, 0),
        "bright_yellow": (255, 255, 0), "bright_blue": (92, 92, 255), "bright_magenta": (255, 0, 255),
        "bright_cyan": (0, 255, 255), "bright_white": (255, 255, 255)
    }
    if color_str in colors_map:
        r, g, b = colors_map[color_str]
        return ColorValue(r, g, b, name=color_str)
    return ColorValue(255, 255, 255, name=color_str) # default fallback

def parse_markup(text: str) -> TextRun:
    pattern = re.compile(r"(\[/?[a-zA-Z_][a-zA-Z0-9_]*(?:=[^\]]+)?\]|\[/\])")
    parts = pattern.split(text)
    
    # Track style state stack
    # Each entry in stack is a dict representing changes, or we can resolve the full style
    # Let's start with a base style (all False / None)
    current_style = {
        "fg": None, "bg": None,
        "bold": False, "dim": False, "italic": False,
        "underline": False, "strikethrough": False
    }
    
    style_stack = [dict(current_style)]
    spans = []
    
    for part in parts:
        if not part:
            continue
        if part.startswith("[") and part.endswith("]"):
            # It's a tag
            tag_content = part[1:-1]
            if tag_content.startswith("/"):
                # End tag
                # E.g. [/bold] or [/fg] or [/]
                end_tag = tag_content[1:].strip().lower()
                if end_tag == "" or end_tag == "/":
                    # pop all or reset to base if stack is empty
                    if len(style_stack) > 1:
                        style_stack.pop()
                    else:
                        style_stack = [dict(current_style)]
                else:
                    # Pop the last style from stack that matches this tag or just pop top
                    # For simple nested tags, popping top is usually fine or we can search back.
                    # Let's do simple stack pop.
                    if len(style_stack) > 1:
                        style_stack.pop()
            else:
                # Start tag
                # E.g. [bold] or [fg=red]
                if "=" in tag_content:
                    tag_name, tag_val = tag_content.split("=", 1)
                    tag_name = tag_name.strip().lower()
                    tag_val = tag_val.strip()
                else:
                    tag_name = tag_content.strip().lower()
                    tag_val = None
                
                # Copy top style to create new nested style
                new_style = dict(style_stack[-1])
                
                if tag_name == "bold":
                    new_style["bold"] = True
                elif tag_name == "dim":
                    new_style["dim"] = True
                elif tag_name == "italic":
                    new_style["italic"] = True
                elif tag_name == "underline":
                    new_style["underline"] = True
                elif tag_name == "strikethrough":
                    new_style["strikethrough"] = True
                elif tag_name == "fg" and tag_val:
                    new_style["fg"] = parse_color_string(tag_val)
                elif tag_name == "bg" and tag_val:
                    new_style["bg"] = parse_color_string(tag_val)
                
                style_stack.append(new_style)
        else:
            # Raw text
            active_style_dict = style_stack[-1]
            style_spec = StyleSpec(
                fg=active_style_dict["fg"],
                bg=active_style_dict["bg"],
                bold=active_style_dict["bold"],
                dim=active_style_dict["dim"],
                italic=active_style_dict["italic"],
                underline=active_style_dict["underline"],
                strikethrough=active_style_dict["strikethrough"]
            )
            spans.append(TextSpan(text=part, style=style_spec))
            
    return TextRun(spans=spans)

def strip_markup(text: str) -> str:
    pattern = re.compile(r"\[/?[a-zA-Z_][a-zA-Z0-9_]*(?:=[^\]]+)?\]|\[/\]")
    return pattern.sub("", text)

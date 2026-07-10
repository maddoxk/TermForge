#!/usr/bin/env python3
import sys
from termforge.borders.types import BorderSpec, BorderStyle
from termforge.borders.render import render_border

def main() -> None:
    styles = [
        BorderStyle.SINGLE,
        BorderStyle.DOUBLE,
        BorderStyle.ROUNDED,
        BorderStyle.HEAVY,
        BorderStyle.ASCII
    ]
    
    content = ["Hello TermForge", "Border System Demo"]
    
    for style in styles:
        print(f"\n--- {style.value.upper()} STYLE ---")
        spec = BorderSpec(style=style, title=f"{style.value.capitalize()}", title_align="center")
        lines = render_border(spec, content, width=24)
        for line in lines:
            print(line)
            
    print("\n--- BORDER WITH STATUS TAGS ---")
    spec_tags = BorderSpec(
        style=BorderStyle.ROUNDED,
        title="Set",
        tags=["On", "v1"]
    )
    lines_tags = render_border(spec_tags, content, width=24)
    for line in lines_tags:
        print(line)

if __name__ == "__main__":
    main()

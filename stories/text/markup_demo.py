#!/usr/bin/env python3
import sys
from termforge.core.types import ColorDepth
from termforge.text.types import TextSpec, TextAlign, TextOverflow
from termforge.text.render import render_text

def main() -> None:
    markup_examples = [
        "Plain text example.",
        "[bold]Bold text example.[/bold]",
        "[dim]Dim text example.[/dim]",
        "[italic]Italic text example.[/italic]",
        "[underline]Underline text example.[/underline]",
        "[strikethrough]Strikethrough text example.[/strikethrough]",
        "[bold][italic][underline]Bold, italic, and underline combined.[/][/][/]",
        "[fg=red]Red foreground text.[/fg]",
        "[bg=blue]Blue background text.[/bg]",
        "[fg=green][bg=yellow]Green on yellow text.[/fg][/bg]",
        "[fg=#ff00ff]Custom Magenta via hex #ff00ff[/fg]"
    ]
    
    print("--- TermForge Text Markup Gallery ---")
    for ex in markup_examples:
        spec = TextSpec(content=ex, align=TextAlign.LEFT, overflow=TextOverflow.WRAP, max_width=60)
        lines = render_text(spec, depth=ColorDepth.TRUECOLOR)
        for line in lines:
            print(line)
            
    print("\n--- Alignment Examples (width=40) ---")
    aligns = [TextAlign.LEFT, TextAlign.CENTER, TextAlign.RIGHT]
    for align in aligns:
        spec = TextSpec(content=f"[bold]Aligned {align.value.upper()}[/bold]", align=align, max_width=40)
        lines = render_text(spec, depth=ColorDepth.TRUECOLOR)
        print(f"|{lines[0]}|")
        
    print("\n--- Truncation / Overflow Examples (width=15) ---")
    long_text = "This is a very long string that will be cut off or wrapped."
    for overflow in [TextOverflow.CLIP, TextOverflow.ELLIPSIS, TextOverflow.WRAP]:
        spec = TextSpec(content=long_text, overflow=overflow, max_width=15)
        lines = render_text(spec, depth=ColorDepth.TRUECOLOR)
        print(f"--- {overflow.value.upper()} ---")
        for line in lines:
            print(line)

if __name__ == "__main__":
    main()

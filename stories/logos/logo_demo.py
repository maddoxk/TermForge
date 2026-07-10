#!/usr/bin/env python3
import sys
from termforge.core.types import ColorDepth
from termforge.logos.types import LogoSpec
from termforge.logos.render import render_logo

def main() -> None:
    fonts = ["small", "standard", "slant"]
    
    # We will use hex color values for the gradient: Red, Magenta, Blue
    gradient_colors = ["#ff0000", "#ff00ff", "#0000ff"]
    
    print("--- TermForge Logos Gallery ---")
    for font in fonts:
        print(f"\n--- FONT: {font.upper()} ---")
        spec = LogoSpec(text="TermForge", font=font, gradient=gradient_colors)
        lines = render_logo(spec, depth=ColorDepth.TRUECOLOR)
        for line in lines:
            print(line)

if __name__ == "__main__":
    main()

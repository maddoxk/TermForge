#!/usr/bin/env python3
import sys
from termforge.core.types import ColorDepth, StyleSpec, ColorValue
from termforge.logos.types import BannerSpec
from termforge.logos.banner import render_banner

def main() -> None:
    style = StyleSpec(bold=True, fg=ColorValue(137, 180, 250)) # Primary blue
    spec = BannerSpec(text="TERMFORGE", font="slant", style=style)
    lines = render_banner(spec, depth=ColorDepth.TRUECOLOR)
    
    print("--- Banner Spec Showcase ---")
    for line in lines:
        print(line)

if __name__ == "__main__":
    main()

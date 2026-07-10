#!/usr/bin/env python3
import sys
from termforge.core.types import ColorDepth
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.theme.preview import render_theme_preview

def main() -> None:
    print("--- TermForge Theme Gallery Preview ---")
    for name, theme in BUILTIN_THEMES.items():
        preview_lines = render_theme_preview(theme, depth=ColorDepth.TRUECOLOR)
        for line in preview_lines:
            print(line)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()

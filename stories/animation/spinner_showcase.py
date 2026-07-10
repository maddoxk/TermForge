#!/usr/bin/env python3
import sys
from termforge.core.types import ColorDepth
from termforge.animation.types import SpinnerSpec, SpinnerStyle
from termforge.animation.spinners import render_spinner

def main() -> None:
    styles = [
        SpinnerStyle.DOTS,
        SpinnerStyle.LINE,
        SpinnerStyle.BRAILLE,
        SpinnerStyle.BOUNCE,
        SpinnerStyle.CLOCK,
        SpinnerStyle.MOON,
        SpinnerStyle.ARROWS,
        SpinnerStyle.PULSE
    ]
    
    print("--- Spinner Showcase (Static Frames) ---")
    for style in styles:
        spec = SpinnerSpec(style=style, label=f"Loading in {style.value} style...", color_token="primary")
        # Print a few frames for each
        frames_str = []
        for f in range(5):
            frames_str.append(render_spinner(spec, f, depth=ColorDepth.TRUECOLOR))
        print(f"{style.value.upper()}:  " + "   ".join(frames_str))

if __name__ == "__main__":
    main()

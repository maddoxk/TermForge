#!/usr/bin/env python3
import sys
from termforge.core.types import ColorDepth
from termforge.animation.types import TransitionType
from termforge.logos.types import LogoSpec
from termforge.logos.reveal import render_logo_reveal

def main() -> None:
    # Render the banner with progress values: 0.0, 0.3, 0.7, 1.0
    spec = LogoSpec(text="TERMFORGE", font="slant", color_token="primary")
    progress_steps = [0.0, 0.3, 0.7, 1.0]
    
    print("--- Animated Logo Reveal Intros Showcase ---")
    for p in progress_steps:
        print(f"\n--- Reveal Progress: {p:.1f} ---")
        lines = render_logo_reveal(spec, TransitionType.FADE, p, depth=ColorDepth.TRUECOLOR)
        for line in lines:
            print(line)

if __name__ == "__main__":
    main()

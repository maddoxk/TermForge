#!/usr/bin/env python3
import sys
import os
import tempfile
from PIL import Image as PILImage
from termforge.core.types import ColorDepth
from termforge.image.types import ImageSpec, ImageFidelity
from termforge.image.render import render_image

def create_gradient_image() -> str:
    # Create a 30x15 gradient image (blue to yellow horizontally, black to red vertically)
    width = 30
    height = 15
    img = PILImage.new("RGB", (width, height))
    
    for y in range(height):
        for x in range(width):
            r = int(255 * (y / (height - 1)))
            g = int(255 * (x / (width - 1)))
            b = int(255 * (1 - (x / (width - 1))))
            img.putpixel((x, y), (r, g, b))
            
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    img.save(path)
    return path

def main() -> None:
    img_path = create_gradient_image()
    try:
        print("--- TermForge Image Gallery ---")
        
        print("\n1. Half-Block Mode (True Color, width=30):")
        spec_hb = ImageSpec(source=img_path, width=30, fidelity=ImageFidelity.HALF_BLOCK)
        lines_hb = render_image(spec_hb, depth=ColorDepth.TRUECOLOR)
        for line in lines_hb:
            print(line)
            
        print("\n2. ASCII Colored Mode (256-Color, width=40):")
        spec_ascii = ImageSpec(source=img_path, width=40, fidelity=ImageFidelity.ASCII_RAMP)
        lines_ascii = render_image(spec_ascii, depth=ColorDepth.COLOR_256)
        for line in lines_ascii:
            print(line)
            
        print("\n3. Monochrome ASCII Mode (width=40):")
        lines_mono = render_image(spec_ascii, depth=ColorDepth.MONOCHROME)
        for line in lines_mono:
            print(line)
            
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)

if __name__ == "__main__":
    main()

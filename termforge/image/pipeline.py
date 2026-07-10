from __future__ import annotations
import urllib.request
import io
from PIL import Image

def resize_for_terminal(img_w: int, img_h: int, term_cols: int | None, term_rows: int | None, preserve_aspect: bool, half_block: bool = True) -> tuple[int, int]:
    if term_cols is None and term_rows is None:
        term_cols = 80
        
    if term_cols is not None and term_rows is not None:
        w = term_cols
        h = term_rows * 2 if half_block else term_rows
        if preserve_aspect:
            img_aspect = img_w / img_h
            if not half_block:
                display_aspect = w / (h * 2.0)
            else:
                display_aspect = w / h
                
            if img_aspect > display_aspect:
                # Width limit
                w = term_cols
                if half_block:
                    h = int(w / img_aspect)
                else:
                    h = int(w / (2.0 * img_aspect))
            else:
                # Height limit
                h = term_rows * 2 if half_block else term_rows
                if half_block:
                    w = int(h * img_aspect)
                else:
                    w = int(h * img_aspect * 2.0)
        return max(1, w), max(1, h)
        
    if term_cols is not None:
        w = term_cols
        img_aspect = img_w / img_h
        if half_block:
            h = int(w / img_aspect)
        else:
            h = int(w / (2.0 * img_aspect))
        return max(1, w), max(1, h)
        
    if term_rows is not None:
        h = term_rows * 2 if half_block else term_rows
        img_aspect = img_w / img_h
        if half_block:
            w = int(h * img_aspect)
        else:
            w = int(h * img_aspect * 2.0)
        return max(1, w), max(1, h)
        
    return 80, 40

def load_pixels(source: str, target_width: int, target_height: int) -> list[list[tuple[int, int, int]]]:
    # 1. Load image (from path or URL)
    if source.startswith("http://") or source.startswith("https://"):
        req = urllib.request.Request(source, headers={'User-Agent': 'TermForge-Image-Loader'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
        img = Image.open(io.BytesIO(img_data))
    else:
        img = Image.open(source)
        
    # Convert to RGB
    img = img.convert("RGB")
    
    # 2. Resize using Pillow
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # 3. Extract pixels
    pixels = []
    width, height = img.size
    for y in range(height):
        row = []
        for x in range(width):
            row.append(img.getpixel((x, y)))
        pixels.append(row)
        
    return pixels

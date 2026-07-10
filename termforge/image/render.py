from __future__ import annotations
from termforge.core.types import ColorDepth
from termforge.core.theme import ThemeTokens
from termforge.image.types import ImageSpec, ImageFidelity
from termforge.image.pipeline import resize_for_terminal, load_pixels
from termforge.image.half_block import render_half_block
from termforge.image.ascii_ramp import render_ascii, render_ascii_colored

def render_image(
    spec: ImageSpec,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
    available_width: int | None = None,
    available_height: int | None = None
) -> list[str]:
    # 1. Determine fidelity
    fidelity = spec.fidelity
    if fidelity is None:
        if depth == ColorDepth.MONOCHROME:
            fidelity = ImageFidelity.ASCII_RAMP
        else:
            fidelity = ImageFidelity.HALF_BLOCK
            
    # 2. Get image size to scale properly
    # We open the image first to get its dimensions
    # Let's import PIL inside render to keep it isolated if needed, but we already have PIL in pipeline.py
    from PIL import Image
    import urllib.request
    import io
    
    source = spec.source
    if not source:
        return []
        
    try:
        if source.startswith("http://") or source.startswith("https://"):
            req = urllib.request.Request(source, headers={'User-Agent': 'TermForge-Image-Loader'})
            with urllib.request.urlopen(req) as response:
                img_data = response.read()
            img = Image.open(io.BytesIO(img_data))
        else:
            img = Image.open(source)
        img_w, img_h = img.size
    except Exception as e:
        # Fallback or error print
        return [f"[Image Load Error: {e}]"]

    # 3. Calculate target cols/rows
    cols = spec.width
    rows = spec.height
    
    if cols is None and rows is None:
        cols = available_width
        rows = available_height
        
    is_hb = (fidelity == ImageFidelity.HALF_BLOCK)
    w, h = resize_for_terminal(img_w, img_h, cols, rows, spec.preserve_aspect, half_block=is_hb)
    
    # 4. Load pixels
    pixels = load_pixels(source, w, h)
    
    # 5. Render
    if fidelity == ImageFidelity.HALF_BLOCK:
        return render_half_block(pixels, depth)
    else:
        if depth == ColorDepth.MONOCHROME:
            return render_ascii(pixels)
        else:
            return render_ascii_colored(pixels, depth)

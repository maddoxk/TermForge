import pytest
import tempfile
import os
from PIL import Image as PILImage
from termforge.core.types import ColorDepth
from termforge.image.types import ImageSpec, ImageFidelity
from termforge.image.pipeline import resize_for_terminal, load_pixels
from termforge.image.ansi import fg_color_ansi, bg_color_ansi
from termforge.image.half_block import render_half_block
from termforge.image.ascii_ramp import rgb_to_brightness, render_ascii, render_ascii_colored
from termforge.image.render import render_image

@pytest.fixture
def temp_image():
    # Create a 4x4 image with a simple colored pattern
    img = PILImage.new("RGB", (4, 4))
    pixels = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255),
        (0, 0, 0), (128, 128, 128), (255, 255, 0), (255, 0, 255),
        (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (64, 64, 64), (192, 192, 192), (32, 64, 128), (10, 20, 30)
    ]
    img.putdata(pixels)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        img.save(f.name)
        temp_path = f.name
        
    yield temp_path
    
    if os.path.exists(temp_path):
        os.remove(temp_path)

def test_image_spec_serialization():
    spec = ImageSpec(source="test.png", width=40, height=20, fidelity=ImageFidelity.HALF_BLOCK, preserve_aspect=False)
    spec_dict = spec.to_dict()
    assert spec_dict["spec_type"] == "image"
    assert spec_dict["source"] == "test.png"
    assert spec_dict["width"] == 40
    assert spec_dict["fidelity"] == "half_block"
    assert spec_dict["preserve_aspect"] is False
    
    spec_back = ImageSpec.from_dict(spec_dict)
    assert spec_back.source == "test.png"
    assert spec_back.width == 40
    assert spec_back.fidelity == ImageFidelity.HALF_BLOCK
    assert spec_back.preserve_aspect is False

def test_resize_for_terminal():
    # Test half block mode
    w, h = resize_for_terminal(100, 100, 40, None, preserve_aspect=True, half_block=True)
    assert w == 40
    assert h == 40 # 100/100 = 1.0 aspect, half block pixels are 1:1, so w=40, h=40
    
    # Test ASCII ramp mode (2:1 terminal cells)
    w, h = resize_for_terminal(100, 100, 40, None, preserve_aspect=True, half_block=False)
    assert w == 40
    assert h == 20 # ASCII pixels are 1:2, so height is halved to preserve aspect ratio

def test_load_pixels(temp_image):
    pixels = load_pixels(temp_image, 2, 2)
    assert len(pixels) == 2
    assert len(pixels[0]) == 2
    assert isinstance(pixels[0][0], tuple)
    assert len(pixels[0][0]) == 3

def test_ansi_generation():
    fg = fg_color_ansi(255, 0, 0, ColorDepth.TRUECOLOR)
    assert fg == "\033[38;2;255;0;0m"
    
    bg = bg_color_ansi(0, 0, 255, ColorDepth.TRUECOLOR)
    assert bg == "\033[48;2;0;0;255m"

def test_half_block_rendering():
    pixels = [
        [(255, 0, 0), (0, 255, 0)],
        [(0, 0, 255), (255, 255, 255)]
    ]
    lines = render_half_block(pixels, ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    # Check that it contains half block characters and escape sequences
    assert "▀" in lines[0]

def test_ascii_ramp_rendering():
    pixels = [
        [(0, 0, 0), (255, 255, 255)]
    ]
    lines = render_ascii(pixels, " .@")
    assert len(lines) == 1
    assert lines[0] == " .@" or lines[0] == " @" or lines[0][0] == " " # Check spacing

def test_render_image(temp_image):
    spec = ImageSpec(source=temp_image, width=4, height=2, fidelity=ImageFidelity.HALF_BLOCK)
    lines = render_image(spec, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 2 # 4 pixel rows high, rendered in half block -> 2 terminal lines

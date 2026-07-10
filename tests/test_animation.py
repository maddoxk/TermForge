import pytest
from termforge.core.types import ColorDepth
from termforge.animation.types import SpinnerSpec, SpinnerStyle, TransitionSpec, TransitionType
from termforge.animation.spinners import get_spinner_frame, render_spinner
from termforge.animation.transitions import render_transition

def test_animation_specs_serialization():
    spinner = SpinnerSpec(style=SpinnerStyle.BRAILLE, label="Loading", fps=12.0, color_token="secondary")
    spinner_dict = spinner.to_dict()
    assert spinner_dict["style"] == "braille"
    assert spinner_dict["label"] == "Loading"
    assert spinner_dict["fps"] == 12.0
    
    spinner_back = SpinnerSpec.from_dict(spinner_dict)
    assert spinner_back.style == SpinnerStyle.BRAILLE
    assert spinner_back.label == "Loading"
    assert spinner_back.fps == 12.0

    trans = TransitionSpec(transition_type=TransitionType.SLIDE_LEFT, duration_ms=500.0)
    trans_dict = trans.to_dict()
    assert trans_dict["transition_type"] == "slide_left"
    assert trans_dict["duration_ms"] == 500.0

def test_spinner_frames():
    assert get_spinner_frame(SpinnerStyle.LINE, 0) == "-"
    assert get_spinner_frame(SpinnerStyle.LINE, 1) == "\\"
    assert get_spinner_frame(SpinnerStyle.LINE, 4) == "-" # loops

def test_render_spinner():
    spec = SpinnerSpec(style=SpinnerStyle.LINE, label="Wait")
    rendered = render_spinner(spec, 0, depth=ColorDepth.MONOCHROME)
    assert rendered == "- Wait"

def test_render_transition_fade():
    spec = TransitionSpec(
        transition_type=TransitionType.FADE,
        from_content=["AAA"],
        to_content=["BBB"]
    )
    # Check midway and endpoints
    lines_start = render_transition(spec, 0.0, depth=ColorDepth.MONOCHROME)
    assert len(lines_start) == 1
    assert "AAA" in lines_start[0]
    
    lines_end = render_transition(spec, 1.0, depth=ColorDepth.MONOCHROME)
    assert len(lines_end) == 1
    assert "BBB" in lines_end[0]

def test_render_transition_wipe():
    spec = TransitionSpec(
        transition_type=TransitionType.WIPE,
        from_content=["XXXXX"],
        to_content=["YYYYY"]
    )
    # progress=0.6: 3 chars Y, 2 chars X -> YYYXX
    lines = render_transition(spec, 0.6, depth=ColorDepth.MONOCHROME)
    # Since it's monochrome, strip the RESET codes to check characters
    from termforge.borders.render import strip_ansi
    plain = strip_ansi(lines[0])
    assert plain == "YYYXX"

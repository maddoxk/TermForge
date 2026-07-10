"""TermForge animation module — spinners and transitions."""
from termforge.animation.types import SpinnerStyle, TransitionType, SpinnerSpec, TransitionSpec
from termforge.animation.spinners import SPINNER_FRAMES, get_spinner_frame, render_spinner
from termforge.animation.transitions import render_transition

__all__ = [
    "SpinnerStyle",
    "TransitionType",
    "SpinnerSpec",
    "TransitionSpec",
    "SPINNER_FRAMES",
    "get_spinner_frame",
    "render_spinner",
    "render_transition",
]

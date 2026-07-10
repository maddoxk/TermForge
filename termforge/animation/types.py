from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from termforge.core.types import RenderableSpec

class SpinnerStyle(str, Enum):
    DOTS = "dots"
    LINE = "line"
    BRAILLE = "braille"
    BOUNCE = "bounce"
    CLOCK = "clock"
    MOON = "moon"
    ARROWS = "arrows"
    PULSE = "pulse"

class TransitionType(str, Enum):
    FADE = "fade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    WIPE = "wipe"

@dataclass
class SpinnerSpec(RenderableSpec):
    style: SpinnerStyle = SpinnerStyle.DOTS
    label: str | None = None
    fps: float = 10.0
    color_token: str = "primary"
    spec_type: str = "spinner"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "style": self.style.value,
            "label": self.label,
            "fps": self.fps,
            "color_token": self.color_token
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SpinnerSpec:
        return cls(
            style=SpinnerStyle(d.get("style", "dots")),
            label=d.get("label"),
            fps=d.get("fps", 10.0),
            color_token=d.get("color_token", "primary")
        )

@dataclass
class TransitionSpec(RenderableSpec):
    transition_type: TransitionType = TransitionType.FADE
    duration_ms: float = 1000.0
    from_content: list[str] = field(default_factory=list)
    to_content: list[str] = field(default_factory=list)
    spec_type: str = "transition"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "transition_type": self.transition_type.value,
            "duration_ms": self.duration_ms,
            "from_content": self.from_content,
            "to_content": self.to_content
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TransitionSpec:
        return cls(
            transition_type=TransitionType(d.get("transition_type", "fade")),
            duration_ms=d.get("duration_ms", 1000.0),
            from_content=d.get("from_content", []),
            to_content=d.get("to_content", [])
        )

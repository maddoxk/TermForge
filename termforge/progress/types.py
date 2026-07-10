from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from termforge.core.types import RenderableSpec, StyleSpec

@dataclass
class ProgressSpec(RenderableSpec):
    progress: float = 0.0
    filled_char: str = "█"
    empty_char: str = "░"
    head_char: str = ""
    show_text: bool = True
    text_format: str = "{percent}%"
    width: int | None = None
    filled_style: StyleSpec | None = None
    empty_style: StyleSpec | None = None
    spec_type: str = "progress"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "progress": self.progress,
            "filled_char": self.filled_char,
            "empty_char": self.empty_char,
            "head_char": self.head_char,
            "show_text": self.show_text,
            "text_format": self.text_format,
            "width": self.width,
            "filled_style": self.filled_style.to_dict() if self.filled_style else None,
            "empty_style": self.empty_style.to_dict() if self.empty_style else None
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ProgressSpec:
        return cls(
            progress=d.get("progress", 0.0),
            filled_char=d.get("filled_char", "█"),
            empty_char=d.get("empty_char", "░"),
            head_char=d.get("head_char", ""),
            show_text=d.get("show_text", True),
            text_format=d.get("text_format", "{percent}%"),
            width=d.get("width"),
            filled_style=StyleSpec.from_dict(d["filled_style"]) if d.get("filled_style") else None,
            empty_style=StyleSpec.from_dict(d["empty_style"]) if d.get("empty_style") else None
        )

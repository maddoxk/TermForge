from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from termforge.core.types import RenderableSpec, StyleSpec, ColorValue

class TextAlign(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class TextOverflow(str, Enum):
    CLIP = "clip"
    TRUNCATE = "truncate"   # explicit hard-truncate (alias for CLIP, no suffix)
    ELLIPSIS = "ellipsis"
    WRAP = "wrap"
    MARQUEE = "marquee"

@dataclass
class TextSpan:
    text: str
    style: StyleSpec | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "style": self.style.to_dict() if self.style else None
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TextSpan:
        style_dict = d.get("style")
        style = StyleSpec.from_dict(style_dict) if style_dict else None
        return cls(text=d["text"], style=style)

@dataclass
class TextRun:
    spans: list[TextSpan] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "spans": [span.to_dict() for span in self.spans]
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TextRun:
        return cls(spans=[TextSpan.from_dict(s) for s in d.get("spans", [])])

@dataclass
class TextSpec(RenderableSpec):
    content: str | TextRun = ""
    align: TextAlign = TextAlign.LEFT
    overflow: TextOverflow = TextOverflow.WRAP
    max_width: int | None = None
    max_lines: int | None = None
    spec_type: str = "text"

    def to_dict(self) -> dict[str, Any]:
        content_data = self.content.to_dict() if isinstance(self.content, TextRun) else self.content
        return {
            "spec_type": self.spec_type,
            "content": content_data,
            "align": self.align.value,
            "overflow": self.overflow.value,
            "max_width": self.max_width,
            "max_lines": self.max_lines
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TextSpec:
        content_data = d.get("content", "")
        if isinstance(content_data, dict) and "spans" in content_data:
            content = TextRun.from_dict(content_data)
        else:
            content = content_data
        return cls(
            content=content,
            align=TextAlign(d.get("align", "left")),
            overflow=TextOverflow(d.get("overflow", "wrap")),
            max_width=d.get("max_width"),
            max_lines=d.get("max_lines")
        )

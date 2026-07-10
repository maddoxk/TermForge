from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from termforge.core.types import RenderableSpec
from termforge.text.types import TextAlign

class BorderStyle(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"
    ROUNDED = "rounded"
    HEAVY = "heavy"
    ASCII = "ascii"
    NONE = "none"

@dataclass
class BorderSide:
    visible: bool = True
    style_override: BorderStyle | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "visible": self.visible,
            "style_override": self.style_override.value if self.style_override else None
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BorderSide:
        override = d.get("style_override")
        style_override = BorderStyle(override) if override else None
        return cls(
            visible=d.get("visible", True),
            style_override=style_override
        )

@dataclass
class BorderSpec(RenderableSpec):
    style: BorderStyle = BorderStyle.SINGLE
    top: BorderSide = field(default_factory=BorderSide)
    right: BorderSide = field(default_factory=BorderSide)
    bottom: BorderSide = field(default_factory=BorderSide)
    left: BorderSide = field(default_factory=BorderSide)
    title: str | None = None
    title_align: TextAlign = TextAlign.LEFT
    subtitle: str | None = None
    content: RenderableSpec | None = None
    glyphs: dict[str, str] | None = None
    tags: list[str] = field(default_factory=list)
    spec_type: str = "border"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "style": self.style.value,
            "top": self.top.to_dict(),
            "right": self.right.to_dict(),
            "bottom": self.bottom.to_dict(),
            "left": self.left.to_dict(),
            "title": self.title,
            "title_align": self.title_align.value,
            "subtitle": self.subtitle,
            "content": self.content.to_dict() if self.content else None,
            "glyphs": self.glyphs,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BorderSpec:
        from termforge.core.types import RenderableSpec
        content_dict = d.get("content")
        content = None
        if content_dict:
            content = RenderableSpec.from_dict(content_dict)
            
        return cls(
            style=BorderStyle(d.get("style", "single")),
            top=BorderSide.from_dict(d.get("top", {})),
            right=BorderSide.from_dict(d.get("right", {})),
            bottom=BorderSide.from_dict(d.get("bottom", {})),
            left=BorderSide.from_dict(d.get("left", {})),
            title=d.get("title"),
            title_align=TextAlign(d.get("title_align", "left")),
            subtitle=d.get("subtitle"),
            content=content,
            glyphs=d.get("glyphs"),
            tags=d.get("tags", [])
        )

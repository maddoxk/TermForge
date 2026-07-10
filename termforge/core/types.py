"""Core data types and the Renderable protocol for TermForge.

All types are plain dataclasses with to_dict()/from_dict() round-trip
serialization. No Rich/Textual imports.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ColorDepth(Enum):
    """Supported terminal color depth tiers."""

    TRUECOLOR = "truecolor"
    COLOR_256 = "color_256"
    COLOR_16 = "color_16"
    MONOCHROME = "monochrome"


@dataclass
class ColorValue:
    """Stores a color as an (r, g, b) tuple with an optional semantic name."""

    r: int
    g: int
    b: int
    name: str | None = None

    @property
    def rgb(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"r": self.r, "g": self.g, "b": self.b}
        if self.name is not None:
            d["name"] = self.name
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ColorValue:
        return cls(r=d["r"], g=d["g"], b=d["b"], name=d.get("name"))


@dataclass
class Size:
    """Width × height in character cells."""

    width: int
    height: int

    def to_dict(self) -> dict[str, Any]:
        return {"width": self.width, "height": self.height}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Size:
        return cls(width=d["width"], height=d["height"])


@dataclass
class Position:
    """(x, y) position in character cells, origin at top-left."""

    x: int
    y: int

    def to_dict(self) -> dict[str, Any]:
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Position:
        return cls(x=d["x"], y=d["y"])


@dataclass
class Spacing:
    """Spacing for padding/margin: top, right, bottom, left."""

    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0

    @property
    def horizontal(self) -> int:
        return self.left + self.right

    @property
    def vertical(self) -> int:
        return self.top + self.bottom

    def to_dict(self) -> dict[str, Any]:
        return {
            "top": self.top,
            "right": self.right,
            "bottom": self.bottom,
            "left": self.left,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Spacing:
        return cls(
            top=d.get("top", 0),
            right=d.get("right", 0),
            bottom=d.get("bottom", 0),
            left=d.get("left", 0),
        )


@dataclass
class BoxConstraints:
    """Min/max width and height constraints for layout."""

    min_width: int = 0
    max_width: int = 0
    min_height: int = 0
    max_height: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "min_width": self.min_width,
            "max_width": self.max_width,
            "min_height": self.min_height,
            "max_height": self.max_height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BoxConstraints:
        return cls(
            min_width=d.get("min_width", 0),
            max_width=d.get("max_width", 0),
            min_height=d.get("min_height", 0),
            max_height=d.get("max_height", 0),
        )


@dataclass
class LayoutResult:
    """Result of layout computation — an absolute-positioned tree."""

    position: Position
    size: Size
    children: list[LayoutResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "position": self.position.to_dict(),
            "size": self.size.to_dict(),
            "children": [c.to_dict() for c in self.children],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> LayoutResult:
        return cls(
            position=Position.from_dict(d["position"]),
            size=Size.from_dict(d["size"]),
            children=[LayoutResult.from_dict(c) for c in d.get("children", [])],
        )


@dataclass
class RenderableSpec:
    """Base spec that all component specs inherit from.

    Every component is described as a plain-data spec before it touches
    any rendering backend.
    """

    spec_type: str = "base"

    def to_dict(self) -> dict[str, Any]:
        return {"spec_type": self.spec_type}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RenderableSpec:
        return cls(spec_type=d.get("spec_type", "base"))


@dataclass
class StyleSpec:
    """Text styling specification — colors + decorations."""

    fg: ColorValue | None = None
    bg: ColorValue | None = None
    bold: bool = False
    dim: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "bold": self.bold,
            "dim": self.dim,
            "italic": self.italic,
            "underline": self.underline,
            "strikethrough": self.strikethrough,
        }
        if self.fg is not None:
            d["fg"] = self.fg.to_dict()
        if self.bg is not None:
            d["bg"] = self.bg.to_dict()
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StyleSpec:
        fg = ColorValue.from_dict(d["fg"]) if "fg" in d else None
        bg = ColorValue.from_dict(d["bg"]) if "bg" in d else None
        return cls(
            fg=fg,
            bg=bg,
            bold=d.get("bold", False),
            dim=d.get("dim", False),
            italic=d.get("italic", False),
            underline=d.get("underline", False),
            strikethrough=d.get("strikethrough", False),
        )

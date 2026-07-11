"""TermForge status bar component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class StatusSectionSpec:
    """An individual informational text segment inside the status bar.

    Attributes:
        text: Plain text content of the segment.
        style: Theme style token name (e.g. "colors.success").
    """
    text: str
    style: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "style": self.style,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StatusSectionSpec:
        return cls(
            text=d.get("text", ""),
            style=d.get("style"),
        )


@dataclass
class StatusBarSpec(RenderableSpec):
    """Specification for status and metadata footer bar layout.

    Attributes:
        left: Left-aligned information sections.
        center: Centered information sections.
        right: Right-aligned information sections.
        separator: String dividing items within alignment groups.
        separator_style: Theme style token for delimiter characters.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    left: list[StatusSectionSpec] = field(default_factory=list)
    center: list[StatusSectionSpec] = field(default_factory=list)
    right: list[StatusSectionSpec] = field(default_factory=list)
    separator: str = " │ "
    separator_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "status_bar"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing status bar properties.
        """
        return {
            "spec_type": self.spec_type,
            "left": [s.to_dict() for s in self.left],
            "center": [s.to_dict() for s in self.center],
            "right": [s.to_dict() for s in self.right],
            "separator": self.separator,
            "separator_style": self.separator_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StatusBarSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing status bar properties.

        Returns:
            A new :class:`StatusBarSpec` instance.
        """
        return cls(
            left=[StatusSectionSpec.from_dict(s) for s in d.get("left", [])],
            center=[StatusSectionSpec.from_dict(s) for s in d.get("center", [])],
            right=[StatusSectionSpec.from_dict(s) for s in d.get("right", [])],
            separator=d.get("separator", " │ "),
            separator_style=d.get("separator_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

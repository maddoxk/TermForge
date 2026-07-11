"""TermForge tooltip component specifications."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class TooltipSpec(RenderableSpec):
    """Specification for anchored floating helper tooltip bubbles.

    Attributes:
        text: Text message content inside the tooltip bubble.
        anchor_x: 0-indexed column coordinate of anchor.
        anchor_y: 0-indexed row coordinate of anchor.
        placement: Location relative to anchor ("top", "bottom", "left", "right").
        bubble_style: Theme style token for text/border.
        pointer_style: Theme style token for pointer indicator glyph.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    text: str = ""

    anchor_x: int = 0
    anchor_y: int = 0
    placement: str = "bottom"
    bubble_style: str | None = None
    pointer_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "tooltip"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing tooltip properties.
        """
        return {
            "spec_type": self.spec_type,
            "text": self.text,
            "anchor_x": self.anchor_x,
            "anchor_y": self.anchor_y,
            "placement": self.placement,
            "bubble_style": self.bubble_style,
            "pointer_style": self.pointer_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TooltipSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing tooltip properties.

        Returns:
            A new :class:`TooltipSpec` instance.
        """
        return cls(
            text=d.get("text", ""),
            anchor_x=d.get("anchor_x", 0),
            anchor_y=d.get("anchor_y", 0),
            placement=d.get("placement", "bottom"),
            bubble_style=d.get("bubble_style"),
            pointer_style=d.get("pointer_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

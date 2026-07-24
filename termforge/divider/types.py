"""TermForge divider component specifications."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class DividerSpec(RenderableSpec):
    """Specification for horizontal line divider elements.

    Attributes:
        label: Text string embedded in horizontal divider line.
        alignment: Text label alignment ("left", "center", "right").
        line_char: Character string used for generating divider line ("─", "═", etc.).
        label_style: Theme style token for label text.
        line_style: Theme style token for divider line.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    label: str = ""
    alignment: str = "center"
    line_char: str = "─"
    label_style: str | None = None
    line_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "divider"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing divider properties.
        """
        return {
            "spec_type": self.spec_type,
            "label": self.label,
            "alignment": self.alignment,
            "line_char": self.line_char,
            "label_style": self.label_style,
            "line_style": self.line_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DividerSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing divider properties.

        Returns:
            A new :class:`DividerSpec` instance.
        """
        return cls(
            label=d.get("label", ""),
            alignment=d.get("alignment", "center"),
            line_char=d.get("line_char", "─"),
            label_style=d.get("label_style"),
            line_style=d.get("line_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

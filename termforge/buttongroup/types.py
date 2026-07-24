"""TermForge button group component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class ButtonGroupSpec(RenderableSpec):
    """Specification for horizontal button group elements.

    Attributes:
        buttons: List of button label strings.
        selected_idx: Focused option index under cursor.
        separator: Spacing string separating adjacent button items (default "   ").
        selected_style: Theme style token for focused/active button item.
        unselected_style: Theme style token for unfocused button items.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    buttons: list[str] = field(default_factory=list)
    selected_idx: int = 0
    separator: str = "   "
    selected_style: str | None = None
    unselected_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "buttongroup"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing button group properties.
        """
        return {
            "spec_type": self.spec_type,
            "buttons": list(self.buttons),
            "selected_idx": self.selected_idx,
            "separator": self.separator,
            "selected_style": self.selected_style,
            "unselected_style": self.unselected_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ButtonGroupSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing button group properties.

        Returns:
            A new :class:`ButtonGroupSpec` instance.
        """
        return cls(
            buttons=list(d.get("buttons", [])),
            selected_idx=d.get("selected_idx", 0),
            separator=d.get("separator", "   "),
            selected_style=d.get("selected_style"),
            unselected_style=d.get("unselected_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

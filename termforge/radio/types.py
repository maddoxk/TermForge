"""TermForge radio button component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class RadioButtonItemSpec:
    """An individual option item inside a radio button group.

    Attributes:
        label: Text label of the option.
        active: Boolean indicator whether this option is the selected active option.
    """
    label: str
    active: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "active": self.active,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RadioButtonItemSpec:
        return cls(
            label=d.get("label", ""),
            active=d.get("active", False),
        )


@dataclass
class RadioButtonSpec(RenderableSpec):
    """Specification for RadioButton option list widgets.

    Attributes:
        items: List of RadioButtonItemSpec elements.
        selected_idx: Focused option item index under cursor.
        active_indicator: Text indicator prefix for active radio buttons (default "(●) ").
        inactive_indicator: Text indicator prefix for inactive radio buttons (default "( ) ").
        active_style: Theme style token for the active radio button.
        selected_style: Theme style token for the focused cursor choice option.
        inactive_style: Theme style token for normal inactive radio button options.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    items: list[RadioButtonItemSpec] = field(default_factory=list)
    selected_idx: int = 0
    active_indicator: str = "(●) "
    inactive_indicator: str = "( ) "
    active_style: str | None = None
    selected_style: str | None = None
    inactive_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "radio_button"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing radio button properties.
        """
        return {
            "spec_type": self.spec_type,
            "items": [item.to_dict() for item in self.items],
            "selected_idx": self.selected_idx,
            "active_indicator": self.active_indicator,
            "inactive_indicator": self.inactive_indicator,
            "active_style": self.active_style,
            "selected_style": self.selected_style,
            "inactive_style": self.inactive_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RadioButtonSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing radio button properties.

        Returns:
            A new :class:`RadioButtonSpec` instance.
        """
        return cls(
            items=[RadioButtonItemSpec.from_dict(item) for item in d.get("items", [])],
            selected_idx=d.get("selected_idx", 0),
            active_indicator=d.get("active_indicator", "(●) "),
            inactive_indicator=d.get("inactive_indicator", "( ) "),
            active_style=d.get("active_style"),
            selected_style=d.get("selected_style"),
            inactive_style=d.get("inactive_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

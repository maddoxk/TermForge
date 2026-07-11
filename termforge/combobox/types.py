"""TermForge combobox component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class ComboboxSpec(RenderableSpec):
    """Specification for dropdown select boxes (comboboxes).

    Attributes:
        options: List of choice strings.
        selected_idx: Index of currently selected option.
        is_open: Boolean flag showing whether dropdown list is open.
        active_hover_idx: Focused option item index inside dropdown.
        caret: Caret dropdown indicator character (default "▼").
        field_style: Theme style token for closed field box text.
        dropdown_style: Theme style token for dropdown items.
        hover_style: Theme style token for active focused item inside dropdown.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    options: list[str] = field(default_factory=list)
    selected_idx: int = 0
    is_open: bool = False
    active_hover_idx: int = 0
    caret: str = "▼"
    field_style: str | None = None
    dropdown_style: str | None = None
    hover_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "combobox"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing combobox properties.
        """
        return {
            "spec_type": self.spec_type,
            "options": list(self.options),
            "selected_idx": self.selected_idx,
            "is_open": self.is_open,
            "active_hover_idx": self.active_hover_idx,
            "caret": self.caret,
            "field_style": self.field_style,
            "dropdown_style": self.dropdown_style,
            "hover_style": self.hover_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ComboboxSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing combobox properties.

        Returns:
            A new :class:`ComboboxSpec` instance.
        """
        return cls(
            options=list(d.get("options", [])),
            selected_idx=d.get("selected_idx", 0),
            is_open=d.get("is_open", False),
            active_hover_idx=d.get("active_hover_idx", 0),
            caret=d.get("caret", "▼"),
            field_style=d.get("field_style"),
            dropdown_style=d.get("dropdown_style"),
            hover_style=d.get("hover_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

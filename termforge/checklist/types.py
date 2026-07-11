"""TermForge checklist component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class ChecklistItemSpec:
    """An individual toggleable option item inside a checklist.

    Attributes:
        label: Text label of the option.
        checked: Boolean indicator whether the option is checked.
    """
    label: str
    checked: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "checked": self.checked,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ChecklistItemSpec:
        return cls(
            label=d.get("label", ""),
            checked=d.get("checked", False),
        )


@dataclass
class ChecklistSpec(RenderableSpec):
    """Specification for Checklist option widgets.

    Attributes:
        items: List of ChecklistItemSpec elements.
        selected_idx: Focused option item index.
        checked_indicator: Text indicator for checked checkboxes.
        unchecked_indicator: Text indicator for unchecked checkboxes.
        checked_style: Theme style token for checked options.
        selected_style: Theme style token for focused keyboard cursor option.
        unchecked_style: Theme style token for standard unchecked options.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    items: list[ChecklistItemSpec] = field(default_factory=list)
    selected_idx: int = 0
    checked_indicator: str = "[x] "
    unchecked_indicator: str = "[ ] "
    checked_style: str | None = None
    selected_style: str | None = None
    unchecked_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "checklist"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing checklist properties.
        """
        return {
            "spec_type": self.spec_type,
            "items": [item.to_dict() for item in self.items],
            "selected_idx": self.selected_idx,
            "checked_indicator": self.checked_indicator,
            "unchecked_indicator": self.unchecked_indicator,
            "checked_style": self.checked_style,
            "selected_style": self.selected_style,
            "unchecked_style": self.unchecked_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ChecklistSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing checklist properties.

        Returns:
            A new :class:`ChecklistSpec` instance.
        """
        return cls(
            items=[ChecklistItemSpec.from_dict(item) for item in d.get("items", [])],
            selected_idx=d.get("selected_idx", 0),
            checked_indicator=d.get("checked_indicator", "[x] "),
            unchecked_indicator=d.get("unchecked_indicator", "[ ] "),
            checked_style=d.get("checked_style"),
            selected_style=d.get("selected_style"),
            unchecked_style=d.get("unchecked_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

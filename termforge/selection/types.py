from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec, StyleSpec
from termforge.text.types import TextAlign

@dataclass
class SelectionItemSpec:
    label: str
    selected: bool = False
    style: StyleSpec | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "selected": self.selected,
            "style": self.style.to_dict() if self.style else None
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SelectionItemSpec:
        return cls(
            label=d["label"],
            selected=d.get("selected", False),
            style=StyleSpec.from_dict(d["style"]) if d.get("style") else None
        )

@dataclass
class SelectionListSpec(RenderableSpec):
    items: list[SelectionItemSpec] = field(default_factory=list)
    focused_index: int = 0
    item_align: TextAlign = TextAlign.LEFT
    item_spacing: int = 0
    spec_type: str = "selection_list"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "items": [item.to_dict() for item in self.items],
            "focused_index": self.focused_index,
            "item_align": self.item_align.value,
            "item_spacing": self.item_spacing
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SelectionListSpec:
        return cls(
            items=[SelectionItemSpec.from_dict(item) for item in d.get("items", [])],
            focused_index=d.get("focused_index", 0),
            item_align=TextAlign(d.get("item_align", "left")),
            item_spacing=d.get("item_spacing", 0)
        )

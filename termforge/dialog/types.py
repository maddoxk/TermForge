from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec, StyleSpec

@dataclass
class DialogSpec(RenderableSpec):
    title: str = ""
    body: str = ""
    buttons: list[str] = field(default_factory=list)
    focused_button_index: int = 0
    spec_type: str = "dialog"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "title": self.title,
            "body": self.body,
            "buttons": self.buttons,
            "focused_button_index": self.focused_button_index
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DialogSpec:
        return cls(
            title=d["title"],
            body=d["body"],
            buttons=d.get("buttons", []),
            focused_button_index=d.get("focused_button_index", 0)
        )

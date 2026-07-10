from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec

@dataclass
class TabSpec(RenderableSpec):
    titles: list[str] = field(default_factory=list)
    active_index: int = 0
    spec_type: str = "tab"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "titles": self.titles,
            "active_index": self.active_index
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TabSpec:
        return cls(
            titles=d.get("titles", []),
            active_index=d.get("active_index", 0)
        )

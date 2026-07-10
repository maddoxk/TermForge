from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec, StyleSpec

@dataclass
class TreeNodeSpec:
    label: str
    expanded: bool = False
    children: list[TreeNodeSpec] = field(default_factory=list)
    style: StyleSpec | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "expanded": self.expanded,
            "children": [c.to_dict() for c in self.children],
            "style": self.style.to_dict() if self.style else None
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TreeNodeSpec:
        return cls(
            label=d["label"],
            expanded=d.get("expanded", False),
            children=[TreeNodeSpec.from_dict(c) for c in d.get("children", [])],
            style=StyleSpec.from_dict(d["style"]) if d.get("style") else None
        )

@dataclass
class TreeSpec(RenderableSpec):
    root_nodes: list[TreeNodeSpec] = field(default_factory=list)
    indent_size: int = 2
    spec_type: str = "tree"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "root_nodes": [n.to_dict() for n in self.root_nodes],
            "indent_size": self.indent_size
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TreeSpec:
        return cls(
            root_nodes=[TreeNodeSpec.from_dict(n) for n in d.get("root_nodes", [])],
            indent_size=d.get("indent_size", 2)
        )

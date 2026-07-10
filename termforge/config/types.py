from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ComponentConfig:
    spec_type: str
    properties: dict[str, Any] = field(default_factory=dict)
    children: list[ComponentConfig] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "properties": self.properties,
            "children": [c.to_dict() for c in self.children]
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ComponentConfig:
        return cls(
            spec_type=d["spec_type"],
            properties=d.get("properties", {}),
            children=[ComponentConfig.from_dict(c) for c in d.get("children", [])]
        )

from termforge.config.input import InputBindingSpec

@dataclass
class LayoutConfig:
    components: list[ComponentConfig] = field(default_factory=list)
    theme: str | None = None
    title: str | None = None
    keybindings: list[InputBindingSpec] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "components": [c.to_dict() for c in self.components],
            "theme": self.theme,
            "title": self.title,
            "keybindings": [k.to_dict() for k in self.keybindings]
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> LayoutConfig:
        return cls(
            components=[ComponentConfig.from_dict(c) for c in d.get("components", [])],
            theme=d.get("theme"),
            title=d.get("title"),
            keybindings=[InputBindingSpec.from_dict(k) for k in d.get("keybindings", [])]
        )

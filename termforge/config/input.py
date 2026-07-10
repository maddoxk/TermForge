from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class InputBindingSpec:
    """Spec mapping a keypress to an action name."""
    key: str
    action: str

    def to_dict(self) -> dict[str, Any]:
        return {"key": self.key, "action": self.action}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> InputBindingSpec:
        return cls(key=d["key"], action=d["action"])

@dataclass
class InputRouter:
    """Utility to route keyboard input to registered action handlers."""
    bindings: list[InputBindingSpec] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"bindings": [b.to_dict() for b in self.bindings]}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> InputRouter:
        return cls(bindings=[InputBindingSpec.from_dict(b) for b in d.get("bindings", [])])

    def route(self, keypress: str) -> str | None:
        """Matches a keypress string to a binding action."""
        kp = keypress.strip().lower()
        for b in self.bindings:
            if b.key.strip().lower() == kp:
                return b.action
        return None

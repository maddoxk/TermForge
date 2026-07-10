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
    buffer: list[str] = field(default_factory=list, init=False)

    def to_dict(self) -> dict[str, Any]:
        return {"bindings": [b.to_dict() for b in self.bindings]}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> InputRouter:
        return cls(bindings=[InputBindingSpec.from_dict(b) for b in d.get("bindings", [])])

    def reset(self) -> None:
        """Clears the keypress sequence buffer."""
        self.buffer.clear()

    def route(self, keypress: str) -> str | None:
        """Matches a keypress string to a binding action, supporting multi-key chords."""
        kp = keypress.strip().lower()
        self.buffer.append(kp)
        
        # Format current buffer sequence
        current_seq = " ".join(self.buffer)
        
        # 1. Check for exact match
        exact_match = None
        for b in self.bindings:
            b_key = " ".join(part.strip().lower() for part in b.key.split())
            if b_key == current_seq:
                exact_match = b.action
                break
                
        # 2. Check if current sequence is a prefix of any binding
        is_prefix = False
        for b in self.bindings:
            b_key = " ".join(part.strip().lower() for part in b.key.split())
            if b_key.startswith(current_seq + " ") or (b_key.startswith(current_seq) and len(b_key.split()) > len(self.buffer)):
                is_prefix = True
                break
                
        if exact_match:
            if is_prefix:
                return None
            else:
                self.buffer.clear()
                return exact_match
                
        if is_prefix:
            return None
            
        # 4. If no match and not a prefix, try to fallback to the last key pressed
        if len(self.buffer) > 1:
            self.buffer = [kp]
            current_seq = kp
            exact_match = None
            for b in self.bindings:
                b_key = " ".join(part.strip().lower() for part in b.key.split())
                if b_key == current_seq:
                    exact_match = b.action
                    break
            is_prefix = False
            for b in self.bindings:
                b_key = " ".join(part.strip().lower() for part in b.key.split())
                if b_key.startswith(current_seq + " ") or (b_key.startswith(current_seq) and len(b_key.split()) > 1):
                    is_prefix = True
                    break
            if exact_match:
                if is_prefix:
                    return None
                else:
                    self.buffer.clear()
                    return exact_match
            if is_prefix:
                return None
                
        self.buffer.clear()
        return None

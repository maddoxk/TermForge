"""TermForge toast component specifications."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class ToastSpec(RenderableSpec):
    """Specification for float pop-up alert notifications (toasts).

    Attributes:
        text: Notification message string.
        toast_type: Severity type ("success", "info", "warning", "error").
        duration_sec: Auto-dismiss timeout duration in seconds.
        position: Layout screen corner ("top-left", "top-right", "bottom-left", "bottom-right").
        border_style: Border style choice ("single", "double", "rounded").
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    text: str = ""
    toast_type: str = "info"
    duration_sec: float = 3.0
    position: str = "top-right"
    border_style: str = "rounded"
    width: int | None = None
    height: int | None = None
    spec_type: str = "toast"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing toast properties.
        """
        return {
            "spec_type": self.spec_type,
            "text": self.text,
            "toast_type": self.toast_type,
            "duration_sec": self.duration_sec,
            "position": self.position,
            "border_style": self.border_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ToastSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing toast properties.

        Returns:
            A new :class:`ToastSpec` instance.
        """
        return cls(
            text=d.get("text", ""),
            toast_type=d.get("toast_type", "info"),
            duration_sec=d.get("duration_sec", 3.0),
            position=d.get("position", "top-right"),
            border_style=d.get("border_style", "rounded"),
            width=d.get("width"),
            height=d.get("height"),
        )

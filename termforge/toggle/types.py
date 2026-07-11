"""TermForge toggle switch component specifications."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class ToggleSwitchSpec(RenderableSpec):
    """Specification for Slider Switch toggle widgets.

    Attributes:
        label: Description text next to the toggle switch.
        state: Active toggle boolean state (True=ON, False=OFF).
        active_indicator: Glyphs representing ON switch position.
        inactive_indicator: Glyphs representing OFF switch position.
        active_label: Custom text label for ON state.
        inactive_label: Custom text label for OFF state.
        active_style: Theme style token for active switch.
        inactive_style: Theme style token for inactive switch.
        label_style: Theme style token for label description text.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    label: str = ""
    state: bool = False
    active_indicator: str = "●"
    inactive_indicator: str = "○"
    active_label: str = "ON"
    inactive_label: str = "OFF"
    active_style: str | None = None
    inactive_style: str | None = None
    label_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "toggle_switch"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing toggle switch properties.
        """
        return {
            "spec_type": self.spec_type,
            "label": self.label,
            "state": self.state,
            "active_indicator": self.active_indicator,
            "inactive_indicator": self.inactive_indicator,
            "active_label": self.active_label,
            "inactive_label": self.inactive_label,
            "active_style": self.active_style,
            "inactive_style": self.inactive_style,
            "label_style": self.label_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ToggleSwitchSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing toggle switch properties.

        Returns:
            A new :class:`ToggleSwitchSpec` instance.
        """
        return cls(
            label=d.get("label", ""),
            state=d.get("state", False),
            active_indicator=d.get("active_indicator", "●"),
            inactive_indicator=d.get("inactive_indicator", "○"),
            active_label=d.get("active_label", "ON"),
            inactive_label=d.get("inactive_label", "OFF"),
            active_style=d.get("active_style"),
            inactive_style=d.get("inactive_style"),
            label_style=d.get("label_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

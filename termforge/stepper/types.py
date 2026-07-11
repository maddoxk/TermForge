"""TermForge stepper component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class StepperSpec(RenderableSpec):
    """Specification for wizard progress stepper indicators.

    Attributes:
        steps: List of step title strings.
        active_idx: Index of currently active step.
        connector: Text connector separator displayed between steps (default " -> ").
        active_style: Theme style token for active step.
        inactive_style: Theme style token for inactive steps.
        connector_style: Theme style token for step connectors.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    steps: list[str] = field(default_factory=list)
    active_idx: int = 0
    connector: str = " -> "
    active_style: str | None = None
    inactive_style: str | None = None
    connector_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "stepper"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing stepper properties.
        """
        return {
            "spec_type": self.spec_type,
            "steps": list(self.steps),
            "active_idx": self.active_idx,
            "connector": self.connector,
            "active_style": self.active_style,
            "inactive_style": self.inactive_style,
            "connector_style": self.connector_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StepperSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing stepper properties.

        Returns:
            A new :class:`StepperSpec` instance.
        """
        return cls(
            steps=list(d.get("steps", [])),
            active_idx=d.get("active_idx", 0),
            connector=d.get("connector", " -> "),
            active_style=d.get("active_style"),
            inactive_style=d.get("inactive_style"),
            connector_style=d.get("connector_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

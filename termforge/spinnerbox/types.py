"""TermForge spinner box component specifications."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class SpinnerBoxSpec(RenderableSpec):
    """Specification for numeric range spinner box widgets.

    Attributes:
        value: Active integer value.
        min_val: Minimum integer limit.
        max_val: Maximum integer limit.
        step: Step size increment.
        label: Description text displayed to the left of the selector.
        left_caret: Character representing decrement option (default "◀").
        right_caret: Character representing increment option (default "▶").
        caret_style: Theme style token for decrement/increment carets.
        value_style: Theme style token for active number value.
        label_style: Theme style token for description label.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    value: int = 5
    min_val: int | None = None
    max_val: int | None = None
    step: int = 1
    label: str = ""
    left_caret: str = "◀"
    right_caret: str = "▶"
    caret_style: str | None = None
    value_style: str | None = None
    label_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "spinner_box"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing spinner box properties.
        """
        return {
            "spec_type": self.spec_type,
            "value": self.value,
            "min_val": self.min_val,
            "max_val": self.max_val,
            "step": self.step,
            "label": self.label,
            "left_caret": self.left_caret,
            "right_caret": self.right_caret,
            "caret_style": self.caret_style,
            "value_style": self.value_style,
            "label_style": self.label_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SpinnerBoxSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing spinner box properties.

        Returns:
            A new :class:`SpinnerBoxSpec` instance.
        """
        return cls(
            value=int(d.get("value", 5)),
            min_val=d.get("min_val"),
            max_val=d.get("max_val"),
            step=int(d.get("step", 1)),
            label=d.get("label", ""),
            left_caret=d.get("left_caret", "◀"),
            right_caret=d.get("right_caret", "▶"),
            caret_style=d.get("caret_style"),
            value_style=d.get("value_style"),
            label_style=d.get("label_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

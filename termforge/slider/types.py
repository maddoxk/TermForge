"""TermForge slider component specifications."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class SliderSpec(RenderableSpec):
    """Specification for numeric range slider widgets.

    Attributes:
        value: Active float value.
        min_val: Minimum range limit (default 0.0).
        max_val: Maximum range limit (default 100.0).
        label: Description text displayed to the left of the track.
        track_fill_char: Character representing progress fill (default "=").
        track_empty_char: Character representing empty track (default "-").
        handle_char: Character representing slider knob knob (default "●").
        value_format: Format string mapping value to text (default "{val}%").
        track_fill_style: Theme style token for progress fill.
        track_empty_style: Theme style token for empty track.
        handle_style: Theme style token for knob handle.
        value_style: Theme style token for value text.
        label_style: Theme style token for description label.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    value: float = 50.0
    min_val: float = 0.0
    max_val: float = 100.0
    label: str = ""
    track_fill_char: str = "="
    track_empty_char: str = "-"
    handle_char: str = "●"
    value_format: str = "{val}%"
    track_fill_style: str | None = None
    track_empty_style: str | None = None
    handle_style: str | None = None
    value_style: str | None = None
    label_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "slider"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing slider properties.
        """
        return {
            "spec_type": self.spec_type,
            "value": self.value,
            "min_val": self.min_val,
            "max_val": self.max_val,
            "label": self.label,
            "track_fill_char": self.track_fill_char,
            "track_empty_char": self.track_empty_char,
            "handle_char": self.handle_char,
            "value_format": self.value_format,
            "track_fill_style": self.track_fill_style,
            "track_empty_style": self.track_empty_style,
            "handle_style": self.handle_style,
            "value_style": self.value_style,
            "label_style": self.label_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SliderSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing slider properties.

        Returns:
            A new :class:`SliderSpec` instance.
        """
        return cls(
            value=float(d.get("value", 50.0)),
            min_val=float(d.get("min_val", 0.0)),
            max_val=float(d.get("max_val", 100.0)),
            label=d.get("label", ""),
            track_fill_char=d.get("track_fill_char", "="),
            track_empty_char=d.get("track_empty_char", "-"),
            handle_char=d.get("handle_char", "●"),
            value_format=d.get("value_format", "{val}%"),
            track_fill_style=d.get("track_fill_style"),
            track_empty_style=d.get("track_empty_style"),
            handle_style=d.get("handle_style"),
            value_style=d.get("value_style"),
            label_style=d.get("label_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

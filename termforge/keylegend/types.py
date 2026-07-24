"""TermForge keybinding shortcut legend component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING
from termforge.core.types import RenderableSpec

if TYPE_CHECKING:
    from termforge.config.input import InputBindingSpec



@dataclass
class KeyLegendSpec(RenderableSpec):
    """Specification for a keybinding shortcut legend component.

    Attributes:
        bindings: List of key-to-action bindings.
        format: Template string containing ``{key}`` and ``{description}`` slots.
        spacing: Number of spaces separating legend items when laid out.
        key_style: Style token for key names (e.g. "colors.primary").
        desc_style: Style token for action descriptions (e.g. "colors.secondary").
        orientation: Render orientation, either "horizontal" or "vertical".
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    bindings: list[InputBindingSpec] = field(default_factory=list)
    format: str = "[{key}] {description}"
    spacing: int = 4
    key_style: str | None = None
    desc_style: str | None = None
    orientation: str = "horizontal"
    width: int | None = None
    height: int | None = None
    spec_type: str = "key_legend"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing key legend properties.
        """
        return {
            "spec_type": self.spec_type,
            "bindings": [b.to_dict() for b in self.bindings],
            "format": self.format,
            "spacing": self.spacing,
            "key_style": self.key_style,
            "desc_style": self.desc_style,
            "orientation": self.orientation,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> KeyLegendSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing key legend properties.

        Returns:
            A new :class:`KeyLegendSpec` instance.
        """
        from termforge.config.input import InputBindingSpec
        return cls(
            bindings=[InputBindingSpec.from_dict(b) for b in d.get("bindings", [])],
            format=d.get("format", "[{key}] {description}"),
            spacing=d.get("spacing", 4),
            key_style=d.get("key_style"),
            desc_style=d.get("desc_style"),
            orientation=d.get("orientation", "horizontal"),
            width=d.get("width"),
            height=d.get("height"),
        )

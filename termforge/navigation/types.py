"""TermForge navigation breadcrumbs component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class BreadcrumbsSpec(RenderableSpec):
    """Specification for path trail/breadcrumbs navigation component.

    Attributes:
        items: List of navigation path segment strings (e.g. ["Root", "Config"]).
        delimiter: Separator string placed between items (default " › ").
        item_style: Theme style token for intermediate items (e.g. "colors.secondary").
        delimiter_style: Theme style token for delimiters.
        active_item_style: Theme style token for the last active item (e.g. "colors.primary").
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    items: list[str] = field(default_factory=list)
    delimiter: str = " › "
    item_style: str | None = None
    delimiter_style: str | None = None
    active_item_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "breadcrumbs"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing breadcrumbs properties.
        """
        return {
            "spec_type": self.spec_type,
            "items": list(self.items),
            "delimiter": self.delimiter,
            "item_style": self.item_style,
            "delimiter_style": self.delimiter_style,
            "active_item_style": self.active_item_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BreadcrumbsSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing breadcrumbs properties.

        Returns:
            A new :class:`BreadcrumbsSpec` instance.
        """
        return cls(
            items=list(d.get("items", [])),
            delimiter=d.get("delimiter", " › "),
            item_style=d.get("item_style"),
            delimiter_style=d.get("delimiter_style"),
            active_item_style=d.get("active_item_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

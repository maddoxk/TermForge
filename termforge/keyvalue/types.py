"""TermForge key-value grid component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class KeyValueItemSpec(RenderableSpec):
    """Specification for a single key-value row.

    Attributes:
        key: The row header/key label.
        value: The value string.
        key_style: Optional theme style token for the key.
        value_style: Optional theme style token for the value.
    """
    key: str = ""
    value: str = ""
    key_style: str | None = None
    value_style: str | None = None
    spec_type: str = "keyvalue_item"


    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing item properties.
        """
        return {
            "spec_type": self.spec_type,
            "key": self.key,
            "value": self.value,
            "key_style": self.key_style,
            "value_style": self.value_style,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> KeyValueItemSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing item properties.

        Returns:
            A new :class:`KeyValueItemSpec` instance.
        """
        return cls(
            key=d["key"],
            value=d["value"],
            key_style=d.get("key_style"),
            value_style=d.get("value_style"),
        )


@dataclass
class KeyValueGridSpec(RenderableSpec):
    """Specification for a grid containing aligned key-value listings.

    Attributes:
        items: List of KeyValueItemSpec rows.
        separator: Separator characters between keys and values.
        key_width: Optional fixed width for the key column. If None,
            the key column is dynamically sized to fit the longest key.
        width: Optional fixed overall width.
        height: Optional fixed overall height.
    """
    items: list[KeyValueItemSpec] = field(default_factory=list)
    separator: str = ": "
    key_width: int | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "keyvalue_grid"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing grid properties.
        """
        return {
            "spec_type": self.spec_type,
            "items": [item.to_dict() for item in self.items],
            "separator": self.separator,
            "key_width": self.key_width,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> KeyValueGridSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing grid properties.

        Returns:
            A new :class:`KeyValueGridSpec` instance.
        """
        return cls(
            items=[KeyValueItemSpec.from_dict(item) for item in d.get("items", [])],
            separator=d.get("separator", ": "),
            key_width=d.get("key_width"),
            width=d.get("width"),
            height=d.get("height"),
        )

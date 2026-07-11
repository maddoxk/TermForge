"""TermForge accordion component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class AccordionItemSpec:
    """An individual collapse/expand option section item.

    Attributes:
        title: Title of the accordion section.
        details: Multiline description details text shown when expanded.
        is_expanded: Boolean flag representing whether the section details are visible.
    """
    title: str
    details: str = ""
    is_expanded: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "details": self.details,
            "is_expanded": self.is_expanded,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> AccordionItemSpec:
        return cls(
            title=d.get("title", ""),
            details=d.get("details", ""),
            is_expanded=d.get("is_expanded", False),
        )


@dataclass
class AccordionSpec(RenderableSpec):
    """Specification for Accordion details list elements.

    Attributes:
        items: List of AccordionItemSpec elements.
        selected_idx: Focused option section index under cursor.
        collapsed_caret: Caret prefix text showing collapsed status (default "> ").
        expanded_caret: Caret prefix text showing expanded status (default "v ").
        active_style: Theme style token for expanded header items.
        selected_style: Theme style token for focused option choice.
        inactive_style: Theme style token for collapsed normal items.
        details_style: Theme style token for expanded details descriptions.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    items: list[AccordionItemSpec] = field(default_factory=list)
    selected_idx: int = 0
    collapsed_caret: str = "> "
    expanded_caret: str = "v "
    active_style: str | None = None
    selected_style: str | None = None
    inactive_style: str | None = None
    details_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "accordion"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing accordion properties.
        """
        return {
            "spec_type": self.spec_type,
            "items": [item.to_dict() for item in self.items],
            "selected_idx": self.selected_idx,
            "collapsed_caret": self.collapsed_caret,
            "expanded_caret": self.expanded_caret,
            "active_style": self.active_style,
            "selected_style": self.selected_style,
            "inactive_style": self.inactive_style,
            "details_style": self.details_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> AccordionSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing accordion properties.

        Returns:
            A new :class:`AccordionSpec` instance.
        """
        return cls(
            items=[AccordionItemSpec.from_dict(item) for item in d.get("items", [])],
            selected_idx=d.get("selected_idx", 0),
            collapsed_caret=d.get("collapsed_caret", "> "),
            expanded_caret=d.get("expanded_caret", "v "),
            active_style=d.get("active_style"),
            selected_style=d.get("selected_style"),
            inactive_style=d.get("inactive_style"),
            details_style=d.get("details_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

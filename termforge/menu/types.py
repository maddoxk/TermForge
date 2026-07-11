"""TermForge status menu bar component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class MenuItemSpec:
    """A top-level menu button containing sub-actions.

    Attributes:
        label: Top-level label string (e.g. "File").
        children: Sub-items list (e.g. ["New", "Open", "-", "Exit"]).
    """
    label: str
    children: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "children": list(self.children),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> MenuItemSpec:
        return cls(
            label=d.get("label", ""),
            children=list(d.get("children", [])),
        )


@dataclass
class MenuBarSpec(RenderableSpec):
    """Specification for horizontal status menu bar layout with dropdown overlays.

    Attributes:
        menus: List of MenuItemSpec options.
        selected_idx: Index of currently focused top-level menu.
        active_menu_idx: Index of open dropdown column, or None if closed.
        selected_child_idx: Index of focused dropdown action.
        spacing: Character spacing between top-level menu labels.
        menu_style: Theme style token for standard menus.
        selected_style: Theme style token for selected menu buttons.
        dropdown_style: Theme style for standard dropdown sub-items.
        dropdown_selected_style: Theme style for selected sub-items.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    menus: list[MenuItemSpec] = field(default_factory=list)
    selected_idx: int = 0
    active_menu_idx: int | None = None
    selected_child_idx: int = 0
    spacing: int = 4
    menu_style: str | None = None
    selected_style: str | None = None
    dropdown_style: str | None = None
    dropdown_selected_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "menu_bar"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing menu bar properties.
        """
        return {
            "spec_type": self.spec_type,
            "menus": [m.to_dict() for m in self.menus],
            "selected_idx": self.selected_idx,
            "active_menu_idx": self.active_menu_idx,
            "selected_child_idx": self.selected_child_idx,
            "spacing": self.spacing,
            "menu_style": self.menu_style,
            "selected_style": self.selected_style,
            "dropdown_style": self.dropdown_style,
            "dropdown_selected_style": self.dropdown_selected_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> MenuBarSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing menu bar properties.

        Returns:
            A new :class:`MenuBarSpec` instance.
        """
        return cls(
            menus=[MenuItemSpec.from_dict(m) for m in d.get("menus", [])],
            selected_idx=d.get("selected_idx", 0),
            active_menu_idx=d.get("active_menu_idx"),
            selected_child_idx=d.get("selected_child_idx", 0),
            spacing=d.get("spacing", 4),
            menu_style=d.get("menu_style"),
            selected_style=d.get("selected_style"),
            dropdown_style=d.get("dropdown_style"),
            dropdown_selected_style=d.get("dropdown_selected_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

"""TermForge search input and filter bar component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class SearchBarSpec(RenderableSpec):
    """Specification for query search bar with matching substring highlights.

    Attributes:
        query: Active search input query text.
        candidates: List of strings to filter.
        placeholder: Text displayed when query is empty.
        match_style: Theme style token for matching highlights (e.g. "colors.warning").
        input_style: Theme style token for query input text.
        placeholder_style: Theme style token for placeholder text.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    query: str = ""
    candidates: list[str] = field(default_factory=list)
    placeholder: str = "Search..."
    match_style: str | None = None
    input_style: str | None = None
    placeholder_style: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "search_bar"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing search bar properties.
        """
        return {
            "spec_type": self.spec_type,
            "query": self.query,
            "candidates": list(self.candidates),
            "placeholder": self.placeholder,
            "match_style": self.match_style,
            "input_style": self.input_style,
            "placeholder_style": self.placeholder_style,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SearchBarSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing search bar properties.

        Returns:
            A new :class:`SearchBarSpec` instance.
        """
        return cls(
            query=d.get("query", ""),
            candidates=list(d.get("candidates", [])),
            placeholder=d.get("placeholder", "Search..."),
            match_style=d.get("match_style"),
            input_style=d.get("input_style"),
            placeholder_style=d.get("placeholder_style"),
            width=d.get("width"),
            height=d.get("height"),
        )

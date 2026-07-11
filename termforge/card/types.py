"""TermForge card component specifications."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class CardSpec(RenderableSpec):
    """Specification for bordered card layout elements.

    Attributes:
        title: Title string shown in top border.
        subtitle: Subtitle string shown next to title in top border.
        content: Multiline body content string.
        border_style: Border style category name (default "single").
        title_style: Theme style token for title.
        subtitle_style: Theme style token for subtitle.
        content_style: Theme style token for body content.
        border_style_token: Theme style token for card borders.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    title: str = ""
    subtitle: str = ""
    content: str = ""
    border_style: str = "single"
    title_style: str | None = None
    subtitle_style: str | None = None
    content_style: str | None = None
    border_style_token: str | None = None
    width: int | None = None
    height: int | None = None
    spec_type: str = "card"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing card properties.
        """
        return {
            "spec_type": self.spec_type,
            "title": self.title,
            "subtitle": self.subtitle,
            "content": self.content,
            "border_style": self.border_style,
            "title_style": self.title_style,
            "subtitle_style": self.subtitle_style,
            "content_style": self.content_style,
            "border_style_token": self.border_style_token,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> CardSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing card properties.

        Returns:
            A new :class:`CardSpec` instance.
        """
        return cls(
            title=d.get("title", ""),
            subtitle=d.get("subtitle", ""),
            content=d.get("content", ""),
            border_style=d.get("border_style", "single"),
            title_style=d.get("title_style"),
            subtitle_style=d.get("subtitle_style"),
            content_style=d.get("content_style"),
            border_style_token=d.get("border_style_token"),
            width=d.get("width"),
            height=d.get("height"),
        )

"""TermForge badge component specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class BadgeSpec(RenderableSpec):
    """Specification for colored status label badge elements.

    Attributes:
        text: Badge label string content.
        severity: Severity classification level ("info", "success", "warning", "error").
        brackets: Bracket formatting style ("( )", "{ }", "[ ]").
        text_style: Optional theme style token for label text override.
        severity_styles: Custom mapping of severity names to theme style tokens.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    text: str = ""
    severity: str = "info"
    brackets: str = "[ ]"
    text_style: str | None = None
    severity_styles: dict[str, str] = field(default_factory=dict)
    width: int | None = None
    height: int | None = None
    spec_type: str = "badge"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing badge properties.
        """
        return {
            "spec_type": self.spec_type,
            "text": self.text,
            "severity": self.severity,
            "brackets": self.brackets,
            "text_style": self.text_style,
            "severity_styles": dict(self.severity_styles),
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BadgeSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing badge properties.

        Returns:
            A new :class:`BadgeSpec` instance.
        """
        return cls(
            text=d.get("text", ""),
            severity=d.get("severity", "info"),
            brackets=d.get("brackets", "[ ]"),
            text_style=d.get("text_style"),
            severity_styles=dict(d.get("severity_styles", {})),
            width=d.get("width"),
            height=d.get("height"),
        )

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec, StyleSpec

@dataclass
class LogoSpec(RenderableSpec):
    text: str = "TermForge"
    font: str = "standard"
    color_token: str = "primary"
    gradient: list[str] | None = None
    spec_type: str = "logo"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "text": self.text,
            "font": self.font,
            "color_token": self.color_token,
            "gradient": self.gradient
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> LogoSpec:
        return cls(
            text=d.get("text", "TermForge"),
            font=d.get("font", "standard"),
            color_token=d.get("color_token", "primary"),
            gradient=d.get("gradient")
        )

@dataclass
class BannerSpec(RenderableSpec):
    text: str = ""
    font: str = "slant"
    style: StyleSpec | None = None
    spec_type: str = "banner"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "text": self.text,
            "font": self.font,
            "style": self.style.to_dict() if self.style else None
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BannerSpec:
        style_dict = d.get("style")
        style = StyleSpec.from_dict(style_dict) if style_dict else None
        return cls(
            text=d.get("text", ""),
            font=d.get("font", "slant"),
            style=style
        )

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any
from termforge.core.types import RenderableSpec

class ImageFidelity(str, Enum):
    HALF_BLOCK = "half_block"
    ASCII_RAMP = "ascii_ramp"

@dataclass
class ImageSpec(RenderableSpec):
    source: str = ""
    width: int | None = None
    height: int | None = None
    fidelity: ImageFidelity | None = None
    preserve_aspect: bool = True
    spec_type: str = "image"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "source": self.source,
            "width": self.width,
            "height": self.height,
            "fidelity": self.fidelity.value if self.fidelity else None,
            "preserve_aspect": self.preserve_aspect
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ImageSpec:
        fid = d.get("fidelity")
        fidelity = ImageFidelity(fid) if fid else None
        return cls(
            source=d.get("source", ""),
            width=d.get("width"),
            height=d.get("height"),
            fidelity=fidelity,
            preserve_aspect=d.get("preserve_aspect", True)
        )

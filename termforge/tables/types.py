from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec, StyleSpec
from termforge.text.types import TextAlign

@dataclass
class ColumnSpec:
    title: str
    width: int | None = None
    align: TextAlign = TextAlign.LEFT
    style: StyleSpec | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "width": self.width,
            "align": self.align.value,
            "style": self.style.to_dict() if self.style else None
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ColumnSpec:
        return cls(
            title=d["title"],
            width=d.get("width"),
            align=TextAlign(d.get("align", "left")),
            style=StyleSpec.from_dict(d["style"]) if d.get("style") else None
        )

@dataclass
class TableSpec(RenderableSpec):
    columns: list[ColumnSpec] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    header_style: StyleSpec | None = None
    row_style: StyleSpec | None = None
    alt_row_style: StyleSpec | None = None
    spec_type: str = "table"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "columns": [c.to_dict() for c in self.columns],
            "rows": self.rows,
            "header_style": self.header_style.to_dict() if self.header_style else None,
            "row_style": self.row_style.to_dict() if self.row_style else None,
            "alt_row_style": self.alt_row_style.to_dict() if self.alt_row_style else None
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TableSpec:
        return cls(
            columns=[ColumnSpec.from_dict(c) for c in d.get("columns", [])],
            rows=d.get("rows", []),
            header_style=StyleSpec.from_dict(d["header_style"]) if d.get("header_style") else None,
            row_style=StyleSpec.from_dict(d["row_style"]) if d.get("row_style") else None,
            alt_row_style=StyleSpec.from_dict(d["alt_row_style"]) if d.get("alt_row_style") else None
        )

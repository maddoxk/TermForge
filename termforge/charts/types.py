from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from termforge.core.types import RenderableSpec

class ChartType(str, Enum):
    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    STACKED_BAR = "stacked_bar"
    MULTI_BAR = "multi_bar"
    HEATMAP = "heatmap"
    SPARKLINE = "sparkline"
    CANDLESTICK = "candlestick"

@dataclass
class Axis:
    label: str | None = None
    min_val: float | None = None
    max_val: float | None = None
    tick_count: int = 5
    format_str: str = "{:.1f}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "min_val": self.min_val,
            "max_val": self.max_val,
            "tick_count": self.tick_count,
            "format_str": self.format_str
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Axis:
        return cls(
            label=d.get("label"),
            min_val=d.get("min_val"),
            max_val=d.get("max_val"),
            tick_count=d.get("tick_count", 5),
            format_str=d.get("format_str", "{:.1f}")
        )

@dataclass
class Series:
    name: str = "series"
    data: list[float] = field(default_factory=list)
    color_token: str = "primary"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "data": self.data,
            "color_token": self.color_token
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Series:
        return cls(
            name=d.get("name", "series"),
            data=d.get("data", []),
            color_token=d.get("color_token", "primary")
        )

@dataclass
class OHLCSeries:
    name: str = "ohlc"
    # data is a list of dicts: {"open": float, "high": float, "low": float, "close": float, "volume": float}
    data: list[dict[str, float]] = field(default_factory=list)
    timestamps: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "data": self.data,
            "timestamps": self.timestamps
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> OHLCSeries:
        return cls(
            name=d.get("name", "ohlc"),
            data=d.get("data", []),
            timestamps=d.get("timestamps")
        )

@dataclass
class ChartSpec(RenderableSpec):
    chart_type: ChartType = ChartType.LINE
    series: list[Series] = field(default_factory=list)
    ohlc_series: OHLCSeries | list[OHLCSeries] | None = None
    x_axis: Axis = field(default_factory=Axis)
    y_axis: Axis = field(default_factory=Axis)
    width: int = 80
    height: int = 24
    title: str | None = None
    show_legend: bool = True
    braille: bool = False
    color_config: dict[str, Any] | None = None
    highlight_max: bool = False
    highlight_min: bool = False
    spec_type: str = "chart"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "chart_type": self.chart_type.value,
            "series": [s.to_dict() for s in self.series],
            "ohlc_series": self.ohlc_series.to_dict() if self.ohlc_series else None,
            "x_axis": self.x_axis.to_dict(),
            "y_axis": self.y_axis.to_dict(),
            "width": self.width,
            "height": self.height,
            "title": self.title,
            "show_legend": self.show_legend,
            "braille": self.braille,
            "color_config": self.color_config,
            "highlight_max": self.highlight_max,
            "highlight_min": self.highlight_min
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ChartSpec:
        series_data = [Series.from_dict(s) for s in d.get("series", [])]
        ohlc_data = d.get("ohlc_series")
        ohlc_series = OHLCSeries.from_dict(ohlc_data) if ohlc_data else None
        
        return cls(
            chart_type=ChartType(d.get("chart_type", "line")),
            series=series_data,
            ohlc_series=ohlc_series,
            x_axis=Axis.from_dict(d.get("x_axis", {})),
            y_axis=Axis.from_dict(d.get("y_axis", {})),
            width=d.get("width", 80),
            height=d.get("height", 24),
            title=d.get("title"),
            show_legend=d.get("show_legend", True),
            braille=d.get("braille", False),
            color_config=d.get("color_config"),
            highlight_max=d.get("highlight_max", False),
            highlight_min=d.get("highlight_min", False)
        )

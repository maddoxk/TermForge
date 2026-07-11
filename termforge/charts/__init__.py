"""TermForge charts module — line, bar, scatter, histogram, sparkline, candlestick."""
from termforge.charts.types import ChartType, Axis, Series, OHLCSeries, ChartSpec
from termforge.charts.scale import nice_bounds, compute_bounds, scale_value, generate_ticks
from termforge.charts.canvas import Canvas, BrailleCanvas, create_canvas, create_braille_canvas
from termforge.charts.chart import render_chart
from termforge.charts.renderers import render_sparkline
from termforge.charts.streaming import StreamingChartBuffer

__all__ = [
    "ChartType",
    "Axis",
    "Series",
    "OHLCSeries",
    "ChartSpec",
    "nice_bounds",
    "compute_bounds",
    "scale_value",
    "generate_ticks",
    "Canvas",
    "BrailleCanvas",
    "create_canvas",
    "create_braille_canvas",
    "render_chart",
    "render_sparkline",
    "StreamingChartBuffer",
]

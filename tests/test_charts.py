import pytest
from termforge.core.types import ColorDepth
from termforge.charts.types import ChartSpec, ChartType, Axis, Series, OHLCSeries
from termforge.charts.scale import nice_bounds, scale_value, compute_bounds, generate_ticks
from termforge.charts.canvas import create_canvas, draw_line
from termforge.charts.chart import render_chart

def test_chart_spec_serialization():
    spec = ChartSpec(
        chart_type=ChartType.LINE,
        series=[Series(name="sales", data=[10.0, 20.0, 15.0])],
        width=60,
        height=15
    )
    spec_dict = spec.to_dict()
    assert spec_dict["spec_type"] == "chart"
    assert spec_dict["chart_type"] == "line"
    assert len(spec_dict["series"]) == 1
    assert spec_dict["width"] == 60
    assert spec_dict["height"] == 15
    
    spec_back = ChartSpec.from_dict(spec_dict)
    assert spec_back.chart_type == ChartType.LINE
    assert len(spec_back.series) == 1
    assert spec_back.series[0].name == "sales"
    assert spec_back.width == 60
    assert spec_back.height == 15

def test_nice_bounds():
    assert nice_bounds(0.0, 10.0) == (0.0, 10.0)
    assert nice_bounds(1.2, 8.9) == (1.0, 9.0)
    assert nice_bounds(5.0, 5.0) == (4.0, 6.0)

def test_scale_value():
    assert scale_value(5.0, 0.0, 10.0, 11) == 5
    assert scale_value(0.0, 0.0, 10.0, 11) == 0
    assert scale_value(10.0, 0.0, 10.0, 11) == 10

def test_canvas_drawing():
    canvas = create_canvas(10, 10)
    draw_line(canvas, 0, 0, 9, 9, "*")
    # check that cells are drawn
    assert canvas.cells[0][9] == "*" # top-right in rows (row 0, col 9)
    assert canvas.cells[9][0] == "*" # bottom-left in rows (row 9, col 0)

def test_sparkline():
    spec = ChartSpec(
        chart_type=ChartType.SPARKLINE,
        series=[Series(data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])]
    )
    lines = render_chart(spec)
    assert len(lines) == 1
    assert lines[0] == " ▂▃▄▅▆▇█"

def test_line_chart_rendering():
    spec = ChartSpec(
        chart_type=ChartType.LINE,
        series=[Series(data=[10.0, 20.0, 15.0])],
        width=40,
        height=10
    )
    lines = render_chart(spec)
    assert len(lines) == 10 # height=10
    for line in lines:
        assert len(line) >= 40 # width=40 (plus ANSI codes)

def test_candlestick_rendering():
    ohlc = OHLCSeries(data=[
        {"open": 10.0, "high": 15.0, "low": 8.0, "close": 12.0},
        {"open": 12.0, "high": 18.0, "low": 11.0, "close": 9.0},
        {"open": 9.0, "high": 14.0, "low": 7.0, "close": 13.0}
    ])
    spec = ChartSpec(
        chart_type=ChartType.CANDLESTICK,
        ohlc_series=ohlc,
        width=40,
        height=10
    )
    lines = render_chart(spec)
    assert len(lines) == 10

"""Tests for Issue #142: Chart Data Streaming API — StreamingChartBuffer."""
import json
import pytest
from termforge.charts.streaming import StreamingChartBuffer, _auto_range
from termforge.charts.types import ChartType, ChartSpec, OHLCSeries, Series


# ---------------------------------------------------------------------------
# _auto_range helper
# ---------------------------------------------------------------------------

def test_auto_range_normal():
    lo, hi = _auto_range([0.0, 10.0])
    assert lo < 0.0   # padding below
    assert hi > 10.0  # padding above


def test_auto_range_empty():
    lo, hi = _auto_range([])
    assert lo == 0.0
    assert hi == 1.0


def test_auto_range_constant():
    lo, hi = _auto_range([5.0, 5.0, 5.0])
    assert lo < 5.0
    assert hi > 5.0


def test_auto_range_zero_padding():
    lo, hi = _auto_range([2.0, 8.0], y_padding=0.0)
    assert lo == 2.0
    assert hi == 8.0


# ---------------------------------------------------------------------------
# StreamingChartBuffer — basic construction
# ---------------------------------------------------------------------------

def test_default_construction():
    buf = StreamingChartBuffer()
    assert buf.max_points == 120
    assert buf.series_count == 1
    assert buf.point_count == 0
    assert not buf.is_full
    assert not buf.ohlc


def test_multi_series_construction():
    buf = StreamingChartBuffer(series_count=3, series_names=["A", "B", "C"])
    assert len(buf._data) == 3
    assert buf.series_names == ["A", "B", "C"]


def test_auto_name_padding():
    buf = StreamingChartBuffer(series_count=3)
    assert len(buf.series_names) == 3
    assert all(n.startswith("series") for n in buf.series_names)


def test_auto_color_padding():
    buf = StreamingChartBuffer(series_count=3)
    assert len(buf.series_colors) == 3


# ---------------------------------------------------------------------------
# push()
# ---------------------------------------------------------------------------

def test_push_single_series():
    buf = StreamingChartBuffer(max_points=5)
    buf.push([1.0])
    assert buf.point_count == 1


def test_push_multi_series():
    buf = StreamingChartBuffer(series_count=2)
    buf.push([10.0, 20.0])
    assert buf.point_count == 1
    assert list(buf._data[0]) == [10.0]
    assert list(buf._data[1]) == [20.0]


def test_push_rolling_window():
    buf = StreamingChartBuffer(max_points=3)
    for v in [1.0, 2.0, 3.0, 4.0, 5.0]:
        buf.push([v])
    # Only last 3 kept
    assert buf.point_count == 3
    assert list(buf._data[0]) == [3.0, 4.0, 5.0]
    assert buf.is_full


def test_push_short_values_padded_with_zero():
    buf = StreamingChartBuffer(series_count=3)
    buf.push([7.0])   # only 1 value for 3 series
    assert list(buf._data[1]) == [0.0]
    assert list(buf._data[2]) == [0.0]


def test_push_raises_on_ohlc_buffer():
    buf = StreamingChartBuffer(ohlc=True)
    with pytest.raises(ValueError, match="push_ohlc"):
        buf.push([1.0])


# ---------------------------------------------------------------------------
# push_ohlc()
# ---------------------------------------------------------------------------

def test_push_ohlc_basic():
    buf = StreamingChartBuffer(ohlc=True)
    buf.push_ohlc(open=100, high=105, low=98, close=103)
    assert buf.point_count == 1
    assert list(buf._ohlc)[0]["open"] == 100.0


def test_push_ohlc_with_timestamp():
    buf = StreamingChartBuffer(ohlc=True)
    buf.push_ohlc(open=1, high=2, low=0.5, close=1.5, timestamp="2026-01-01")
    bar = list(buf._ohlc)[0]
    assert bar["timestamp"] == "2026-01-01"


def test_push_ohlc_rolling_window():
    buf = StreamingChartBuffer(max_points=2, ohlc=True)
    for i in range(5):
        buf.push_ohlc(open=i, high=i+1, low=i-0.5, close=i+0.5)
    assert buf.point_count == 2
    assert buf.is_full


def test_push_ohlc_raises_on_series_buffer():
    buf = StreamingChartBuffer()
    with pytest.raises(ValueError, match="push"):
        buf.push_ohlc(open=1, high=2, low=0.5, close=1.5)


# ---------------------------------------------------------------------------
# to_chart_spec() — series mode
# ---------------------------------------------------------------------------

def test_to_chart_spec_returns_chart_spec():
    buf = StreamingChartBuffer(series_count=2)
    buf.push([10.0, 20.0])
    spec = buf.to_chart_spec()
    assert isinstance(spec, ChartSpec)


def test_to_chart_spec_series_count():
    buf = StreamingChartBuffer(series_count=2, series_names=["CPU", "Mem"])
    buf.push([50.0, 70.0])
    spec = buf.to_chart_spec()
    assert len(spec.series) == 2
    assert spec.series[0].name == "CPU"
    assert spec.series[1].name == "Mem"


def test_to_chart_spec_data_snapshot():
    buf = StreamingChartBuffer(max_points=5)
    for v in [1.0, 2.0, 3.0]:
        buf.push([v])
    spec = buf.to_chart_spec()
    assert spec.series[0].data == [1.0, 2.0, 3.0]


def test_to_chart_spec_auto_y_bounds():
    buf = StreamingChartBuffer()
    buf.push([10.0])
    buf.push([20.0])
    spec = buf.to_chart_spec()
    assert spec.y_axis.min_val is not None
    assert spec.y_axis.max_val is not None
    assert spec.y_axis.min_val < 10.0
    assert spec.y_axis.max_val > 20.0


def test_to_chart_spec_y_override():
    buf = StreamingChartBuffer()
    buf.push([50.0])
    spec = buf.to_chart_spec(y_min=0.0, y_max=100.0)
    assert spec.y_axis.min_val == 0.0
    assert spec.y_axis.max_val == 100.0


def test_to_chart_spec_chart_type():
    buf = StreamingChartBuffer()
    buf.push([5.0])
    spec = buf.to_chart_spec(chart_type=ChartType.BAR)
    assert spec.chart_type == ChartType.BAR


def test_to_chart_spec_title_and_dimensions():
    buf = StreamingChartBuffer()
    buf.push([1.0])
    spec = buf.to_chart_spec(title="Metrics", width=60, height=15)
    assert spec.title == "Metrics"
    assert spec.width == 60
    assert spec.height == 15


# ---------------------------------------------------------------------------
# to_chart_spec() — OHLC mode
# ---------------------------------------------------------------------------

def test_to_chart_spec_ohlc_mode():
    buf = StreamingChartBuffer(ohlc=True)
    buf.push_ohlc(100, 105, 98, 103)
    buf.push_ohlc(103, 108, 101, 107)
    spec = buf.to_chart_spec(chart_type=ChartType.CANDLESTICK)
    assert spec.ohlc_series is not None
    assert isinstance(spec.ohlc_series, OHLCSeries)
    assert len(spec.ohlc_series.data) == 2


def test_to_chart_spec_ohlc_y_bounds():
    buf = StreamingChartBuffer(ohlc=True)
    buf.push_ohlc(100, 110, 90, 105)
    spec = buf.to_chart_spec(chart_type=ChartType.CANDLESTICK)
    assert spec.y_axis.min_val < 90.0
    assert spec.y_axis.max_val > 110.0


def test_to_chart_spec_ohlc_timestamps():
    buf = StreamingChartBuffer(ohlc=True)
    buf.push_ohlc(1, 2, 0.5, 1.5, timestamp="T1")
    buf.push_ohlc(2, 3, 1.5, 2.5, timestamp="T2")
    spec = buf.to_chart_spec(chart_type=ChartType.CANDLESTICK)
    assert spec.ohlc_series.timestamps == ["T1", "T2"]


# ---------------------------------------------------------------------------
# latest() / latest_ohlc()
# ---------------------------------------------------------------------------

def test_latest_single():
    buf = StreamingChartBuffer(series_count=2)
    buf.push([1.0, 10.0])
    buf.push([2.0, 20.0])
    rows = buf.latest(1)
    assert rows == [[2.0, 20.0]]


def test_latest_multiple():
    buf = StreamingChartBuffer()
    for v in [1.0, 2.0, 3.0, 4.0]:
        buf.push([v])
    rows = buf.latest(2)
    assert rows == [[3.0], [4.0]]


def test_latest_raises_on_ohlc():
    buf = StreamingChartBuffer(ohlc=True)
    with pytest.raises(ValueError):
        buf.latest()


def test_latest_ohlc():
    buf = StreamingChartBuffer(ohlc=True)
    buf.push_ohlc(1, 2, 0.5, 1.5)
    buf.push_ohlc(2, 3, 1.5, 2.5)
    bars = buf.latest_ohlc(1)
    assert len(bars) == 1
    assert bars[0]["close"] == 2.5


# ---------------------------------------------------------------------------
# clear()
# ---------------------------------------------------------------------------

def test_clear_series():
    buf = StreamingChartBuffer()
    buf.push([1.0])
    buf.clear()
    assert buf.point_count == 0


def test_clear_ohlc():
    buf = StreamingChartBuffer(ohlc=True)
    buf.push_ohlc(1, 2, 0.5, 1.5)
    buf.clear()
    assert buf.point_count == 0


# ---------------------------------------------------------------------------
# Portability contract — JSON round-trip
# ---------------------------------------------------------------------------

def test_series_buffer_json_roundtrip():
    buf = StreamingChartBuffer(
        max_points=10, series_count=2,
        series_names=["A", "B"], series_colors=["primary", "secondary"]
    )
    buf.push([1.0, 100.0])
    buf.push([2.0, 200.0])

    d = buf.to_dict()
    json_str = json.dumps(d)
    d2 = json.loads(json_str)
    buf2 = StreamingChartBuffer.from_dict(d2)

    assert buf2.max_points == 10
    assert buf2.series_count == 2
    assert buf2.series_names == ["A", "B"]
    assert buf2.point_count == 2
    assert list(buf2._data[0]) == [1.0, 2.0]
    assert list(buf2._data[1]) == [100.0, 200.0]


def test_ohlc_buffer_json_roundtrip():
    buf = StreamingChartBuffer(max_points=5, ohlc=True, ohlc_name="BTC")
    buf.push_ohlc(100, 105, 98, 103, timestamp="2026-01-01")
    buf.push_ohlc(103, 108, 101, 107)

    d = buf.to_dict()
    json_str = json.dumps(d)
    d2 = json.loads(json_str)
    buf2 = StreamingChartBuffer.from_dict(d2)

    assert buf2.ohlc
    assert buf2.ohlc_name == "BTC"
    assert buf2.point_count == 2
    assert list(buf2._ohlc)[0]["open"] == 100.0
    assert list(buf2._ohlc)[0]["timestamp"] == "2026-01-01"


def test_to_chart_spec_portability():
    """ChartSpec produced by to_chart_spec() must itself be JSON-serializable."""
    buf = StreamingChartBuffer(series_count=2)
    for i in range(5):
        buf.push([float(i), float(i * 2)])
    spec = buf.to_chart_spec(title="Portability", width=60, height=15)
    d = spec.to_dict()
    json_str = json.dumps(d)
    d2 = json.loads(json_str)
    spec2 = ChartSpec.from_dict(d2)
    assert spec2.title == "Portability"
    assert len(spec2.series) == 2

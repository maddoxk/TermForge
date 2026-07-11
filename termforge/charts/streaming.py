"""TermForge chart streaming — rolling-window data buffer for live/real-time charts.

A ``StreamingChartBuffer`` holds a fixed-size FIFO window of data points that
can be snapshotted into a ``ChartSpec`` at any time.  It supports both regular
multi-series line/bar data and OHLC candlestick data.

Design principles (portability contract):
- Pure data — no Rich/Textual types anywhere.
- JSON-serializable: ``to_dict()`` / ``from_dict()`` work for every class.
- Thread safety is explicitly OUT of scope: callers that need it should
  wrap ``push()`` / ``push_ohlc()`` in their own ``threading.Lock``.

Example::

    from termforge.charts.streaming import StreamingChartBuffer
    from termforge.charts.types import ChartType

    buf = StreamingChartBuffer(max_points=60, series_count=2,
                               series_names=["CPU", "Memory"])
    buf.push([42.1, 68.3])
    buf.push([44.7, 71.0])

    spec = buf.to_chart_spec(
        chart_type=ChartType.LINE,
        title="System Metrics",
        width=80, height=20,
    )

OHLC example::

    ohlc_buf = StreamingChartBuffer(max_points=30, ohlc=True)
    ohlc_buf.push_ohlc(open=100.0, high=102.5, low=99.1, close=101.8)
    spec = ohlc_buf.to_chart_spec(chart_type=ChartType.CANDLESTICK,
                                  title="BTC/USD", width=80, height=20)
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any

from termforge.charts.types import (
    Axis,
    ChartSpec,
    ChartType,
    OHLCSeries,
    Series,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _auto_range(
    values: list[float],
    y_padding: float = 0.05,
) -> tuple[float, float]:
    """Return (min, max) for *values* with optional percentage padding.

    Args:
        values: Flat list of float data values.
        y_padding: Fraction of the data range to add above and below.
            Default ``0.05`` == 5 %.

    Returns:
        A ``(y_min, y_max)`` tuple suitable for ``Axis.min_val`` /
        ``Axis.max_val``.  If all values are equal, returns
        ``(value - 1, value + 1)`` to avoid zero-height axes.
    """
    if not values:
        return 0.0, 1.0
    lo, hi = min(values), max(values)
    span = hi - lo
    if span == 0:
        return lo - 1.0, hi + 1.0
    pad = span * y_padding
    return lo - pad, hi + pad


# ---------------------------------------------------------------------------
# StreamingChartBuffer
# ---------------------------------------------------------------------------

@dataclass
class StreamingChartBuffer:
    """A fixed-capacity rolling buffer that snapshots into a ``ChartSpec``.

    Attributes:
        max_points: Maximum number of samples stored.  When the buffer is
            full, the oldest sample is dropped (FIFO).
        series_count: Number of parallel data series (for non-OHLC charts).
        series_names: Display names for each series.  If shorter than
            *series_count*, missing names default to ``"series<N>"``.
        series_colors: Token names for each series colour.  Defaults to
            standard token names from the active theme.
        ohlc: When ``True``, the buffer stores OHLC tuples instead of
            per-series floats.  ``series_count`` is ignored.
        ohlc_name: Display name for the OHLC series.
        y_padding: Fraction of data range to use as padding when
            auto-scaling the y axis (default ``0.05``).
        _data: Internal per-series deques (non-OHLC mode).
        _ohlc: Internal OHLC deque (OHLC mode).
    """

    max_points: int = 120
    series_count: int = 1
    series_names: list[str] = field(default_factory=list)
    series_colors: list[str] = field(default_factory=list)
    ohlc: bool = False
    ohlc_name: str = "ohlc"
    y_padding: float = 0.05

    # Internal storage — not serialized as dataclass defaults,
    # but round-tripped via to_dict/from_dict.
    _data: list[deque[float]] = field(default_factory=list, repr=False)
    _ohlc: deque[dict[str, float]] = field(
        default_factory=deque, repr=False
    )

    def __post_init__(self) -> None:
        if not self.ohlc:
            # Initialise per-series deques if not already set
            if not self._data:
                self._data = [
                    deque(maxlen=self.max_points)
                    for _ in range(self.series_count)
                ]
            # Pad names list
            while len(self.series_names) < self.series_count:
                self.series_names.append(
                    f"series{len(self.series_names)}"
                )
            # Pad colours list
            _default_colors = [
                "primary", "secondary", "accent",
                "success", "warning", "error",
            ]
            while len(self.series_colors) < self.series_count:
                idx = len(self.series_colors) % len(_default_colors)
                self.series_colors.append(_default_colors[idx])
        else:
            if not isinstance(self._ohlc, deque):
                self._ohlc = deque(maxlen=self.max_points)
            else:
                self._ohlc = deque(self._ohlc, maxlen=self.max_points)

    # ------------------------------------------------------------------
    # Data ingestion
    # ------------------------------------------------------------------

    def push(self, values: list[float]) -> None:
        """Append one sample per series.

        Args:
            values: A list of floats, one per series.  If shorter than
                ``series_count``, missing series receive ``0.0``.

        Raises:
            ValueError: If the buffer was created in OHLC mode.
        """
        if self.ohlc:
            raise ValueError(
                "Use push_ohlc() for OHLC buffers, not push()."
            )
        for i, dq in enumerate(self._data):
            dq.append(values[i] if i < len(values) else 0.0)

    def push_ohlc(
        self,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: float = 0.0,
        timestamp: str | None = None,
    ) -> None:
        """Append one OHLC candlestick bar.

        Args:
            open: Opening price.
            high: High price.
            low: Low price.
            close: Closing price.
            volume: Optional volume (stored but not rendered by default).
            timestamp: Optional label string for the x-axis.

        Raises:
            ValueError: If the buffer was NOT created in OHLC mode.
        """
        if not self.ohlc:
            raise ValueError(
                "Use push() for non-OHLC buffers, not push_ohlc()."
            )
        bar: dict[str, Any] = {
            "open": float(open),
            "high": float(high),
            "low": float(low),
            "close": float(close),
            "volume": float(volume),
        }
        if timestamp is not None:
            bar["timestamp"] = timestamp
        self._ohlc.append(bar)

    # ------------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------------

    def to_chart_spec(
        self,
        chart_type: ChartType = ChartType.LINE,
        title: str | None = None,
        width: int = 80,
        height: int = 24,
        show_legend: bool = True,
        braille: bool = False,
        x_label: str | None = None,
        y_label: str | None = None,
        tick_count: int = 5,
        y_min: float | None = None,
        y_max: float | None = None,
        **kwargs: Any,
    ) -> ChartSpec:
        """Snapshot the current buffer window into a ``ChartSpec``.

        Y-axis bounds are auto-computed from current window data unless
        *y_min* / *y_max* are provided explicitly.

        Args:
            chart_type: The chart type to render.
            title: Optional chart title.
            width: Canvas width in characters.
            height: Canvas height in characters.
            show_legend: Whether to show the series legend.
            braille: Whether to use Braille dot rendering.
            x_label: Optional x-axis label.
            y_label: Optional y-axis label.
            tick_count: Number of y-axis ticks.
            y_min: Override auto-computed y minimum.
            y_max: Override auto-computed y maximum.
            **kwargs: Forwarded to ``ChartSpec`` constructor (e.g.
                ``highlight_max=True``).

        Returns:
            A fully-configured :class:`~termforge.charts.types.ChartSpec`.
        """
        if self.ohlc:
            return self._build_ohlc_spec(
                chart_type=chart_type,
                title=title, width=width, height=height,
                show_legend=show_legend, braille=braille,
                x_label=x_label, y_label=y_label,
                tick_count=tick_count,
                y_min=y_min, y_max=y_max, **kwargs
            )
        return self._build_series_spec(
            chart_type=chart_type,
            title=title, width=width, height=height,
            show_legend=show_legend, braille=braille,
            x_label=x_label, y_label=y_label,
            tick_count=tick_count,
            y_min=y_min, y_max=y_max, **kwargs
        )

    def _build_series_spec(self, *, chart_type: ChartType, title: str | None, width: int, height: int,
                           show_legend: bool, braille: bool, x_label: str | None, y_label: str | None,
                           tick_count: int, y_min: float | None, y_max: float | None, **kwargs: Any) -> ChartSpec:
        series_list = []
        all_values: list[float] = []
        for i, dq in enumerate(self._data):
            pts = list(dq)
            all_values.extend(pts)
            series_list.append(Series(
                name=self.series_names[i],
                data=pts,
                color_token=self.series_colors[i],
            ))
        computed_min, computed_max = _auto_range(all_values, self.y_padding)
        y_axis = Axis(
            label=y_label,
            min_val=y_min if y_min is not None else computed_min,
            max_val=y_max if y_max is not None else computed_max,
            tick_count=tick_count,
        )
        return ChartSpec(
            chart_type=chart_type,
            series=series_list,
            x_axis=Axis(label=x_label),
            y_axis=y_axis,
            width=width, height=height,
            title=title,
            show_legend=show_legend,
            braille=braille,
            **kwargs,
        )

    def _build_ohlc_spec(self, *, chart_type: ChartType, title: str | None, width: int, height: int,
                         show_legend: bool, braille: bool, x_label: str | None, y_label: str | None,
                         tick_count: int, y_min: float | None, y_max: float | None, **kwargs: Any) -> ChartSpec:
        bars = list(self._ohlc)
        timestamps = [str(b["timestamp"]) for b in bars if "timestamp" in b]
        ohlc_data = [
            {k: v for k, v in b.items() if k != "timestamp"}
            for b in bars
        ]
        # Auto-scale y from all high/low values
        all_prices: list[float] = []
        for b in ohlc_data:
            all_prices.extend([b.get("low", 0.0), b.get("high", 0.0)])
        computed_min, computed_max = _auto_range(all_prices, self.y_padding)
        ohlc_series = OHLCSeries(
            name=self.ohlc_name,
            data=ohlc_data,
            timestamps=timestamps if timestamps else None,
        )


        y_axis = Axis(
            label=y_label,
            min_val=y_min if y_min is not None else computed_min,
            max_val=y_max if y_max is not None else computed_max,
            tick_count=tick_count,
        )
        return ChartSpec(
            chart_type=chart_type,
            ohlc_series=ohlc_series,
            x_axis=Axis(label=x_label),
            y_axis=y_axis,
            width=width, height=height,
            title=title,
            show_legend=show_legend,
            braille=braille,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    @property
    def point_count(self) -> int:
        """Number of data points currently stored (across the first series)."""
        if self.ohlc:
            return len(self._ohlc)
        return len(self._data[0]) if self._data else 0

    @property
    def is_full(self) -> bool:
        """``True`` if the buffer has reached ``max_points`` capacity."""
        return self.point_count >= self.max_points

    def clear(self) -> None:
        """Remove all data from the buffer without changing configuration."""
        if self.ohlc:
            self._ohlc.clear()
        else:
            for dq in self._data:
                dq.clear()

    def latest(self, n: int = 1) -> list[list[float]]:
        """Return the last *n* samples as a list of ``[v_series0, ...]`` rows.

        Args:
            n: Number of most-recent samples to return.

        Returns:
            List of rows, each row being a list of one float per series.
        """
        if self.ohlc:
            raise ValueError("Use latest_ohlc() for OHLC buffers.")
        n = max(1, n)
        rows: list[list[float]] = []
        if not self._data:
            return rows
        length = len(self._data[0])
        start = max(0, length - n)
        for i in range(start, length):
            rows.append([list(dq)[i] for dq in self._data])
        return rows

    def latest_ohlc(self, n: int = 1) -> list[dict[str, float]]:
        """Return the last *n* OHLC bars.

        Args:
            n: Number of most-recent bars to return.

        Returns:
            List of OHLC dicts (same format as ``push_ohlc`` arguments).
        """
        if not self.ohlc:
            raise ValueError("Use latest() for non-OHLC buffers.")
        bars = list(self._ohlc)
        return bars[max(0, len(bars) - n):]

    # ------------------------------------------------------------------
    # Portability contract
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialize the buffer to a JSON-compatible dict.

        Note:
            Serialises the current window content so the snapshot can be
            restored via :meth:`from_dict`.

        Returns:
            A plain dict that round-trips through ``json.dumps`` /
            ``json.loads``.
        """
        return {
            "max_points": self.max_points,
            "series_count": self.series_count,
            "series_names": list(self.series_names),
            "series_colors": list(self.series_colors),
            "ohlc": self.ohlc,
            "ohlc_name": self.ohlc_name,
            "y_padding": self.y_padding,
            "_data": [list(dq) for dq in self._data],
            "_ohlc": list(self._ohlc),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "StreamingChartBuffer":
        """Deserialise a buffer previously produced by :meth:`to_dict`.

        Args:
            d: Dict as returned by :meth:`to_dict`.

        Returns:
            A new :class:`StreamingChartBuffer` with its data window
            restored.
        """
        is_ohlc = d.get("ohlc", False)
        max_pts = d.get("max_points", 120)
        buf = cls(
            max_points=max_pts,
            series_count=d.get("series_count", 1),
            series_names=list(d.get("series_names", [])),
            series_colors=list(d.get("series_colors", [])),
            ohlc=is_ohlc,
            ohlc_name=d.get("ohlc_name", "ohlc"),
            y_padding=d.get("y_padding", 0.05),
        )
        if is_ohlc:
            for bar in d.get("_ohlc", []):
                buf._ohlc.append(dict(bar))
        else:
            for i, pts in enumerate(d.get("_data", [])):
                if i < len(buf._data):
                    for v in pts:
                        buf._data[i].append(v)
        return buf

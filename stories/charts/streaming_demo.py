"""Story: charts/streaming_demo — showcase StreamingChartBuffer.

Demonstrates the three main use patterns:
1. Single-series rolling window (seeded random CPU data)
2. Multi-series rolling window (CPU + Memory)
3. OHLC candlestick rolling window (synthetic stock ticks)
"""
import random
from termforge.charts.streaming import StreamingChartBuffer
from termforge.charts.types import ChartType


def main() -> None:
    rng = random.Random(42)  # seeded for deterministic golden

    print("=== TermForge Chart Streaming Demo ===\n")

    # ------------------------------------------------------------------ 1
    print("─── 1. Single-series CPU rolling buffer (max_points=5) ───")
    buf = StreamingChartBuffer(max_points=5, series_names=["CPU %"])
    cpu_values = [45.2, 52.1, 60.8, 55.3, 48.9, 67.4, 71.2, 63.5]
    for v in cpu_values:
        buf.push([v])
    print(f"  pushed {len(cpu_values)} samples, window holds {buf.point_count}")
    print(f"  is_full: {buf.is_full}")
    print(f"  latest 2 rows: {buf.latest(2)}")
    spec = buf.to_chart_spec(chart_type=ChartType.LINE, title="CPU %",
                             width=60, height=10)
    d = spec.to_dict()
    print(f"  spec type: {d['chart_type']}  y_min={d['y_axis']['min_val']:.2f}"
          f"  y_max={d['y_axis']['max_val']:.2f}")
    print()

    # ------------------------------------------------------------------ 2
    print("─── 2. Multi-series CPU + Memory (max_points=4) ───")
    mbuf = StreamingChartBuffer(max_points=4, series_count=2,
                                series_names=["CPU", "Memory"])
    samples = [(42.1, 68.3), (44.7, 71.0), (47.3, 73.5), (50.0, 75.1), (52.8, 77.3)]
    for cpu, mem in samples:
        mbuf.push([cpu, mem])
    print(f"  series: {mbuf.series_names}")
    print(f"  window size: {mbuf.point_count}")
    mspec = mbuf.to_chart_spec(title="System Metrics", width=60, height=12)
    md = mspec.to_dict()
    for s in md["series"]:
        print(f"  [{s['name']}] data={s['data']}")
    print()

    # ------------------------------------------------------------------ 3
    print("─── 3. OHLC candlestick buffer (max_points=4) ───")
    obuf = StreamingChartBuffer(max_points=4, ohlc=True, ohlc_name="BTC/USD")
    ticks = [
        (100.0, 104.5, 99.2, 102.3, "T1"),
        (102.3, 106.1, 101.0, 105.8, "T2"),
        (105.8, 107.2, 103.5, 104.1, "T3"),
        (104.1, 109.3, 102.8, 108.7, "T4"),
        (108.7, 112.0, 107.4, 110.5, "T5"),
    ]
    for o, h, lo, c, ts in ticks:
        obuf.push_ohlc(open=o, high=h, low=lo, close=c, timestamp=ts)
    print(f"  bars in window: {obuf.point_count}")
    print(f"  latest bar: {obuf.latest_ohlc(1)[0]}")
    ospec = obuf.to_chart_spec(chart_type=ChartType.CANDLESTICK,
                               title="BTC/USD", width=60, height=14)
    od = ospec.to_dict()
    print(f"  ohlc_series name: {od['ohlc_series']['name']}")
    print(f"  timestamps: {od['ohlc_series']['timestamps']}")
    print(f"  y range: [{od['y_axis']['min_val']:.2f}, {od['y_axis']['max_val']:.2f}]")
    print()

    # ------------------------------------------------------------------ 4 — portability
    print("─── 4. Portability: JSON round-trip ───")
    import json
    d_serial = mbuf.to_dict()
    json_str = json.dumps(d_serial)
    buf_restored = StreamingChartBuffer.from_dict(json.loads(json_str))
    print(f"  JSON bytes: {len(json_str)}")
    print(f"  restored series count: {buf_restored.series_count}")
    print(f"  restored point count: {buf_restored.point_count}")
    assert buf_restored.series_names == mbuf.series_names
    print("  Portability: OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import sys
from termforge.core.types import ColorDepth
from termforge.charts.types import ChartSpec, ChartType, OHLCSeries, Axis
from termforge.charts.chart import render_chart

def seeded_ohlc_generator(seed: int, count: int) -> list[dict[str, float]]:
    state = seed
    data = []
    close = 100.0
    for _ in range(count):
        state = (state * 1103515245 + 12345) & 0x7fffffff
        r1 = (state % 100) / 100.0
        state = (state * 1103515245 + 12345) & 0x7fffffff
        r2 = (state % 100) / 100.0
        state = (state * 1103515245 + 12345) & 0x7fffffff
        r3 = (state % 100) / 100.0
        
        change = (r1 - 0.46) * 12.0
        open_val = close
        close_val = open_val + change
        high_val = max(open_val, close_val) + r2 * 5.0
        low_val = min(open_val, close_val) - r3 * 5.0
        
        data.append({
            "open": round(open_val, 2),
            "high": round(high_val, 2),
            "low": round(low_val, 2),
            "close": round(close_val, 2)
        })
        close = close_val
    return data

def main() -> None:
    ohlc_data = seeded_ohlc_generator(42, 10) # 10 days of candles
    ohlc_series = OHLCSeries(name="stock", data=ohlc_data)
    
    spec = ChartSpec(
        chart_type=ChartType.CANDLESTICK,
        ohlc_series=ohlc_series,
        width=60,
        height=14,
        title="Seeded OHLC Stock Candlestick Chart",
        x_axis=Axis(label="Days", tick_count=5),
        y_axis=Axis(label="Price", tick_count=5)
    )
    
    print("--- Stock Candlestick Chart ---")
    lines = render_chart(spec, depth=ColorDepth.TRUECOLOR)
    for line in lines:
        print(line)

if __name__ == "__main__":
    main()

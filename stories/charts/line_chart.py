#!/usr/bin/env python3
import sys
import math
from termforge.core.types import ColorDepth
from termforge.charts.types import ChartSpec, ChartType, Series, Axis
from termforge.charts.chart import render_chart

def main() -> None:
    # Generate a sine wave data
    data = [math.sin(x * 0.5) * 10.0 for x in range(30)]
    
    spec = ChartSpec(
        chart_type=ChartType.LINE,
        series=[Series(name="sine", data=data, color_token="primary")],
        width=60,
        height=15,
        title="Sine Wave Line Chart",
        x_axis=Axis(label="Time", tick_count=5),
        y_axis=Axis(label="Amplitude", tick_count=5)
    )
    
    print("--- Sine Wave (Standard Canvas) ---")
    lines = render_chart(spec, depth=ColorDepth.TRUECOLOR)
    for line in lines:
        print(line)
        
    print("\n--- Sine Wave (Braille High-Res Canvas) ---")
    spec.braille = True
    lines_braille = render_chart(spec, depth=ColorDepth.TRUECOLOR)
    for line in lines_braille:
        print(line)

if __name__ == "__main__":
    main()

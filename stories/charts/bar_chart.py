#!/usr/bin/env python3
import sys
from termforge.core.types import ColorDepth
from termforge.charts.types import ChartSpec, ChartType, Series, Axis
from termforge.charts.chart import render_chart

def main() -> None:
    data = [4.0, 8.0, 15.0, 16.0, 23.0, 42.0]
    
    spec = ChartSpec(
        chart_type=ChartType.BAR,
        series=[Series(name="lost_numbers", data=data, color_token="primary")],
        width=50,
        height=12,
        title="Lost Numbers Bar Chart",
        x_axis=Axis(label="Index", tick_count=6),
        y_axis=Axis(label="Value", tick_count=5)
    )
    
    print("--- Bar Chart (Standard Canvas) ---")
    lines = render_chart(spec, depth=ColorDepth.TRUECOLOR)
    for line in lines:
        print(line)

if __name__ == "__main__":
    main()

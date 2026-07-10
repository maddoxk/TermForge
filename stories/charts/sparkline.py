#!/usr/bin/env python3
import sys
from termforge.charts.types import ChartSpec, ChartType, Series
from termforge.charts.chart import render_chart

def main() -> None:
    data = [1.0, 3.0, 2.0, 5.0, 4.0, 8.0, 7.0, 9.0, 6.0, 10.0]
    
    spec = ChartSpec(
        chart_type=ChartType.SPARKLINE,
        series=[Series(name="spark", data=data)]
    )
    
    lines = render_chart(spec)
    print("Sparkline:")
    print(lines[0])

if __name__ == "__main__":
    main()

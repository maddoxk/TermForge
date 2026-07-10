from __future__ import annotations
from termforge.core.types import ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.charts.types import ChartSpec, ChartType
from termforge.charts.scale import compute_bounds, generate_ticks
from termforge.charts.canvas import Canvas, BrailleCanvas, create_canvas, create_braille_canvas, canvas_to_lines, braille_canvas_to_lines
from termforge.charts.renderers import (
    render_sparkline, render_line_chart, render_bar_chart, render_scatter_chart,
    render_histogram, render_stacked_bar, render_multi_bar, render_heatmap, render_candlestick
)

def render_chart(spec: ChartSpec, theme: ThemeTokens | None = None, depth: ColorDepth = ColorDepth.TRUECOLOR) -> list[str]:
    # Sparkline is inline, handles itself
    if spec.chart_type == ChartType.SPARKLINE:
        return [render_sparkline(spec)]
        
    # Calculate Plotting Area dimensions (accounting for axes)
    # y-axis label column: 8 chars (e.g. "  12.5 │")
    # x-axis tick row: 1 char, x-axis label row: 1 char
    y_axis_w = 8
    x_axis_h = 2
    
    plot_w = max(10, spec.width - y_axis_w)
    plot_h = max(5, spec.height - x_axis_h)
    
    # 1. Create Canvas
    is_braille = spec.braille and spec.chart_type in (ChartType.LINE, ChartType.SCATTER)
    if is_braille:
        canvas = create_braille_canvas(plot_w, plot_h)
    else:
        canvas = create_canvas(plot_w, plot_h)
        
    # 2. Render plot contents
    if spec.chart_type == ChartType.LINE:
        render_line_chart(spec, canvas)
    elif spec.chart_type == ChartType.BAR:
        render_bar_chart(spec, canvas)
    elif spec.chart_type == ChartType.SCATTER:
        render_scatter_chart(spec, canvas)
    elif spec.chart_type == ChartType.HISTOGRAM:
        render_histogram(spec, canvas)
    elif spec.chart_type == ChartType.STACKED_BAR:
        render_stacked_bar(spec, canvas)
    elif spec.chart_type == ChartType.MULTI_BAR:
        render_multi_bar(spec, canvas)
    elif spec.chart_type == ChartType.HEATMAP:
        render_heatmap(spec, canvas)
    elif spec.chart_type == ChartType.CANDLESTICK:
        render_candlestick(spec, canvas)
        
    # 3. Convert plotting canvas to lines of strings
    if is_braille:
        plot_lines = braille_canvas_to_lines(canvas, theme, depth)
    else:
        plot_lines = canvas_to_lines(canvas, theme, depth)
        
    # 4. Add Y-Axis Labels
    # Compute bounds for Y axis labels
    if spec.chart_type == ChartType.CANDLESTICK and spec.ohlc_series:
        highs = [d["high"] for d in spec.ohlc_series.data]
        lows = [d["low"] for d in spec.ohlc_series.data]
        y_min, y_max = compute_bounds(highs + lows, spec.y_axis)
    else:
        all_y = []
        for s in spec.series:
            all_y.extend(s.data)
        y_min, y_max = compute_bounds(all_y, spec.y_axis)
        
    y_ticks = generate_ticks(y_min, y_max, plot_h, spec.y_axis.format_str)
    # y_ticks are generated from min to max (bottom to top)
    # our lines are from top to bottom (row 0 is max, row height-1 is min)
    # So we reverse the y_ticks to match lines
    y_ticks = list(reversed(y_ticks))
    
    final_lines = []
    for r in range(plot_h):
        val, label = y_ticks[r]
        # Format label to fit exactly y_axis_w - 2 (6 chars), plus axis line "│"
        short_label = label[:y_axis_w - 2].rjust(y_axis_w - 2)
        final_lines.append(f"{short_label} │{plot_lines[r]}")
        
    # 5. Add X-Axis Line and Labels
    # Draw bottom horizontal axis line
    axis_line = "─" * plot_w
    final_lines.append(" " * (y_axis_w - 2) + " └" + axis_line)
    
    # Generate X-axis labels
    # We display e.g. 5 ticks across plot_w
    max_len = 0
    if spec.chart_type == ChartType.CANDLESTICK and spec.ohlc_series:
        max_len = len(spec.ohlc_series.data)
    elif spec.series:
        max_len = max(len(s.data) for s in spec.series)
        
    x_min, x_max = 0.0, float(max_len - 1) if max_len > 0 else 1.0
    x_ticks = generate_ticks(x_min, x_max, spec.x_axis.tick_count, spec.x_axis.format_str)
    
    # We construct the label row.
    # We want to space out labels at their scaled column index
    label_row = [" "] * (spec.width)
    for val, label in x_ticks:
        # Scale X val to plot cols
        from termforge.charts.scale import scale_value
        cx = scale_value(val, x_min, x_max, plot_w)
        # Shift cx by the Y-axis width offset
        target_x = y_axis_w + cx
        
        # Center the label text on target_x
        start_idx = target_x - len(label) // 2
        for char_idx, char in enumerate(label):
            idx = start_idx + char_idx
            if y_axis_w <= idx < spec.width:
                label_row[idx] = char
                
    final_lines.append("".join(label_row))
    
    # Append Title if present
    if spec.title:
        title_line = spec.title.center(spec.width)
        final_lines.insert(0, title_line)
        
    return final_lines

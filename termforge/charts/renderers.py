from __future__ import annotations
import math
from termforge.core.types import StyleSpec, ColorValue, ColorDepth
from termforge.core.theme import ThemeTokens
from termforge.charts.types import ChartSpec, OHLCSeries
from termforge.charts.scale import compute_bounds, scale_value, nice_bounds
from termforge.charts.canvas import Canvas, BrailleCanvas, set_cell, draw_line, set_braille_pixel, draw_braille_line

def render_sparkline(spec: ChartSpec, theme: ThemeTokens | None = None, depth: ColorDepth = ColorDepth.TRUECOLOR) -> str:
    if not spec.series or not spec.series[0].data:
        return ""
    data = spec.series[0].data
    val_min = min(data)
    val_max = max(data)
    if val_min == val_max:
        return "▄" * len(data)
        
    c_start = None
    c_end = None
    if theme and spec.color_config and "gradient" in spec.color_config:
        grad = spec.color_config["gradient"]
        if isinstance(grad, list) and len(grad) >= 2:
            from termforge.core.theme import resolve_token
            c_start = resolve_token(theme, f"colors.{grad[0]}")
            c_end = resolve_token(theme, f"colors.{grad[1]}")

    idx_max = data.index(val_max) if (spec.highlight_max and val_min != val_max) else -1
    idx_min = data.index(val_min) if (spec.highlight_min and val_min != val_max) else -1
            
    blocks = " ▂▃▄▅▆▇█"
    num_blocks = len(blocks)
    spark = []
    for idx_val, val in enumerate(data):
        ratio = (val - val_min) / (val_max - val_min)
        idx = min(num_blocks - 1, max(0, int(ratio * (num_blocks - 1))))
        char = blocks[idx]
        
        if idx_val == idx_max:
            from termforge.text.render import style_to_ansi
            style = StyleSpec(fg=ColorValue(0, 0, 0, name="colors.accent"))
            start_ansi, end_ansi = style_to_ansi(style, theme, depth)
            char = f"{start_ansi}{char}{end_ansi}"
        elif idx_val == idx_min:
            from termforge.text.render import style_to_ansi
            style = StyleSpec(fg=ColorValue(0, 0, 0, name="colors.error"))
            start_ansi, end_ansi = style_to_ansi(style, theme, depth)
            char = f"{start_ansi}{char}{end_ansi}"
        elif c_start and c_end:
            from termforge.core.color import interpolate_color
            from termforge.text.render import style_to_ansi
            
            c_curr = interpolate_color(c_start, c_end, ratio)
            style = StyleSpec(fg=c_curr)
            start_ansi, end_ansi = style_to_ansi(style, theme, depth)
            char = f"{start_ansi}{char}{end_ansi}"
            
        spark.append(char)
    return "".join(spark)

def get_style_for_token(color_token: str) -> StyleSpec:
    # A simple token-to-color mapper fallback. Real theme resolving happens at canvas rendering.
    # We can encode the color token into the style's fg name!
    # For example, style.fg = ColorValue(0,0,0, name=f"colors.{color_token}")
    # That way style_to_ansi will resolve it directly from the theme pack!
    return StyleSpec(fg=ColorValue(0, 0, 0, name=f"colors.{color_token}"))

def render_line_chart(spec: ChartSpec, canvas: Canvas | BrailleCanvas) -> None:
    if not spec.series or not spec.series[0].data:
        return
        
    # Gather all Y data to compute bounds
    all_y = []
    for s in spec.series:
        all_y.extend(s.data)
        
    y_min, y_max = compute_bounds(all_y, spec.y_axis)
    
    # X bounds are simply 0 to max_len - 1
    max_len = max(len(s.data) for s in spec.series)
    x_min, x_max = 0.0, float(max_len - 1)
    
    is_braille = isinstance(canvas, BrailleCanvas)
    
    for s in spec.series:
        style = get_style_for_token(s.color_token)
        points = []
        
        # Calculate scaled coordinates
        for idx, val in enumerate(s.data):
            if is_braille:
                cx = scale_value(idx, x_min, x_max, 2 * canvas.width)
                cy = scale_value(val, y_min, y_max, 4 * canvas.height)
            else:
                cx = scale_value(idx, x_min, x_max, canvas.width)
                cy = scale_value(val, y_min, y_max, canvas.height)
            points.append((cx, cy))
            
        # Draw lines between successive points
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            if isinstance(canvas, BrailleCanvas):
                draw_braille_line(canvas, x1, y1, x2, y2, style)
            elif isinstance(canvas, Canvas):
                draw_line(canvas, x1, y1, x2, y2, "*", style)

def render_bar_chart(spec: ChartSpec, canvas: Canvas) -> None:
    if not spec.series or not spec.series[0].data:
        return
    data = spec.series[0].data
    y_min, y_max = compute_bounds(data, spec.y_axis)
    
    # We want to fit all bars across the width
    num_bars = len(data)
    bar_width = max(1, canvas.width // num_bars)
    
    style = get_style_for_token(spec.series[0].color_token)
    
    for idx, val in enumerate(data):
        scaled_y = scale_value(val, y_min, y_max, canvas.height)
        scaled_zero = scale_value(0.0, y_min, y_max, canvas.height)
        
        # Draw column
        x_start = idx * bar_width
        start_y = min(scaled_zero, scaled_y)
        end_y = max(scaled_zero, scaled_y)
        
        for x in range(x_start, min(canvas.width, x_start + bar_width - 1)):
            for y in range(start_y, end_y + 1):
                set_cell(canvas, x, y, "█", style)

def render_scatter_chart(spec: ChartSpec, canvas: Canvas | BrailleCanvas) -> None:
    if not spec.series or not spec.series[0].data:
        return
        
    all_y = []
    for s in spec.series:
        all_y.extend(s.data)
    y_min, y_max = compute_bounds(all_y, spec.y_axis)
    
    max_len = max(len(s.data) for s in spec.series)
    x_min, x_max = 0.0, float(max_len - 1)
    
    is_braille = isinstance(canvas, BrailleCanvas)
    
    for s in spec.series:
        style = get_style_for_token(s.color_token)
        for idx, val in enumerate(s.data):
            if isinstance(canvas, BrailleCanvas):
                cx = scale_value(idx, x_min, x_max, 2 * canvas.width)
                cy = scale_value(val, y_min, y_max, 4 * canvas.height)
                set_braille_pixel(canvas, cx, cy, True, style)
            elif isinstance(canvas, Canvas):
                cx = scale_value(idx, x_min, x_max, canvas.width)
                cy = scale_value(val, y_min, y_max, canvas.height)
                set_cell(canvas, cx, cy, "o", style)

def render_histogram(spec: ChartSpec, canvas: Canvas) -> None:
    if not spec.series or not spec.series[0].data:
        return
    data = spec.series[0].data
    
    # Compute bins
    num_bins = min(canvas.width // 2, 10) # default 10 bins or less
    val_min = min(data)
    val_max = max(data)
    if val_min == val_max:
        val_max += 1.0
        
    bin_width = (val_max - val_min) / num_bins
    bins = [0] * num_bins
    for val in data:
        bin_idx = min(num_bins - 1, max(0, int((val - val_min) / bin_width)))
        bins[bin_idx] += 1
        
    # Now plot bins as a bar chart
    y_min, y_max = 0.0, float(max(bins))
    bar_width = max(1, canvas.width // num_bins)
    style = get_style_for_token(spec.series[0].color_token)
    
    for idx, count in enumerate(bins):
        scaled_y = scale_value(count, y_min, y_max, canvas.height)
        x_start = idx * bar_width
        for x in range(x_start, min(canvas.width, x_start + bar_width - 1)):
            for y in range(0, scaled_y + 1):
                set_cell(canvas, x, y, "█", style)

def render_stacked_bar(spec: ChartSpec, canvas: Canvas) -> None:
    if not spec.series or not spec.series[0].data:
        return
        
    num_bars = len(spec.series[0].data)
    bar_width = max(1, canvas.width // num_bars)
    
    # Compute stacked heights
    stacked_data = []
    for i in range(num_bars):
        col_sum = sum(s.data[i] for s in spec.series if i < len(s.data))
        stacked_data.append(col_sum)
        
    y_min, y_max = compute_bounds(stacked_data, spec.y_axis)
    
    for col_idx in range(num_bars):
        current_y_val = 0.0
        x_start = col_idx * bar_width
        
        for s in spec.series:
            if col_idx >= len(s.data):
                continue
            val = s.data[col_idx]
            style = get_style_for_token(s.color_token)
            
            scaled_start = scale_value(current_y_val, y_min, y_max, canvas.height)
            scaled_end = scale_value(current_y_val + val, y_min, y_max, canvas.height)
            
            for x in range(x_start, min(canvas.width, x_start + bar_width - 1)):
                for y in range(scaled_start, scaled_end + 1):
                    set_cell(canvas, x, y, "█", style)
            current_y_val += val

def render_multi_bar(spec: ChartSpec, canvas: Canvas) -> None:
    if not spec.series:
        return
        
    num_groups = len(spec.series[0].data)
    num_series = len(spec.series)
    group_width = max(1, canvas.width // num_groups)
    bar_width = max(1, (group_width - 1) // num_series)
    
    all_y = []
    for s in spec.series:
        all_y.extend(s.data)
    y_min, y_max = compute_bounds(all_y, spec.y_axis)
    
    for group_idx in range(num_groups):
        group_x = group_idx * group_width
        for series_idx, s in enumerate(spec.series):
            if group_idx >= len(s.data):
                continue
            val = s.data[group_idx]
            style = get_style_for_token(s.color_token)
            
            scaled_y = scale_value(val, y_min, y_max, canvas.height)
            x_start = group_x + series_idx * bar_width
            
            for x in range(x_start, min(canvas.width, x_start + bar_width)):
                for y in range(0, scaled_y + 1):
                    set_cell(canvas, x, y, "█", style)

def render_heatmap(spec: ChartSpec, canvas: Canvas) -> None:
    if not spec.series:
        return
    # In a heatmap, each series is a row, data elements are columns
    num_rows = len(spec.series)
    num_cols = len(spec.series[0].data)
    
    row_height = max(1, canvas.height // num_rows)
    col_width = max(1, canvas.width // num_cols)
    
    all_vals = []
    for s in spec.series:
        all_vals.extend(s.data)
    val_min = min(all_vals)
    val_max = max(all_vals)
    if val_min == val_max:
        val_max += 1.0
        
    # Render cell by cell
    for r_idx, s in enumerate(spec.series):
        y_start = r_idx * row_height
        for c_idx, val in enumerate(s.data):
            x_start = c_idx * col_width
            
            # Map value to color gradient: blue (low) to red (high)
            ratio = (val - val_min) / (val_max - val_min)
            # Create a ColorValue based on ratio
            color = ColorValue(int(255 * ratio), 0, int(255 * (1 - ratio)))
            style = StyleSpec(fg=color, bg=color) # Solid color box
            
            for x in range(x_start, min(canvas.width, x_start + col_width)):
                for y in range(y_start, min(canvas.height, y_start + row_height)):
                    set_cell(canvas, x, y, "█", style)

def render_candlestick(spec: ChartSpec, canvas: Canvas) -> None:
    if not spec.ohlc_series or not spec.ohlc_series.data:
        return
    ohlc = spec.ohlc_series.data
    
    # Calculate bounds over all highs and lows
    highs = [d["high"] for d in ohlc]
    lows = [d["low"] for d in ohlc]
    y_min, y_max = compute_bounds(highs + lows, spec.y_axis)
    
    num_candles = len(ohlc)
    candle_width = max(3, canvas.width // num_candles) # at least 3 cols wide for wick + body
    
    # Theme colors for up/down candles
    up_style = StyleSpec(fg=ColorValue(0, 0, 0, name="colors.success"))
    down_style = StyleSpec(fg=ColorValue(0, 0, 0, name="colors.error"))
    
    for idx, tick in enumerate(ohlc):
        o = tick["open"]
        h = tick["high"]
        l = tick["low"]
        c = tick["close"]
        
        # Center column of this candlestick
        x_center = idx * candle_width + (candle_width // 2)
        
        # Scale Y positions
        sy_high = scale_value(h, y_min, y_max, canvas.height)
        sy_low = scale_value(l, y_min, y_max, canvas.height)
        sy_open = scale_value(o, y_min, y_max, canvas.height)
        sy_close = scale_value(c, y_min, y_max, canvas.height)
        
        # Determine up/down style
        style = up_style if c >= o else down_style
        
        # 1. Draw wick (high to low)
        for y in range(min(sy_low, sy_high), max(sy_low, sy_high) + 1):
            set_cell(canvas, x_center, y, "│", style)
            
        # 2. Draw body (open to close)
        body_start = min(sy_open, sy_close)
        body_end = max(sy_open, sy_close)
        
        body_char = "█" if c < o else "░" # Solid for down, shaded/hollow for up
        
        # Body width is candle_width - 2 (leaving gaps)
        half_w = max(1, (candle_width - 2) // 2)
        for x in range(x_center - half_w, x_center + half_w + 1):
            for y in range(body_start, body_end + 1):
                set_cell(canvas, x, y, body_char, style)

# TermForge Charts Module Specification

This module defines unified chart structures, data scaling, coordinate mapping, Bresenham's line drawing, Braille dot mapping, and specific rendering geometries.

## 1. Data Structures

### `Axis`
Describes properties of an axis.
- `label`: string | null
- `min_val`: float | null
- `max_val`: float | null
- `tick_count`: integer
- `format_str`: string

### `Series`
- `name`: string
- `data`: list of floats
- `color_token`: string

### `OHLCSeries`
- `name`: string
- `data`: list of dictionaries with keys `open`, `high`, `low`, `close`
- `timestamps`: list of strings | null

### `ChartSpec`
- `chart_type`: `ChartType` (line, bar, scatter, candlestick, sparkline, etc.)
- `series`: list of `Series`
- `ohlc_series`: `OHLCSeries` | null
- `x_axis`: `Axis`
- `y_axis`: `Axis`
- `width`: integer
- `height`: integer
- `title`: string | null
- `show_legend`: boolean
- `braille`: boolean

---

## 2. Algorithms

### Nice Bounds Computation (`nice_bounds`)
Rounds minimum and maximum data values to clean, readable numbers for axis tick marks.

#### Pseudocode:
```
function nice_bounds(min_val: float, max_val: float) -> tuple[float, float]:
    if min_val == max_val:
        return min_val - 1.0, max_val + 1.0
    diff = max_val - min_val
    magnitude = 10 ^ floor(log10(diff))
    
    nice_steps = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
    step = magnitude
    for s in nice_steps:
        curr_step = s * magnitude
        if diff / curr_step <= 10:
            step = curr_step
            break
            
    nice_min = floor(min_val / step) * step
    nice_max = ceil(max_val / step) * step
    return nice_min, nice_max
```

### Coordinate Scaling (`scale_value`)
Maps a data point value to a discrete column or row index on the character grid.
$$\text{index} = \text{ratio} \times (\text{target\_size} - 1)$$
where $\text{ratio} = \frac{\text{val} - \text{min}}{\text{max} - \text{min}}$.

### Braille Canvas Encoding
Unicode Braille characters occupy the range `U+2800` to `U+28FF`. Each cell is a 2x4 grid of sub-pixels.
Offset logic:
$$\text{Code} = 0\text{x}2800 + \sum_{dx=0}^{1} \sum_{dy=0}^{3} \text{mask}(dx, dy) \times \text{active}(dx, dy)$$
Where $\text{mask}$ maps dot coordinates to bit indices:
- `(0, 0) -> 0x01`
- `(0, 1) -> 0x02`
- `(0, 2) -> 0x04`
- `(0, 3) -> 0x40`
- `(1, 0) -> 0x08`
- `(1, 1) -> 0x10`
- `(1, 2) -> 0x20`
- `(1, 3) -> 0x80`

### Candlestick Geometry
For each OHLC tick:
1. Identify the center column of the candle.
2. Draw a vertical line `│` from the scaled `low` value to the scaled `high` value (the wick).
3. Draw a box of width $\text{candle\_width} - 2$ from the scaled `open` value to the scaled `close` value (the body).
   - If `close >= open` (upward), use a hollow/shaded body character `░`.
   - If `close < open` (downward), use a filled body character `█`.
4. Style the candle: Green/Success for upward, Red/Error for downward.

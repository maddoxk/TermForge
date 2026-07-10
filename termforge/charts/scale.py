from __future__ import annotations
import math
from termforge.charts.types import Axis

def nice_bounds(min_val: float, max_val: float) -> tuple[float, float]:
    if min_val == max_val:
        return min_val - 1.0, max_val + 1.0
    diff = max_val - min_val
    try:
        mag = 10 ** math.floor(math.log10(diff))
    except (ValueError, OverflowError):
        mag = 1.0
        
    steps = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
    step = mag
    for s in steps:
        curr_step = s * mag
        if curr_step > 0 and diff / curr_step <= 10:
            step = curr_step
            break
            
    nice_min = math.floor(min_val / step) * step
    nice_max = math.ceil(max_val / step) * step
    return nice_min, nice_max

def compute_bounds(data: list[float], axis: Axis) -> tuple[float, float]:
    if not data:
        return 0.0, 1.0
    val_min = min(data)
    val_max = max(data)
    
    # Apply nice bounds first if not overridden
    nice_min, nice_max = nice_bounds(val_min, val_max)
    
    final_min = axis.min_val if axis.min_val is not None else nice_min
    final_max = axis.max_val if axis.max_val is not None else nice_max
    
    if final_min == final_max:
        final_min -= 1.0
        final_max += 1.0
        
    return final_min, final_max

def scale_value(value: float, min_val: float, max_val: float, target_size: int) -> int:
    if min_val == max_val:
        return 0
    ratio = (value - min_val) / (max_val - min_val)
    idx = int(ratio * (target_size - 1))
    return min(target_size - 1, max(0, idx))

def generate_ticks(min_val: float, max_val: float, count: int, format_str: str = "{:.1f}") -> list[tuple[float, str]]:
    if count <= 1:
        return [(min_val, format_str.format(min_val))]
        
    ticks = []
    step = (max_val - min_val) / (count - 1)
    for i in range(count):
        val = min_val + step * i
        # Format the label nicely
        try:
            label = format_str.format(val)
        except Exception:
            label = f"{val:.1f}"
        ticks.append((val, label))
    return ticks

#!/usr/bin/env python3
import sys
from termforge.core import Size, FlexDirection
from termforge.windows.types import WindowSpec, PaneSpec
from termforge.windows.compositor import compose_panes, render_window

def main() -> None:
    # We want a layout of width=60, height=10
    total_size = Size(60, 10)
    
    left_win = WindowSpec(title="Sidebar", width=20, height=10)
    right_win = WindowSpec(title="Content Pane", width=40, height=10, focused=True)
    
    pane = PaneSpec(
        direction=FlexDirection.ROW,
        children=[left_win, right_win],
        ratios=[1.0, 2.0],
        gap=0
    )
    
    # 1. Compose sizes and positions
    layouts = compose_panes(pane, total_size)
    
    # 2. Render each window separately with its computed size
    left_content = ["* Home", "* Settings", "* Dashboard", "* Help"]
    right_content = [
        "Welcome to TermForge!",
        "This is a split screen layout demo.",
        "The right window has focus.",
        "Layout math distributed sizes automatically:"
    ]
    
    # Update widths/heights of specs from composed layout
    pos_left, size_left, spec_left = layouts[0]
    spec_left.width = size_left.width
    spec_left.height = size_left.height
    
    pos_right, size_right, spec_right = layouts[1]
    spec_right.width = size_right.width
    spec_right.height = size_right.height
    
    left_rendered = render_window(spec_left, left_content)
    right_rendered = render_window(spec_right, right_content)
    
    # 3. Combine row by row
    print("--- Window Layout Composited Screen ---")
    for r in range(total_size.height):
        line = left_rendered[r] + right_rendered[r]
        print(line)

if __name__ == "__main__":
    main()

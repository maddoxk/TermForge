from __future__ import annotations
import sys
import time
import os
from termforge.core import Size, ColorDepth, detect_capabilities
from termforge.core.types import FlexDirection
from termforge.core.scheduler import create_scheduler, register_animation, tick, AnimationSpec
from termforge.windows.types import WindowSpec, PaneSpec
from termforge.windows.compositor import compose_panes, render_window
from termforge.text.types import TextSpec
from termforge.text.render import render_text
from termforge.charts.types import ChartSpec, ChartType, OHLCSeries
from termforge.charts.chart import render_chart
from termforge.logos.types import LogoSpec
from termforge.logos.render import render_logo
from termforge.animation.types import SpinnerSpec, SpinnerStyle
from termforge.animation.spinners import render_spinner

def create_ohlc_data() -> list[dict[str, float]]:
    return [
        {"open": 100.0, "high": 105.0, "low": 98.0, "close": 102.5},
        {"open": 102.5, "high": 108.0, "low": 101.0, "close": 107.0},
        {"open": 107.0, "high": 107.5, "low": 99.0, "close": 101.2},
        {"open": 101.2, "high": 104.0, "low": 95.0, "close": 96.8},
        {"open": 96.8, "high": 102.0, "low": 96.0, "close": 101.5},
        {"open": 101.5, "high": 106.0, "low": 100.2, "close": 105.1},
        {"open": 105.1, "high": 111.0, "low": 104.0, "close": 109.8},
        {"open": 109.8, "high": 110.0, "low": 105.0, "close": 106.5}
    ]

def main() -> None:
    # 1. Detect capabilities
    caps = detect_capabilities()
    depth = caps.color_depth
    
    # 2. Main Window setup (width 80, height 24)
    win_w, win_h = 80, 24
    main_win = WindowSpec(title="TermForge Flagship Dashboard", width=win_w, height=win_h, focused=True)
    
    # Inner viewport size
    inner_w = win_w - 2
    inner_h = win_h - 2
    inner_size = Size(inner_w, inner_h)
    
    pane = PaneSpec(
        direction=FlexDirection.COLUMN,
        children=[
            LogoSpec(text="TF", font="small"),
            ChartSpec(chart_type=ChartType.CANDLESTICK),
            TextSpec(content="")
        ],
        ratios=[5.0, 12.0, 5.0],
        gap=0
    )
    
    # 3. Setup Scheduler
    scheduler = create_scheduler()
    anim_spec = AnimationSpec(fps=10.0, duration_ms=None, callback_id="spinner")
    scheduler = register_animation(scheduler, anim_spec)
    
    # Render loop
    print("\033[2J", end="") # Initial full screen clear
    
    try:
        while True:
            # Update scheduler clock (in ms)
            curr_time_ms = time.time() * 1000.0
            scheduler, fired = tick(scheduler, curr_time_ms)
            
            # Get current frame for spinner
            spinner_frame_num = scheduler.frame_counts.get("spinner", 0)
            
            # Resolve layout geometry
            layouts = compose_panes(pane, inner_size)
            
            # --- Render Row 0 (Top Panel: Logo & Spinner split) ---
            pos_top, size_top, _ = layouts[0]
            top_pane = PaneSpec(direction=FlexDirection.ROW, children=[LogoSpec(), SpinnerSpec()], ratios=[1.0, 2.0])
            top_layouts = compose_panes(top_pane, size_top)
            
            # Left Top: Logo
            _, size_logo, _ = top_layouts[0]
            logo_spec = LogoSpec(text="TF", font="small", gradient=["#ff007f", "#7f00ff"])
            logo_lines = render_logo(logo_spec, depth=depth)
            logo_lines += [""] * (size_logo.height - len(logo_lines))
            logo_lines = [f"{line:<{size_logo.width}}" for line in logo_lines]
            
            # Right Top: Spinner & Status
            _, size_spin, _ = top_layouts[1]
            spin_spec = SpinnerSpec(style=SpinnerStyle.DOTS, label="Streaming Real-Time Stock Feed...")
            spin_frame = render_spinner(spin_spec, spinner_frame_num, depth=depth)
            
            spin_lines = [
                spin_frame,
                "Market Status: \033[32mOPEN\033[0m",
                "Connected to WebSocket server",
                "Refresh rate: 10 FPS"
            ]
            spin_lines += [""] * (size_spin.height - len(spin_lines))
            spin_lines = [f"{line:<{size_spin.width}}" for line in spin_lines]
            
            top_panel_lines = []
            for r in range(size_top.height):
                top_panel_lines.append(logo_lines[r] + spin_lines[r])
                
            # --- Render Row 1 (Candlestick Chart) ---
            _, size_chart, _ = layouts[1]
            ohlc_data = create_ohlc_data()
            chart_spec = ChartSpec(
                chart_type=ChartType.CANDLESTICK,
                ohlc_series=OHLCSeries(data=ohlc_data),
                width=size_chart.width,
                height=size_chart.height,
                title="Apple Inc. (AAPL) 1-Minute Candle",
                show_legend=False
            )
            chart_lines = render_chart(chart_spec, depth=depth)
            chart_lines += [""] * (size_chart.height - len(chart_lines))
            
            # --- Render Row 2 (Data Table) ---
            _, size_table, _ = layouts[2]
            table_markup = (
                "[bold]Ticker │ Open   │ High   │ Low    │ Close  │ Volume[/bold]\n"
                "───────┼────────┼────────┼────────┼────────┼────────\n"
                "AAPL   │ 100.00 │ 111.00 │ 95.00  │ 106.50 │ 4.8M\n"
                "GOOG   │ 172.10 │ 175.40 │ 170.80 │ 174.90 │ 1.1M"
            )
            table_spec = TextSpec(content=table_markup, max_width=size_table.width)
            table_lines = render_text(table_spec, depth=depth)
            table_lines += [""] * (size_table.height - len(table_lines))
            
            # --- Composite all parts ---
            full_body = top_panel_lines + chart_lines + table_lines
            
            # Wrap in main bordered window
            screen = render_window(main_win, full_body, depth=depth)
            
            # Draw on screen in-place
            print("\033[H", end="")
            for line in screen:
                print(line)
                
            print("\nPress Ctrl+C to exit demo.")
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\033[2J\033[HTermForge Demo completed.")
        sys.exit(0)

if __name__ == "__main__":
    main()

"""TermForge v2.1 Interactive Showcase & Live Command Center App.

Features live interactive keyboard navigation (Tab/Shift+Tab, Arrow keys, 1-3)
across live-updating component views.
"""
from __future__ import annotations

import math
import random
import termforge as tf
from termforge.combobox.types import ComboboxSpec
from termforge.search.types import SearchBarSpec


def generate_ohlc_series(count: int = 10) -> list[dict[str, float]]:
    base = 150.0
    series = []
    for _ in range(count):
        change = random.uniform(-3.0, 3.5)
        open_val = base
        close_val = base + change
        high_val = max(open_val, close_val) + random.uniform(0.5, 2.0)
        low_val = min(open_val, close_val) - random.uniform(0.5, 2.0)
        series.append({
            "open": round(open_val, 2),
            "high": round(high_val, 2),
            "low": round(low_val, 2),
            "close": round(close_val, 2),
        })
        base = close_val
    return series


def run_super_app_demo(duration_sec: float | None = None, fps: float = 10.0) -> None:
    # Interactive State Containers
    active_tab = tf.State(0)
    selected_btn = tf.State(0)
    accordion_expanded = tf.State(0)
    focused_item = tf.State("Tabs")

    cpu_usage = tf.State(45.0)
    ram_usage = tf.State(8.2)
    packet_rate = tf.State(1200)

    # Keypress Event Handler
    def handle_key_input(key: str) -> None:
        if key in ("tab", "right", "l"):
            active_tab.value = (active_tab.value + 1) % 3
            focused_item.value = f"Tab {active_tab.value + 1}"
        elif key in ("left", "h"):
            active_tab.value = (active_tab.value - 1) % 3
            focused_item.value = f"Tab {active_tab.value + 1}"
        elif key in ("1", "f1"):
            active_tab.value = 0
            focused_item.value = "Tab 1"
        elif key in ("2", "f2"):
            active_tab.value = 1
            focused_item.value = "Tab 2"
        elif key in ("3", "f3"):
            active_tab.value = 2
            focused_item.value = "Tab 3"
        elif key in ("up", "k"):
            accordion_expanded.value = 0
        elif key in ("down", "j"):
            accordion_expanded.value = 1
        elif key in ("space", "enter"):
            selected_btn.value = (selected_btn.value + 1) % 3
            focused_item.value = f"Action {selected_btn.value + 1}"

    def render_frame(frame_idx: int) -> tf.RenderableSpec:
        t = frame_idx * 0.1
        cpu_val = max(10.0, min(99.0, 50.0 + 35.0 * math.sin(t * 0.8) + random.uniform(-4, 4)))
        ram_val = max(4.0, min(15.8, 8.0 + 4.0 * math.cos(t * 0.4) + random.uniform(-0.2, 0.2)))
        pkt_val = int(max(200, 1500 + 800 * math.sin(t * 1.5) + random.uniform(-80, 80)))

        cpu_usage.value = round(cpu_val, 1)
        ram_usage.value = round(ram_val, 1)
        packet_rate.value = pkt_val

        # ------------------- 1. HEADER -------------------
        tabs = tf.TabSpec(
            titles=["1: Dashboard", "2: Market Stream", "3: Config & Mesh"],
            active_index=active_tab.value
        )

        status_badge = tf.BadgeSpec(text="LIVE INTERACTIVE", severity="success", brackets="[ ]")
        spinner = tf.SpinnerSpec(style=tf.SpinnerStyle.DOTS, label="Keyboard Ready")
        search_bar = SearchBarSpec(query="cluster-prod", placeholder="Search...")

        hdr_left = tf.draw(tabs, width=54, height=1).strip()
        hdr_badge = " " + tf.draw(status_badge, width=20, height=1).strip()
        hdr_spinner = " " + tf.draw(spinner, width=20, height=1).strip()
        header_line = f"{hdr_left}{hdr_badge}{hdr_spinner}"

        # ------------------- 2. DYNAMIC TAB CONTENT -------------------
        if active_tab.value == 0:
            # --- Tab 1: System Telemetry & Task Checklist ---
            cpu_progress = tf.ProgressSpec(progress=cpu_val / 100.0, text_width=4, width=24)
            ram_progress = tf.ProgressSpec(progress=ram_val / 16.0, text_width=4, width=24)

            telemetry_grid = tf.KeyValueGridSpec(
                items=[
                    tf.KeyValueItemSpec(key="CPU Load", value=f"{cpu_val:5.1f}%  {tf.draw(cpu_progress, width=24, height=1).strip()}"),
                    tf.KeyValueItemSpec(key="Memory", value=f"{ram_val:4.1f} GB  {tf.draw(ram_progress, width=24, height=1).strip()}"),
                    tf.KeyValueItemSpec(key="Packets", value=f"{pkt_val} req/s"),
                    tf.KeyValueItemSpec(key="Threads", value=f"{random.randint(16, 32)} workers"),
                ],
                key_width=10,
                separator=": "
            )

            metrics_card = tf.CardSpec(title="Cluster Telemetry", content=tf.draw(telemetry_grid, width=54, height=6))

            checklist = tf.ChecklistSpec(
                items=[
                    tf.ChecklistItemSpec(label="src/core.py (Refactored)", checked=True),
                    tf.ChecklistItemSpec(label="src/render.py (Optimized)", checked=True),
                    tf.ChecklistItemSpec(label="config.yaml (Validated)", checked=False),
                ],
                selected_idx=2
            )
            tree_card = tf.CardSpec(title="Project Tasks Checklist", content=tf.draw(checklist, width=54, height=4))

            c1 = tf.draw(metrics_card, width=56, height=8).split("\n")
            c2 = tf.draw(tree_card, width=56, height=8).split("\n")
            tab_lines = [f"{c1[r]}  {c2[r]}" for r in range(max(len(c1), len(c2)))]

        elif active_tab.value == 1:
            # --- Tab 2: OHLC Stock Candlesticks & Live Logs ---
            series = generate_ohlc_series(7)
            chart = tf.ChartSpec(
                chart_type=tf.ChartType.CANDLESTICK,
                ohlc_series=[tf.OHLCSeries(data=series, name="AAPL")],
                title="Real-time OHLC Candlesticks",
                width=54,
                height=7
            )
            chart_card = tf.CardSpec(title="Market Candlestick Stream", content=tf.draw(chart, width=54, height=7))

            log_buffer = [{"level": lvl, "message": msg, "timestamp": "17:03:00"} for lvl, msg in [
                ("INFO", "Keyboard input listener attached."),
                ("INFO", f"Active Tab: {active_tab.value + 1}"),
                ("WARN", "Traffic spike detected on eth0"),
                ("INFO", f"Workers: {random.randint(16, 32)}"),
                ("DEBUG", "Syncing ledger state..."),
            ]]
            log_streamer = tf.LogStreamerSpec(buffer=log_buffer, max_lines=5)
            logs_card = tf.CardSpec(title="System Event Log Stream", content=tf.draw(log_streamer, width=54, height=6))

            c1 = tf.draw(chart_card, width=56, height=8).split("\n")
            c2 = tf.draw(logs_card, width=56, height=8).split("\n")
            tab_lines = [f"{c1[r]}  {c2[r]}" for r in range(max(len(c1), len(c2)))]

        else:
            # --- Tab 3: Accordions, Table, Buttons, & Controls ---
            accordion = tf.AccordionSpec(
                items=[
                    tf.AccordionItemSpec(title="Network Configuration", details="Interface: eth0 | IP: 192.168.1.100", is_expanded=(accordion_expanded.value == 0)),
                    tf.AccordionItemSpec(title="Security Policies", details="TLS v1.3 | Strict Transport Security: Enabled", is_expanded=(accordion_expanded.value == 1)),
                ],
                selected_idx=accordion_expanded.value
            )

            buttons = tf.ButtonGroupSpec(buttons=["Deploy", "Rollback", "Purge Cache"], selected_idx=selected_btn.value)
            combo = ComboboxSpec(options=["Production", "Staging", "Development"], selected_idx=0)

            controls_str = (
                tf.draw(accordion, width=52, height=4) + "\n" +
                "Actions: " + tf.draw(buttons, width=32, height=1).strip() +
                "  Env: " + tf.draw(combo, width=16, height=1).strip()
            )
            controls_card = tf.CardSpec(title="Node Controls & Accordion", content=controls_str)

            table = tf.TableSpec(
                columns=[
                    tf.ColumnSpec(title="Service"),
                    tf.ColumnSpec(title="Port"),
                    tf.ColumnSpec(title="Latency"),
                    tf.ColumnSpec(title="Health"),
                ],
                rows=[
                    ["auth-service", "8080", "4ms", "100%"],
                    ["db-primary", "5432", "1ms", "100%"],
                    ["redis-cache", "6379", "0.5ms", "99.9%"],
                ]
            )
            table_card = tf.CardSpec(title="Service Mesh Table", content=tf.draw(table, width=54, height=5))

            c1 = tf.draw(controls_card, width=56, height=8).split("\n")
            c2 = tf.draw(table_card, width=56, height=8).split("\n")
            tab_lines = [f"{c1[r]}  {c2[r]}" for r in range(max(len(c1), len(c2)))]

        middle_section = "\n".join(tab_lines)

        # ------------------- 3. FOOTER & NAVIGATION LEGEND -------------------
        status_bar = tf.StatusBarSpec(
            left=[tf.StatusSectionSpec(text=f"FOCUSED: {focused_item.value}")],
            right=[tf.StatusSectionSpec(text=f"FPS: {fps:.0f}"), tf.StatusSectionSpec(text=f"Frame: {frame_idx}")]
        )
        legend = tf.KeyLegendSpec(
            bindings=[
                tf.InputBindingSpec(key="Tab / ← →", action="Switch Tabs"),
                tf.InputBindingSpec(key="↑ ↓", action="Expand Accordion"),
                tf.InputBindingSpec(key="Space / Enter", action="Click Action"),
                tf.InputBindingSpec(key="Ctrl+C", action="Exit")
            ],
            spacing=3
        )

        footer_line = tf.draw(status_bar, width=114, height=1) + "\n" + tf.draw(legend, width=114, height=1)

        page_body = (
            header_line + "\n" +
            tf.draw(tf.DividerSpec(label="INTERACTIVE TERMINAL COMMAND CENTER", alignment="center"), width=114, height=1) + "\n" +
            middle_section + "\n" +
            footer_line
        )

        return tf.WindowSpec(
            title="TermForge v2.1 Interactive Terminal Command Center",
            content=page_body,
            width=118,
            height=20
        )

    tf.stream(render_frame, fps=fps, duration_sec=duration_sec, on_key=handle_key_input, width=118, height=20)


def main() -> None:
    print("Starting TermForge v2.1 Interactive Command Center...")
    run_super_app_demo()


if __name__ == "__main__":
    main()

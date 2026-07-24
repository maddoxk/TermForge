"""TermForge Ultimate Comprehensive Showcase Demo.

Demonstrates multi-component live reactive layout streaming, dynamic data sources,
page tab switching, charts, tables, log streaming, badges, accordions, and controls.
"""
from __future__ import annotations

import math
import random
import time
import termforge as tf


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


def run_showcase_demo(duration_sec: float = 10.0, fps: float = 10.0) -> None:
    # 1. State containers for live data feeds
    active_tab = tf.State(0)
    cpu_usage = tf.State(45.0)
    ram_usage = tf.State(8.2)
    packet_rate = tf.State(1200)
    system_status = tf.State("HEALTHY")
    
    logs = [
        "[INFO] System boot sequence complete.",
        "[INFO] Connected to telemetry WebSocket endpoint.",
        "[DEBUG] Syncing cluster node states...",
    ]

    log_levels = ["INFO", "DEBUG", "WARN", "ERROR"]
    log_messages = [
        "Inbound traffic spike on eth0",
        "GC pause 12ms in worker-03",
        "Cache hit ratio 94.2%",
        "Heartbeat acknowledged by peer node",
        "Database pool connection reset",
    ]

    start_time = time.time()

    def render_frame(frame_idx: int) -> tf.RenderableSpec:
        # Simulate live data mutation every frame step
        t = frame_idx * 0.1
        cpu_val = max(10.0, min(99.0, 50.0 + 35.0 * math.sin(t * 0.8) + random.uniform(-5, 5)))
        ram_val = max(4.0, min(15.8, 8.0 + 4.0 * math.cos(t * 0.4) + random.uniform(-0.2, 0.2)))
        pkt_val = int(max(200, 1500 + 800 * math.sin(t * 1.5) + random.uniform(-100, 100)))

        cpu_usage.value = round(cpu_val, 1)
        ram_usage.value = round(ram_val, 1)
        packet_rate.value = pkt_val

        # Change tabs every 5 seconds (50 frames)
        tab_idx = (frame_idx // 50) % 3
        active_tab.value = tab_idx

        # Append live log line every 8 frames
        if frame_idx % 8 == 0:
            lvl = random.choice(log_levels)
            msg = random.choice(log_messages)
            logs.append(f"[{lvl}] {msg}")
            if len(logs) > 6:
                logs.pop(0)

        # Update status severity
        if cpu_val > 80.0:
            system_status.value = "CRITICAL"
            badge_severity = "error"
        elif cpu_val > 65.0:
            system_status.value = "WARNING"
            badge_severity = "warning"
        else:
            system_status.value = "OPTIMAL"
            badge_severity = "success"

        # ------------------- Build Page UI Layout -------------------
        # Header Menu Bar + Tabs
        header_menu = tf.MenuBarSpec(
            menus=[
                tf.MenuItemSpec(label="Dashboard (F1)"),
                tf.MenuItemSpec(label="Market Feed (F2)"),
                tf.MenuItemSpec(label="System Config (F3)"),
            ],
            selected_idx=tab_idx,
            spacing=3
        )

        top_badge = tf.BadgeSpec(text=system_status.value, severity=badge_severity, brackets="[ ]")

        # Tab Content Switching
        if tab_idx == 0:
            # --- Tab 0: System Telemetry & Log Streamer ---
            cpu_progress = tf.ProgressSpec(progress=cpu_val / 100.0, width=32)
            ram_progress = tf.ProgressSpec(progress=ram_val / 16.0, width=32)

            telemetry_grid = tf.KeyValueGridSpec(
                items=[
                    tf.KeyValueItemSpec(key="CPU Load", value=f"{cpu_val:5.1f}%  {tf.draw(cpu_progress, width=28, height=1).strip()}"),
                    tf.KeyValueItemSpec(key="Memory Usage", value=f"{ram_val:4.1f} GB / 16.0 GB  {tf.draw(ram_progress, width=28, height=1).strip()}"),
                    tf.KeyValueItemSpec(key="Net Packets", value=f"{pkt_val} req/s"),
                    tf.KeyValueItemSpec(key="Active Threads", value=f"{random.randint(12, 32)} workers"),
                ],
                key_width=14,
                separator=" : "
            )

            metrics_card = tf.CardSpec(
                title="Cluster Metrics",
                content=tf.draw(telemetry_grid, width=74, height=6)
            )

            log_buffer = [{"level": lvl, "message": msg, "timestamp": "15:48:30"} for lvl, msg in [
                ("INFO", "System boot sequence complete."),
                ("INFO", "Connected to telemetry WebSocket endpoint."),
                ("DEBUG", "Syncing cluster node states..."),
                ("WARN", "Inbound traffic spike on eth0"),
                ("INFO", "Cache hit ratio 94.2%"),
            ]]

            log_streamer = tf.LogStreamerSpec(
                buffer=log_buffer,
                max_lines=5
            )

            logs_card = tf.CardSpec(
                title="Real-Time Event Streamer",
                content=tf.draw(log_streamer, width=74, height=6)
            )

            tab_body_str = tf.draw(metrics_card, width=76, height=8) + "\n" + tf.draw(logs_card, width=76, height=7)

        elif tab_idx == 1:
            # --- Tab 1: Financial OHLC Stock Candlestick Chart ---
            series = generate_ohlc_series(8)
            chart = tf.ChartSpec(
                chart_type=tf.ChartType.CANDLESTICK,
                ohlc_series=[tf.OHLCSeries(data=series, name="AAPL")],
                title="Apple Inc. (AAPL) Live Trading Stream",
                width=72,
                height=9
            )

            table = tf.TableSpec(
                columns=[
                    tf.ColumnSpec(title="Ticker"),
                    tf.ColumnSpec(title="Open"),
                    tf.ColumnSpec(title="High"),
                    tf.ColumnSpec(title="Low"),
                    tf.ColumnSpec(title="Close"),
                ],
                rows=[
                    ["AAPL", f"{series[-1]['open']:.2f}", f"{series[-1]['high']:.2f}", f"{series[-1]['low']:.2f}", f"{series[-1]['close']:.2f}"],
                    ["NVDA", "124.50", "128.90", "123.10", "127.80"],
                    ["TSLA", "215.10", "222.00", "212.40", "220.60"],
                ]
            )

            tab_body_str = tf.draw(chart, width=76, height=10) + "\n" + tf.draw(table, width=76, height=5)

        else:
            # --- Tab 2: Accordion & Form Controls ---
            accordion = tf.AccordionSpec(
                items=[
                    tf.AccordionItemSpec(title="Network Routing & DNS", details="Primary interface: eth0\nSubnet: 192.168.1.0/24", is_expanded=True),
                    tf.AccordionItemSpec(title="Database Connections", details="Max pool size: 50 connections\nIdle timeout: 300s", is_expanded=False),
                    tf.AccordionItemSpec(title="Security & Certificates", details="TLS v1.3 Enabled\nAuto-renew: True", is_expanded=False),
                ],
                selected_idx=0
            )

            buttons = tf.ButtonGroupSpec(
                buttons=["Save Config", "Reset Defaults", "Export YAML"],
                selected_idx=0,
                separator="   "
            )

            tab_body_str = tf.draw(accordion, width=76, height=9) + "\n\n" + tf.draw(buttons, width=76, height=2)

        # Footer Status Bar & Shortcut Legend
        status_bar = tf.StatusBarSpec(
            left=[tf.StatusSectionSpec(text="MODE: LIVE_SHOWCASE")],
            right=[tf.StatusSectionSpec(text=f"FPS: {fps:.0f}"), tf.StatusSectionSpec(text=f"Frame: {frame_idx}")]
        )

        legend = tf.KeyLegendSpec(
            bindings=[
                tf.InputBindingSpec(key="F1-F3", action="Switch Tabs"),
                tf.InputBindingSpec(key="Ctrl+C", action="Exit Demo")
            ],
            spacing=3
        )

        # Combine whole screen inside main Window Container
        main_content = (
            tf.draw(header_menu, width=76, height=1) + "\n" +
            "  System Status: " + tf.draw(top_badge, width=20, height=1).strip() + "\n" +
            tf.draw(tf.DividerSpec(label="LIVE FEED", alignment="center"), width=76, height=1) + "\n" +
            tab_body_str + "\n" +
            tf.draw(status_bar, width=76, height=1) + "\n" +
            tf.draw(legend, width=76, height=1)
        )

        return tf.WindowSpec(
            title="TermForge v2.1 Ultimate Showcase & Stress Test",
            content=main_content,
            width=80,
            height=24
        )

    # Execute stream
    tf.stream(render_frame, fps=fps, duration_sec=duration_sec, width=80, height=24)


def main() -> None:
    print("Starting TermForge v2.1 Ultimate Showcase...")
    run_showcase_demo(duration_sec=8.0, fps=10.0)


if __name__ == "__main__":
    main()

"""TermForge Ultimate Comprehensive Single-Page Application (Super Dashboard).

Combines every single component category into a live, interactive 120x40 single-page terminal UI.
"""
from __future__ import annotations

import math
import random
import time
import termforge as tf
from termforge.dialog.types import DialogSpec
from termforge.tree.types import TreeSpec, TreeNodeSpec
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


def run_super_app_demo(duration_sec: float = 12.0, fps: float = 10.0) -> None:
    # State containers
    cpu_usage = tf.State(45.0)
    ram_usage = tf.State(8.2)
    packet_rate = tf.State(1200)
    system_status = tf.State("OPTIMAL")

    logs = [
        "[INFO] Cluster init complete.",
        "[INFO] Telemetry WebSocket connected.",
        "[DEBUG] Node health check OK.",
    ]
    log_levels = ["INFO", "DEBUG", "WARN", "ERROR"]
    log_messages = [
        "Inbound traffic spike eth0",
        "GC pause 12ms worker-3",
        "Cache hit ratio 94.2%",
        "Heartbeat acknowledged",
        "Database pool reconnected",
    ]

    def render_frame(frame_idx: int) -> tf.RenderableSpec:
        t = frame_idx * 0.1
        cpu_val = max(10.0, min(99.0, 50.0 + 35.0 * math.sin(t * 0.8) + random.uniform(-4, 4)))
        ram_val = max(4.0, min(15.8, 8.0 + 4.0 * math.cos(t * 0.4) + random.uniform(-0.2, 0.2)))
        pkt_val = int(max(200, 1500 + 800 * math.sin(t * 1.5) + random.uniform(-80, 80)))

        cpu_usage.value = round(cpu_val, 1)
        ram_usage.value = round(ram_val, 1)
        packet_rate.value = pkt_val

        if frame_idx % 6 == 0:
            lvl = random.choice(log_levels)
            msg = random.choice(log_messages)
            logs.append(f"[{lvl}] {msg}")
            if len(logs) > 5:
                logs.pop(0)

        if cpu_val > 80.0:
            system_status.value = "CRITICAL"
            badge_sev = "error"
        elif cpu_val > 65.0:
            system_status.value = "WARNING"
            badge_sev = "warning"
        else:
            system_status.value = "OPTIMAL"
            badge_sev = "success"

        # ------------------- 1. HEADER -------------------
        menu_bar = tf.MenuBarSpec(
            menus=[
                tf.MenuItemSpec(label="File", children=["New", "Save", "Exit"]),
                tf.MenuItemSpec(label="View", children=["Metrics", "Analytics"]),
                tf.MenuItemSpec(label="Help", children=["Docs", "About"]),
            ],
            selected_idx=0,
            spacing=4
        )

        status_badge = tf.BadgeSpec(text=system_status.value, severity=badge_sev, brackets="[ ]")
        spinner = tf.SpinnerSpec(style=tf.SpinnerStyle.DOTS, label="Live Sync...")
        search_bar = SearchBarSpec(query="cluster-prod", placeholder="Filter resources...")

        # Header bar string
        hdr_left = tf.draw(menu_bar, width=35, height=1).strip()
        hdr_badge = " Status: " + tf.draw(status_badge, width=16, height=1).strip()
        hdr_spinner = "  " + tf.draw(spinner, width=24, height=1).strip()
        hdr_search = "  " + tf.draw(search_bar, width=28, height=1).strip()
        header_line = f"{hdr_left}{hdr_badge}{hdr_spinner}{hdr_search}"

        # ------------------- 2. COLUMN 1: System Telemetry & File Tree -------------------
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

        metrics_card = tf.CardSpec(
            title="Cluster Telemetry",
            content=tf.draw(telemetry_grid, width=54, height=6)
        )

        # Workspace Tasks Checklist
        checklist = tf.ChecklistSpec(
            items=[
                tf.ChecklistItemSpec(label="src/core.py (Refactored)", checked=True),
                tf.ChecklistItemSpec(label="src/render.py (Optimized)", checked=True),
                tf.ChecklistItemSpec(label="config.yaml (Validated)", checked=False),
            ],
            selected_idx=2
        )

        tree_card = tf.CardSpec(
            title="Project Tasks Checklist",
            content=tf.draw(checklist, width=54, height=4)
        )

        col1_str = tf.draw(metrics_card, width=56, height=8) + "\n" + tf.draw(tree_card, width=56, height=8)

        # ------------------- 3. COLUMN 2: Market Feed & Event Logs -------------------
        series = generate_ohlc_series(7)
        chart = tf.ChartSpec(
            chart_type=tf.ChartType.CANDLESTICK,
            ohlc_series=[tf.OHLCSeries(data=series, name="AAPL")],
            title="Live Candlestick Analytics",
            width=54,
            height=7
        )

        log_buffer = [{"level": lvl, "message": msg, "timestamp": "16:58:00"} for lvl, msg in [
            ("INFO", "Cluster boot sequence OK."),
            ("INFO", "WebSocket telemetry connected."),
            ("WARN", "Traffic spike detected on eth0"),
            ("INFO", f"Active workers: {random.randint(16, 32)}"),
            ("DEBUG", "Syncing ledger state..."),
        ]]
        log_streamer = tf.LogStreamerSpec(buffer=log_buffer, max_lines=5)

        chart_card = tf.CardSpec(title="Market Stream", content=tf.draw(chart, width=54, height=7))
        logs_card = tf.CardSpec(title="Event Logs", content=tf.draw(log_streamer, width=54, height=6))

        col2_str = tf.draw(chart_card, width=56, height=9) + "\n" + tf.draw(logs_card, width=56, height=7)

        # Combine Col1 & Col2 side by side
        col1_lines = col1_str.split("\n")
        col2_lines = col2_str.split("\n")
        max_rows = max(len(col1_lines), len(col2_lines))
        middle_lines = []
        for r in range(max_rows):
            c1 = col1_lines[r] if r < len(col1_lines) else " " * 56
            c2 = col2_lines[r] if r < len(col2_lines) else " " * 56
            middle_lines.append(f"{c1}  {c2}")
        middle_section = "\n".join(middle_lines)

        # ------------------- 4. BOTTOM SECTION: Accordion & Controls & Table -------------------
        accordion = tf.AccordionSpec(
            items=[
                tf.AccordionItemSpec(title="Network Configuration", details="Interface: eth0 | IP: 192.168.1.100", is_expanded=True),
                tf.AccordionItemSpec(title="Security Policies", details="TLS v1.3 | Strict Transport Security: Enabled", is_expanded=False),
            ],
            selected_idx=0
        )

        buttons = tf.ButtonGroupSpec(buttons=["Deploy", "Rollback", "Purge Cache"], selected_idx=0)
        combo = ComboboxSpec(options=["Production", "Staging", "Development"], selected_idx=0)

        controls_str = (
            tf.draw(accordion, width=54, height=5) + "\n" +
            "Actions: " + tf.draw(buttons, width=32, height=1).strip() +
            "  Env: " + tf.draw(combo, width=16, height=1).strip()
        )
        controls_card = tf.CardSpec(title="Node Controls", content=controls_str)

        # Data Table
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
        table_card = tf.CardSpec(title="Service Mesh Status", content=tf.draw(table, width=54, height=5))

        bot1_lines = tf.draw(controls_card, width=56, height=8).split("\n")
        bot2_lines = tf.draw(table_card, width=56, height=8).split("\n")
        bottom_lines = []
        for r in range(max(len(bot1_lines), len(bot2_lines))):
            b1 = bot1_lines[r] if r < len(bot1_lines) else " " * 56
            b2 = bot2_lines[r] if r < len(bot2_lines) else " " * 56
            bottom_lines.append(f"{b1}  {b2}")
        bottom_section = "\n".join(bottom_lines)

        # ------------------- 5. FOOTER & OVERLAY DIALOG -------------------
        status_bar = tf.StatusBarSpec(
            left=[tf.StatusSectionSpec(text="MODE: LIVE_SUPER_APP")],
            right=[tf.StatusSectionSpec(text=f"FPS: {fps:.0f}"), tf.StatusSectionSpec(text=f"Frame: {frame_idx}")]
        )
        legend = tf.KeyLegendSpec(
            bindings=[
                tf.InputBindingSpec(key="F1-F12", action="Hotkeys"),
                tf.InputBindingSpec(key="Ctrl+C", action="Exit App")
            ],
            spacing=4
        )

        footer_line = tf.draw(status_bar, width=114, height=1) + "\n" + tf.draw(legend, width=114, height=1)

        # Combine entire single page canvas
        page_body = (
            header_line + "\n" +
            tf.draw(tf.DividerSpec(label="LIVE UNIFIED DASHBOARD", alignment="center"), width=114, height=1) + "\n" +
            middle_section + "\n" +
            bottom_section + "\n" +
            footer_line
        )

        return tf.WindowSpec(
            title="TermForge v2.1 Super-App Unified Terminal Command Center",
            content=page_body,
            width=118,
            height=34
        )

    tf.stream(render_frame, fps=fps, duration_sec=duration_sec, width=118, height=34)


def main() -> None:
    print("Starting TermForge v2.1 Super-App Unified Live Command Center...")
    run_super_app_demo(duration_sec=12.0, fps=10.0)


if __name__ == "__main__":
    main()

"""TermForge v2.1 Mega Single-Page Application.

Renders EVERY SINGLE ONE of the 30 library component types simultaneously on a single live page!
"""
from __future__ import annotations

import math
import random
import termforge as tf
from termforge.combobox.types import ComboboxSpec
from termforge.search.types import SearchBarSpec
from termforge.navigation.types import BreadcrumbsSpec
from termforge.radio.types import RadioButtonSpec, RadioButtonItemSpec
from termforge.slider.types import SliderSpec
from termforge.spinnerbox.types import SpinnerBoxSpec
from termforge.stepper.types import StepperSpec
from termforge.toast.types import ToastSpec
from termforge.toggle.types import ToggleSwitchSpec
from termforge.tooltip.types import TooltipSpec
from termforge.tree.types import TreeSpec, TreeNodeSpec
from termforge.dialog.types import DialogSpec


def generate_ohlc_series(count: int = 8) -> list[dict[str, float]]:
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
    slider_val = tf.State(65)
    toggle_val = tf.State(True)
    radio_idx = tf.State(0)

    cpu_usage = tf.State(45.0)
    ram_usage = tf.State(8.2)

    def handle_key_input(key: str) -> None:
        if key in ("tab", "right", "l"):
            active_tab.value = (active_tab.value + 1) % 3
        elif key in ("left", "h"):
            active_tab.value = (active_tab.value - 1) % 3
        elif key in ("up", "k"):
            slider_val.value = min(100, slider_val.value + 5)
        elif key in ("down", "j"):
            slider_val.value = max(0, slider_val.value - 5)
        elif key in ("space", "enter"):
            toggle_val.value = not toggle_val.value
            radio_idx.value = (radio_idx.value + 1) % 3

    def render_frame(frame_idx: int) -> tf.RenderableSpec:
        t = frame_idx * 0.1
        cpu_val = max(10.0, min(99.0, 50.0 + 35.0 * math.sin(t * 0.8) + random.uniform(-4, 4)))
        ram_val = max(4.0, min(15.8, 8.0 + 4.0 * math.cos(t * 0.4) + random.uniform(-0.2, 0.2)))
        cpu_usage.value = round(cpu_val, 1)
        ram_usage.value = round(ram_val, 1)

        # 1. MENU_BAR (1)
        menu_bar = tf.MenuBarSpec(
            menus=[
                tf.MenuItemSpec(label="File", children=["Save"]),
                tf.MenuItemSpec(label="Edit", children=["Copy"]),
                tf.MenuItemSpec(label="Help", children=["About"]),
            ],
            selected_idx=0
        )
        # 2. BREADCRUMBS (2)
        breadcrumbs = BreadcrumbsSpec(
            items=["Home", "Cluster", "Prod"]
        )
        # 3. BADGE (3)
        status_badge = tf.BadgeSpec(text="LIVE ALL-COMPONENTS", severity="success", brackets="[ ]")
        # 4. SPINNER (4)
        spinner = tf.SpinnerSpec(style=tf.SpinnerStyle.DOTS, label="Sync")
        # 5. SEARCH_BAR (5)
        search_bar = SearchBarSpec(query="mesh-01", placeholder="Search...")

        hdr1 = f"{tf.draw(menu_bar, width=28, height=1).strip()}  {tf.draw(breadcrumbs, width=32, height=1).strip()}  {tf.draw(status_badge, width=22, height=1).strip()}  {tf.draw(spinner, width=12, height=1).strip()}  {tf.draw(search_bar, width=18, height=1).strip()}"

        # 6. TAB (6)
        tabs = tf.TabSpec(
            titles=["1: Telemetry & Controls", "2: Market & Logs", "3: Config & Mesh"],
            active_index=active_tab.value
        )
        hdr2 = tf.draw(tabs, width=118, height=1)

        # 7. DIVIDER (7)
        divider = tf.DividerSpec(label="ALL 30 COMPONENTS LIVE CANVAS", alignment="center")
        hdr3 = tf.draw(divider, width=118, height=1)

        # --- SECTION A: LEFT COLUMN (Width 57) ---
        # 8. PROGRESS (8) & 9. KEYVALUE_GRID (9)
        cpu_prog = tf.ProgressSpec(progress=cpu_val / 100.0, text_width=4, width=20)
        ram_prog = tf.ProgressSpec(progress=ram_val / 16.0, text_width=4, width=20)
        kv_grid = tf.KeyValueGridSpec(
            items=[
                tf.KeyValueItemSpec(key="CPU", value=f"{cpu_val:5.1f}% {tf.draw(cpu_prog, width=20, height=1).strip()}"),
                tf.KeyValueItemSpec(key="RAM", value=f"{ram_val:4.1f}GB {tf.draw(ram_prog, width=20, height=1).strip()}"),
            ],
            key_width=6,
            separator=": "
        )
        # 10. CARD (10)
        card_metrics = tf.CardSpec(title="1-10: Cluster Telemetry", content=tf.draw(kv_grid, width=54, height=3))

        # 11. ACCORDION (11)
        accordion = tf.AccordionSpec(
            items=[tf.AccordionItemSpec(title="Network Settings", details="eth0 | 192.168.1.1", is_expanded=True)],
            selected_idx=0
        )
        # 12. CHECKLIST (12)
        checklist = tf.ChecklistSpec(
            items=[tf.ChecklistItemSpec(label="Auth Service OK", checked=True), tf.ChecklistItemSpec(label="Redis Cache OK", checked=True)],
            selected_idx=0
        )
        # 13. SELECTION (13)
        selection = tf.SelectionListSpec(
            items=[tf.SelectionItemSpec(label="Primary Node", selected=True), tf.SelectionItemSpec(label="Standby Node", selected=False)],
            focused_index=0
        )
        c_left_mid = (
            tf.draw(accordion, width=54, height=3) + "\n" +
            "Tasks: " + tf.draw(checklist, width=46, height=2).strip() + "\n" +
            "Node:  " + tf.draw(selection, width=46, height=2).strip()
        )
        card_controls = tf.CardSpec(title="11-13: Accordion & Lists", content=c_left_mid)

        # 14. BUTTONGROUP (14) & 15. COMBOBOX (15) & 16. RADIO (16) & 17. TOGGLE (17)
        btn_group = tf.ButtonGroupSpec(buttons=["Deploy", "Reset"], selected_idx=0)
        combo_box = ComboboxSpec(options=["Prod", "Stage"], selected_idx=0)
        radio_group = RadioButtonSpec(items=[RadioButtonItemSpec("Fast"), RadioButtonItemSpec("Slow")], selected_idx=radio_idx.value)
        toggle_sw = ToggleSwitchSpec(state=toggle_val.value, label="TLS")

        c_inputs = (
            "Btns: " + tf.draw(btn_group, width=18, height=1).strip() + "  Combo: " + tf.draw(combo_box, width=12, height=1).strip() + "\n" +
            "Mode: " + tf.draw(radio_group, width=20, height=1).strip() + "  Toggle: " + tf.draw(toggle_sw, width=12, height=1).strip()
        )
        card_inputs = tf.CardSpec(title="14-17: Buttons, Combo, Radio, Toggle", content=c_inputs)

        # 18. SLIDER (18) & 19. STEPPER (19) & 20. SPINNERBOX (20)
        slider = SliderSpec(value=float(slider_val.value), min_val=0.0, max_val=100.0, label="Vol")
        stepper = StepperSpec(steps=["Init", "Deploy", "Done"], active_idx=1)
        spin_box = SpinnerBoxSpec(value=42, min_val=0, max_val=100, label="MaxConn")

        c_widgets = (
            tf.draw(slider, width=54, height=1).strip() + "\n" +
            tf.draw(stepper, width=54, height=1).strip() + "\n" +
            tf.draw(spin_box, width=54, height=1).strip()
        )
        card_widgets = tf.CardSpec(title="18-20: Slider, Stepper, SpinnerBox", content=c_widgets)

        col_a_lines = (
            tf.draw(card_metrics, width=57, height=5) + "\n" +
            tf.draw(card_controls, width=57, height=7) + "\n" +
            tf.draw(card_inputs, width=57, height=4) + "\n" +
            tf.draw(card_widgets, width=57, height=5)
        ).split("\n")

        # --- SECTION B: RIGHT COLUMN (Width 57) ---
        # 21. CHART (21)
        chart_series = generate_ohlc_series(6)
        chart = tf.ChartSpec(
            chart_type=tf.ChartType.CANDLESTICK,
            ohlc_series=[tf.OHLCSeries(data=chart_series, name="AAPL")],
            title="OHLC Candlesticks",
            width=54,
            height=5
        )
        card_chart = tf.CardSpec(title="21: Candlestick Chart", content=tf.draw(chart, width=54, height=5))

        # 22. LOG_STREAMER (22)
        log_buf = [{"level": "INFO", "message": "Cluster operational.", "timestamp": "17:13:00"}]
        log_streamer = tf.LogStreamerSpec(buffer=log_buf, max_lines=2)
        card_logs = tf.CardSpec(title="22: Log Streamer", content=tf.draw(log_streamer, width=54, height=2))

        # 23. TABLE (23)
        table = tf.TableSpec(
            columns=[tf.ColumnSpec(title="Svc"), tf.ColumnSpec(title="Port"), tf.ColumnSpec(title="Latency")],
            rows=[["auth", "8080", "2ms"], ["db", "5432", "1ms"]]
        )
        card_table = tf.CardSpec(title="23: Service Table", content=tf.draw(table, width=54, height=3))

        # 24. TREE (24) & 25. TEXT (25) & 26. TOAST (26) & 27. TOOLTIP (27)
        tree = TreeSpec(root_nodes=[TreeNodeSpec(label="src/", expanded=True, children=[TreeNodeSpec(label="main.py")])], indent_size=2)
        rich_txt = tf.TextSpec(content="TermForge v2.1 Engine Active")
        toast = ToastSpec(text="Node 01 Synced", toast_type="success")
        tooltip = TooltipSpec(text="Active Node Info")

        c_misc = (
            "Tree:  " + "\n".join(tf.draw(tree, width=46, height=2)).strip() + "\n" +
            "Text:  " + tf.draw(rich_txt, width=20, height=1).strip() + "  Toast: " + tf.draw(toast, width=20, height=1).strip() + "\n" +
            "Tip:   " + tf.draw(tooltip, width=46, height=1).strip()
        )
        card_misc = tf.CardSpec(title="24-27: Tree, Text, Toast, Tooltip", content=c_misc)

        # 28. LOGO (28) & 29. IMAGE (29) & 30. DIALOG (30)
        logo = tf.LogoSpec(text="TERMFORGE", font="slant")
        dialog = DialogSpec(title="Alert", body="Mesh System Operational", buttons=["OK"])

        c_visuals = (
            "Logo:   " + tf.draw(logo, width=46, height=2).strip() + "\n" +
            "Dialog: " + tf.draw(dialog, width=46, height=3).strip()
        )
        card_visuals = tf.CardSpec(title="28-30: Logo & Dialog", content=c_visuals)

        col_b_lines = (
            tf.draw(card_chart, width=57, height=6) + "\n" +
            tf.draw(card_logs, width=57, height=4) + "\n" +
            tf.draw(card_table, width=57, height=4) + "\n" +
            tf.draw(card_misc, width=57, height=3) + "\n" +
            tf.draw(card_visuals, width=57, height=3)
        ).split("\n")

        # Combine Col A & Col B side-by-side
        max_rows = max(len(col_a_lines), len(col_b_lines))
        middle_rows = []
        for r in range(max_rows):
            ca = col_a_lines[r] if r < len(col_a_lines) else " " * 57
            cb = col_b_lines[r] if r < len(col_b_lines) else " " * 57
            middle_rows.append(f"{ca}  {cb}")

        # FOOTER: STATUS_BAR & KEY_LEGEND & WINDOW (Container Window)
        status_bar = tf.StatusBarSpec(
            left=[tf.StatusSectionSpec(text="ALL 30 COMPONENTS ACTIVE")],
            right=[tf.StatusSectionSpec(text=f"FPS: {fps:.0f}"), tf.StatusSectionSpec(text=f"Frame: {frame_idx}")]
        )
        legend = tf.KeyLegendSpec(
            bindings=[
                tf.InputBindingSpec(key="Tab/←/→", action="Tabs"),
                tf.InputBindingSpec(key="↑/↓", action="Slider"),
                tf.InputBindingSpec(key="Space", action="Toggle"),
                tf.InputBindingSpec(key="Ctrl+C", action="Exit"),
            ],
            spacing=2
        )
        ftr1 = tf.draw(status_bar, width=116, height=1)
        ftr2 = tf.draw(legend, width=116, height=1)

        page_body = (
            hdr1 + "\n" +
            hdr2 + "\n" +
            hdr3 + "\n" +
            "\n".join(middle_rows) + "\n" +
            ftr1 + "\n" +
            ftr2
        )

        return tf.WindowSpec(
            title="TermForge v2.1 Ultimate 30-Component Single-Page Mega Application",
            content=page_body,
            width=118,
            height=26
        )

    tf.stream(render_frame, fps=fps, duration_sec=duration_sec, on_key=handle_key_input, width=118, height=26)


def main() -> None:
    print("Starting TermForge v2.1 Ultimate 30-Component Mega Application...")
    run_super_app_demo()


if __name__ == "__main__":
    main()

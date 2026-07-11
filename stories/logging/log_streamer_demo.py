"""Story: logging/log_streamer_demo — showcase scrollable logger panel.

Demonstrates rolling buffers, automatic level highlighting, auto scroll behavior,
and integration with container borders.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.windows.types import WindowSpec
from termforge.windows.compositor import render_window
from termforge.logging.types import LogStreamerSpec
from termforge.logging.render import render_log_streamer


def main() -> None:
    print("=== TermForge LogStreamer Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # 1. Initialize LogStreamerSpec with level mapping styles
    logger = LogStreamerSpec(
        max_lines=15,
        auto_scroll=True,
        timestamp_format="%H:%M:%S",
        level_colors={
            "INFO": "colors.success",
            "WARNING": "colors.warning",
            "ERROR": "colors.danger",
        }
    )

    # 2. Append mock log messages
    logger.log("INFO", "Starting engine thread", timestamp="12:00:00")
    logger.log("INFO", "Loading configuration presets", timestamp="12:00:01")
    logger.log("WARNING", "Slow DB response detected, retrying", timestamp="12:00:03")
    logger.log("ERROR", "Database connection lost!", timestamp="12:00:05")
    logger.log("INFO", "Reconnecting to primary cluster", timestamp="12:00:06")
    logger.log("INFO", "Cluster status: OK", timestamp="12:00:07")

    # 3. Render inside a WindowSpec with scrollbar
    win_h = 8
    win_w = 52
    inner_h = win_h - 2
    inner_w = win_w - 2

    # Render logs content lines
    log_lines = render_log_streamer(logger, Size(inner_w, inner_h), theme=theme)

    # Wrap in Window
    win = WindowSpec(
        title="System Events Log",
        width=win_w,
        height=win_h,
        show_scrollbar=True,
        scrollbar_style="colors.primary"
    )
    rendered_win = render_window(win, log_lines, theme=theme)

    # Output to screen
    for line in rendered_win:
        print(line)
    print()

    # 4. Portability / serialization test
    d = logger.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = LogStreamerSpec.from_dict(d)
    print(f"Restored timestamp format: {restored.timestamp_format}")
    print(f"Restored log buffer size: {len(restored.buffer)}")
    print("Portability check: OK")


if __name__ == "__main__":
    main()

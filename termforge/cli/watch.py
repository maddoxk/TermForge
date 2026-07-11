"""CLI subcommand: termforge-watch — monitors and hot-reloads declarative layout configurations."""
from __future__ import annotations

import argparse
import os
import sys
import time

from termforge.cli.layout import render_once


def main() -> None:
    """Watch command entrypoint."""
    parser = argparse.ArgumentParser(
        description="TermForge Live Layout Config Watcher & Hot-Reloader"
    )
    parser.add_argument("path", help="Path to layout configuration file (yaml/json/toml)")
    parser.add_argument(
        "--color-depth",
        choices=["truecolor", "color_256", "color_16", "monochrome"],
        default=None,
        help="Simulated color depth tier (default: None)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Target configuration file '{args.path}' does not exist.")
        sys.exit(1)

    print(f"Watching '{args.path}' for modifications... Press Ctrl+C to stop.")
    last_mtime = 0.0

    try:
        while True:
            try:
                mtime = os.path.getmtime(args.path)
            except OSError:
                time.sleep(0.2)
                continue

            if mtime != last_mtime:
                last_mtime = mtime
                # Clear terminal screen and reset cursor home
                sys.stdout.write("\033[H\033[2J")
                sys.stdout.flush()
                print(f"Reloading layout preview for '{args.path}'...")
                try:
                    render_once(args.path, strict=False, color_depth=args.color_depth)
                except Exception as e:
                    print(f"\n❌ Error parsing configuration: {e}")

            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nStopping hot-reloader watcher.")
        sys.exit(0)


if __name__ == "__main__":
    main()

# TermForge

A universal terminal UI/UX design system for rendering rich, themed terminal interfaces.

## Features

- **Styled text** with markup parsing, wrapping, and color-depth fallback
- **Image rendering** via half-block Unicode and ASCII character ramps
- **Charts** — line, bar, scatter, histogram, heatmap, sparkline, candlestick/OHLC
- **Borders & windows** — composable panes with swappable glyph sets
- **Animations** — spinners, transitions, logo reveals
- **Theming** — data-driven token system (Catppuccin, Dracula, Tokyo Night, high-contrast)
- **Declarative config** — YAML/TOML/JSON specs that map 1:1 to the Python API

## Quick Start

```bash
pip install termforge
termforge-demo
```

## Architecture

Every visual element is a JSON-serializable **spec** consumed by a **renderer**.
Business logic lives in pure functions — no Rich/Textual types in signatures.
See `SPEC.md` files per module for language-agnostic algorithms.

## License

MIT

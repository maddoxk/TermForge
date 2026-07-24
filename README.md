# TermForge v2.0.0

A universal terminal UI/UX design system for rendering rich, themed terminal interfaces with minimal boilerplate.

## 🚀 What's New in v2.0.0?

TermForge v2.0.0 introduces a developer-first, high-level API designed to make building beautiful terminal components effortless:

- **Single Top-Level Import**: Access all component specs directly via `import termforge as tf`.
- **`tf.draw()` & `tf.render()`**: Render any component or layout with a single line of code without wiring up individual component renderers manually.

## 💡 Quick Start

```python
import termforge as tf

# Render a Card component
print(tf.draw(tf.CardSpec(title="Server Node-01", content="CPU: 42%\nRAM: 8.2 GB")))

# Render a Badge
print(tf.draw(tf.BadgeSpec(text="ACTIVE", severity="success")))

# Render a Progress Bar
print(tf.draw(tf.ProgressSpec(progress=0.85, width=30)))
```

## Features

- **Styled text** with markup parsing, wrapping, and color-depth fallback
- **Image rendering** via half-block Unicode and ASCII character ramps
- **Charts** — line, bar, scatter, histogram, heatmap, sparkline, candlestick/OHLC
- **Borders & windows** — composable panes with swappable glyph sets
- **Animations** — spinners, transitions, logo reveals
- **Theming** — data-driven token system (Catppuccin, Dracula, Tokyo Night, Nord, Gruvbox, high-contrast)
- **Declarative config** — YAML/TOML/JSON specs that map 1:1 to the Python API

## Quick CLI Demo

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

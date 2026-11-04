# TermForge

**A universal terminal UI/UX design system for Python.**

Build beautiful, themed terminal interfaces with a single import. No Rich types in your signatures. Pure functions. Zero boilerplate.

```python
import termforge as tf

print(tf.draw(tf.CardSpec(title="Server Node-01", content="CPU: 42%\nRAM: 8.2 GB")))
print(tf.draw(tf.BadgeSpec(text="ACTIVE", severity="success")))
print(tf.draw(tf.ProgressSpec(progress=0.85, width=30)))
```

## Why TermForge?

- **Single import** — `import termforge as tf` gives you everything
- **Declarative specs** — JSON-serializable component specs, renderers are pure functions
- **6 built-in themes** — Catppuccin Mocha, Dracula, Tokyo Night, Nord, Gruvbox, High Contrast
- **30+ components** — cards, charts, tables, trees, dialogs, animations, and more
- **Color-depth fallback** — truecolor to 256 to 16 to monochrome, automatic
- **CLI tools** — demo, playground REPL, layout visualizer, benchmark

## Quick Install

```bash
pip install git+https://github.com/maddoxk/TermForge
```

## Included Components

| Category | Components |
|----------|-----------|
| Display | Card, Badge, Text, Toast, Tooltip, Divider |
| Navigation | Breadcrumbs, MenuBar, Tabs, StatusBar |
| Input | ButtonGroup, Checklist, Combobox, Radio, Slider, Toggle, SearchBar |
| Data | Tables, TreeView, KeyValue, LogStreamer |
| Charts | Line, Bar, Scatter, Sparkline, Heatmap, Candlestick |
| Layout | Windows, Panes, Dialog, Accordion |
| Animation | Spinners, Transitions, Logo reveals |

## Next Steps

- [Install TermForge](getting-started/installation.md)
- [Follow the Quick Start](getting-started/quickstart.md)
- [Browse the Components gallery](components/index.md)
- [Explore the Themes](themes.md)

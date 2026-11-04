# Components

TermForge ships 30+ terminal UI components. All are:

- **Spec-based** — create a spec object, pass it to a renderer
- **Themeable** — accept an optional `theme: ThemeTokens`
- **Serializable** — all specs have `.to_dict()` / `.from_dict()`
- **Pure functions** — renderers return `list[str]`, no side effects

## Usage Pattern

```python
import termforge as tf

# 1. Create a spec
spec = tf.CardSpec(title="My Card", content="Hello world")

# 2. Render via tf.draw() (easiest) — returns a printable string
print(tf.draw(spec))

# 3. Or render via tf.render() for a list of lines
lines = tf.render(spec, width=50, height=8)
```

## Categories

- [Display](display.md) — Card, Badge, Text, Toast, Tooltip, Divider
- [Input](input.md) — ButtonGroup, Checklist, Combobox, Radio, Slider, Toggle, SearchBar
- [Layout](layout.md) — Windows, Panes, Dialog, Accordion, Tabs
- [Charts](charts.md) — Line, Bar, Scatter, Sparkline, Heatmap, Candlestick

# API Reference

## Top-Level (`termforge`)

### `tf.draw(spec, width=80, height=24, theme=None, depth=None) -> str`

Render any component spec to a printable multi-line string.

```python
import termforge as tf
print(tf.draw(tf.CardSpec(title="Hi", content="Hello")))
```

### `tf.render(spec, width=80, height=24, theme=None, depth=None) -> list[str]`

Render any component spec to a list of ANSI-formatted strings (one per row).

```python
lines = tf.render(tf.CardSpec(title="Hi", content="Hello"), width=50, height=6)
```

### Arguments

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `spec` | `RenderableSpec` | — | Any component spec (e.g. `CardSpec`) |
| `width` | `int` | `80` | Canvas width in columns |
| `height` | `int` | `24` | Canvas height in rows |
| `theme` | `ThemeTokens \| None` | `None` | Theme tokens; defaults to Tokyo Night |
| `depth` | `ColorDepth \| None` | `None` | Color depth; auto-detected if `None` |

### Default Theme

When `theme` is `None`, TermForge uses Tokyo Night. To obtain those tokens
explicitly:

```python
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT
theme = load_theme_from_dict(TOKYO_NIGHT)
```

## Specs

All specs follow the pattern `tf.<Name>Spec(...)` and expose `.to_dict()` /
`.from_dict()` for JSON serialization. Refer to each component's section in
[Components](components/index.md) for field details.

## Capabilities

```python
from termforge.core.capability import detect_capabilities
caps = detect_capabilities()
print(caps.color_depth)  # auto-detected terminal color depth
```

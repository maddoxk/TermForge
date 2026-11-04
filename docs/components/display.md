# Display Components

Components for presenting information. Each example builds a spec and renders it with `tf.draw()`.

## Card

A bordered panel with an optional title, subtitle, and body content.

```python
import termforge as tf

print(tf.draw(tf.CardSpec(
    title="Server Node-01",
    subtitle="us-east-1",
    content="CPU: 42%\nRAM: 8.2 GB\nStatus: healthy",
    width=36,
)))
```

## Badge

A compact status label with a severity color.

```python
import termforge as tf

print(tf.draw(tf.BadgeSpec(text="ACTIVE", severity="success")))
print(tf.draw(tf.BadgeSpec(text="DEGRADED", severity="warning")))
print(tf.draw(tf.BadgeSpec(text="OFFLINE", severity="error")))
```

## Text

Aligned, wrapped text with overflow control.

```python
import termforge as tf

print(tf.draw(tf.TextSpec(
    content="TermForge renders rich text with alignment and wrapping.",
    align="center",
    max_width=40,
), width=40))
```

## Toast

A transient notification bubble.

```python
import termforge as tf

print(tf.draw(tf.ToastSpec(text="File saved successfully", toast_type="success")))
```

## Tooltip

A pointer bubble anchored to a coordinate.

```python
import termforge as tf

print(tf.draw(tf.TooltipSpec(text="Press Enter to confirm", anchor_x=4, anchor_y=0)))
```

## Divider

A horizontal rule with an optional centered label.

```python
import termforge as tf

print(tf.draw(tf.DividerSpec(label="SETTINGS", alignment="center", width=40), width=40))
```

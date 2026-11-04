# Layout Components

Components for structuring the screen — windows, split panes, dialogs, and collapsible sections.

## Windows

A bordered, titled region with scrollable content.

```python
import termforge as tf

print(tf.draw(tf.WindowSpec(
    title="Logs",
    content="[12:00] boot complete\n[12:01] listening on :8080",
    width=48,
    height=6,
), width=48, height=6))
```

## Panes

Split layouts that compose child windows horizontally or vertically.

```python
import termforge as tf

left = tf.WindowSpec(title="Nav", content="Home\nDocs\nAbout")
right = tf.WindowSpec(title="Content", content="Welcome to TermForge")

pane = tf.PaneSpec(direction="horizontal", children=[left, right], ratios=[1, 2])
print(tf.draw(pane, width=60, height=8))
```

## Dialog

A modal prompt with a title, body, and focusable buttons.

```python
import termforge as tf

print(tf.draw(tf.DialogSpec(
    title="Confirm",
    body="Delete this file? This cannot be undone.",
    buttons=["Cancel", "Delete"],
    focused_button_index=1,
), width=48, height=8))
```

## Accordion

A vertical list of collapsible sections.

```python
import termforge as tf

print(tf.draw(tf.AccordionSpec(
    items=[
        tf.AccordionItemSpec(title="General", details="Theme, language", is_expanded=True),
        tf.AccordionItemSpec(title="Advanced", details="Flags, env vars"),
    ],
    selected_idx=0,
)))
```

## Tabs

A horizontal tab strip with one active tab.

```python
import termforge as tf

print(tf.draw(tf.TabSpec(titles=["Overview", "Metrics", "Logs"], active_index=1), width=48))
```

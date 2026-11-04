# Input Components

Components that represent interactive controls. Specs are stateless — you hold selection state (e.g. `selected_idx`) in your own application and re-render on change.

## ButtonGroup

A horizontal row of buttons with one selected.

```python
import termforge as tf

print(tf.draw(tf.ButtonGroupSpec(
    buttons=["Save", "Cancel", "Reset"],
    selected_idx=0,
)))
```

## Checklist

A multi-item list with checked/unchecked state and a cursor.

```python
import termforge as tf

print(tf.draw(tf.ChecklistSpec(
    items=[
        tf.ChecklistItemSpec(label="Enable logging", checked=True),
        tf.ChecklistItemSpec(label="Verbose output", checked=False),
    ],
    selected_idx=0,
)))
```

## Combobox

A single-select dropdown.

```python
import termforge as tf

print(tf.draw(tf.ComboboxSpec(
    options=["Python", "Rust", "Go"],
    selected_idx=0,
    is_open=True,
)))
```

## Radio

A single-select group of options.

```python
import termforge as tf

print(tf.draw(tf.RadioButtonSpec(
    items=[
        tf.RadioButtonItemSpec(label="Light"),
        tf.RadioButtonItemSpec(label="Dark"),
    ],
    selected_idx=1,
)))
```

## Slider

A value slider between a min and max.

```python
import termforge as tf

print(tf.draw(tf.SliderSpec(value=65, min_val=0, max_val=100, label="Volume", width=40), width=40))
```

## Toggle

An on/off switch.

```python
import termforge as tf

print(tf.draw(tf.ToggleSwitchSpec(label="Dark mode", state=True)))
```

## SearchBar

A query field with filtered candidates.

```python
import termforge as tf

print(tf.draw(tf.SearchBarSpec(
    query="dra",
    candidates=["dracula", "gruvbox", "nord"],
    placeholder="Search themes...",
)))
```

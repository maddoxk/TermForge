# Quick Start

## Your First Component

```python
import termforge as tf

# Render a card
print(tf.draw(tf.CardSpec(title="Hello", content="Welcome to TermForge!")))
```

## Using Themes

```python
import termforge as tf
from termforge.theme.builtin import BUILTIN_THEMES

# Load a theme (keys: catppuccin_mocha, dracula, tokyo_night, nord, gruvbox, high_contrast)
theme = BUILTIN_THEMES["catppuccin_mocha"].tokens

# Apply it to any component
print(tf.draw(tf.BadgeSpec(text="SUCCESS", severity="success"), theme=theme))
```

## Declarative Config

```yaml
# layout.yaml
type: window
title: Dashboard
width: 60
height: 10
content: "System status: OK"
```

```python
from termforge.config.loader import load_config_yaml
specs = load_config_yaml("layout.yaml")
```

## CLI Tools

```bash
termforge-demo        # Flagship TUI dashboard
termforge-play        # Interactive Python REPL
termforge-layout      # Layout visualizer
termforge-benchmark   # Rendering performance test
```

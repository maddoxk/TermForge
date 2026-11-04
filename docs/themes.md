# Themes

TermForge ships 6 built-in themes.

## Available Themes

| Theme | Key | Style |
|-------|-----|-------|
| Catppuccin Mocha | `catppuccin_mocha` | Pastel dark |
| Dracula | `dracula` | High-contrast dark |
| Tokyo Night | `tokyo_night` | Blue-toned dark |
| Nord | `nord` | Arctic cool |
| Gruvbox | `gruvbox` | Warm retro |
| High Contrast | `high_contrast` | Accessibility |

## Usage

```python
import termforge as tf
from termforge.theme.builtin import BUILTIN_THEMES

theme = BUILTIN_THEMES["catppuccin_mocha"].tokens
print(tf.draw(tf.BadgeSpec(text="OK", severity="success"), theme=theme))
```

## Default Theme

Tokyo Night is applied automatically when no theme is provided. You can also
build its tokens directly:

```python
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT

theme = load_theme_from_dict(TOKYO_NIGHT)
```

## Custom Themes

Themes are plain dicts loaded via `load_theme_from_dict`:

```python
from termforge.core.theme import load_theme_from_dict

my_theme = load_theme_from_dict({
    "colors": {
        "primary": [100, 200, 255],
        "secondary": [180, 150, 255],
        # ...
    }
})
```

# TermForge Animation Specification

This specification defines spinners, transition formulas (fade, slide, wipe), and progress ticks.

## 1. Data Structures

### `SpinnerStyle`
Enum of spinner sequences. Supported styles include:
- `DOTS` = `["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]`
- `LINE` = `["-","\\","|","/"]`
- `BRAILLE` = `["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]`
- `BOUNCE`, `CLOCK`, `MOON`, `ARROWS`, `PULSE`

### `SpinnerSpec`
- `style`: `SpinnerStyle`
- `label`: string | null
- `fps`: float
- `color_token`: string

### `TransitionType`
Enum of transition movements:
- `FADE` — Line characters cross-fade their color stops.
- `SLIDE_LEFT` / `SLIDE_RIGHT` — Shift characters horizontally.
- `SLIDE_UP` / `SLIDE_DOWN` — Shift lines vertically.
- `WIPE` — Horizontal wipe from left to right.

### `TransitionSpec`
- `transition_type`: `TransitionType`
- `duration_ms`: float
- `from_content`: list of strings
- `to_content`: list of strings

---

## 2. Algorithms

### Cross-Fade Transition (`render_fade`)
To perform a fade in terminal systems:
1. Deconstruct both old and new lines into list of character tuples: `(char, style)`.
2. Pad both lists to match the maximum width.
3. For progress $t \in [0.0, 1.0]$:
   - If $t < 0.5$: Render the old character, and interpolate its style color towards the background color (surface token) by factor $2t$.
   - If $t \ge 0.5$: Render the new character, and interpolate its style color from the background color to its target color by factor $2(t - 0.5)$.

### Wipe Transition (`render_wipe`)
1. Determine current index `wipe_x = int(progress * width)`.
2. For each line, return the first `wipe_x` characters from the new line, and the remaining characters from the old line.

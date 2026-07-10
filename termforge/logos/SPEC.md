# TermForge Logos Specification

This specification defines ASCII art fonts, horizontal and vertical gradient rendering, and custom banners.

## 1. Data Structures

### `LogoSpec`
- `text`: string
- `font`: string (e.g. "small", "standard", "slant")
- `color_token`: string
- `gradient`: list of strings (color tokens or hex values) | null

---

## 2. Algorithms

### Text Art Layout
1. For each character in the string, fetch its 3-line or 5-line string list representation from the font dictionary.
2. Join character lines horizontally to produce the final line buffer.

### Multi-Stop Color Gradient (`get_gradient_color`)
Given $N$ colors and a progress $t \in [0.0, 1.0]$:
1. Divide $[0, 1]$ range into $N-1$ segments.
2. The active segment index is $idx = \lfloor t \times (N - 1) \rfloor$, clamped to $[0, N-2]$.
3. The local segment progress is $t_{local} = (t \times (N - 1)) - idx$.
4. Linearly interpolate between `colors[idx]` and `colors[idx + 1]` using $t_{local}$.

### Horizontal Gradient (`apply_gradient`)
For each row of text art:
1. For each character column index `col_idx`:
   - Compute progress $t = \frac{col\_idx}{width - 1}$.
   - Get the gradient color $C$ for progress $t$.
   - Wrap the character at `col_idx` with ANSI foreground code for $C$.
2. Append Reset ANSI code to the end of each row.

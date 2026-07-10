# TermForge Theme Specification

This specification defines ThemeMeta, ThemePack, WCAG relative luminance contrast calculation, and JSON/YAML serialization.

## 1. Data Structures

### `ThemeMeta`
Metadata for a theme pack.
- `name`: string
- `author`: string
- `version`: string
- `description`: string
- `dark`: boolean

### `ThemePack`
- `meta`: `ThemeMeta`
- `tokens`: `ThemeTokens` (from core)

---

## 2. Algorithms

### WCAG Relative Luminance
Relative luminance is calculated per standard sRGB Rec. 709:
$$L = 0.2126R_{linear} + 0.7152G_{linear} + 0.0722B_{linear}$$
Where the linear conversion is:
$$C_{linear} = \begin{cases} 
      \frac{C_{srgb}}{12.92} & C_{srgb} \le 0.04045 \\
      \left(\frac{C_{srgb} + 0.055}{1.055}\right)^{2.4} & C_{srgb} > 0.04045 
   \end{cases}$$
where $C_{srgb} = \frac{C}{255}$ for each color component $C \in \{R, G, B\}$.

### Contrast Ratio
The contrast ratio of two colors is calculated as:
$$\text{Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05}$$
where $L_1$ is the relative luminance of the lighter color and $L_2$ is the relative luminance of the darker color.
- AA check passes if $\text{Ratio} \ge 4.5$.
- AAA check passes if $\text{Ratio} \ge 7.0$.

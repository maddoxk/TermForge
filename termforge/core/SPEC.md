# TermForge Core — Language-Agnostic Specification

> This document describes every data type, function, and algorithm in
> `termforge.core` using pseudocode and examples. It is the primary
> reference for porting to Go, Rust, or TypeScript.

---

## Table of Contents

1. [Data Types](#1-data-types)
2. [Capability Detection](#2-capability-detection)
3. [Color Resolution](#3-color-resolution)
4. [Theme Token System](#4-theme-token-system)
5. [Box-Model Layout Engine](#5-box-model-layout-engine)
6. [Animation Tick Scheduler](#6-animation-tick-scheduler)
7. [Spec Diff / Change Detection](#7-spec-diff--change-detection)
8. [Component Event Hooks](#8-component-event-hooks)

---

## 1. Data Types

### ColorDepth (enum)
Terminal color depth tiers, ordered from highest to lowest fidelity.

| Value       | Description                  |
|-------------|------------------------------|
| TRUECOLOR   | 24-bit RGB (16.7M colors)    |
| COLOR_256   | 256-color palette            |
| COLOR_16    | 16 standard ANSI colors      |
| MONOCHROME  | No color (bold/dim only)     |

### ColorValue
Stores a color as an RGB triple with an optional semantic name.

| Field | Type          | Description                          |
|-------|---------------|--------------------------------------|
| r     | int (0-255)   | Red channel                          |
| g     | int (0-255)   | Green channel                        |
| b     | int (0-255)   | Blue channel                         |
| name  | string | null | Optional semantic name (e.g. "primary") |

**Serialization:**
```json
{"r": 137, "g": 180, "b": 250, "name": "blue"}
```

### Size
Width × height in character cells.

| Field  | Type | Description        |
|--------|------|--------------------|
| width  | int  | Width in columns   |
| height | int  | Height in rows     |

### Position
(x, y) position, origin at top-left (0, 0).

| Field | Type | Description      |
|-------|------|------------------|
| x     | int  | Column offset    |
| y     | int  | Row offset       |

### Spacing
Used for padding and margin (CSS-like order: top, right, bottom, left).

| Field  | Type | Default | Description  |
|--------|------|---------|--------------|
| top    | int  | 0       | Top spacing  |
| right  | int  | 0       | Right spacing|
| bottom | int  | 0       | Bottom spacing|
| left   | int  | 0       | Left spacing |

**Derived properties:**
- `horizontal = left + right`
- `vertical = top + bottom`

### BoxConstraints
Min/max width and height constraints passed into layout.

| Field      | Type | Default | Description         |
|------------|------|---------|---------------------|
| min_width  | int  | 0       | Minimum width       |
| max_width  | int  | 0       | Maximum width       |
| min_height | int  | 0       | Minimum height      |
| max_height | int  | 0       | Maximum height      |

### LayoutResult
Result of layout computation — absolute positions in a tree.

| Field    | Type             | Description                    |
|----------|------------------|--------------------------------|
| position | Position         | Absolute (x, y) position       |
| size     | Size             | Computed width × height        |
| children | list[LayoutResult] | Child layout results (recursive) |

### RenderableSpec
Base spec that all component specs inherit from.

| Field     | Type   | Default | Description                    |
|-----------|--------|---------|--------------------------------|
| spec_type | string | "base"  | Identifies the component type  |

All concrete component specs extend this with additional fields while preserving `spec_type`.

### StyleSpec
Text styling specification.

| Field         | Type            | Default | Description               |
|---------------|-----------------|---------|---------------------------|
| fg            | ColorValue|null | null    | Foreground color          |
| bg            | ColorValue|null | null    | Background color          |
| bold          | bool            | false   | Bold text                 |
| dim           | bool            | false   | Dimmed text               |
| italic        | bool            | false   | Italic text               |
| underline     | bool            | false   | Underlined text           |
| strikethrough | bool            | false   | Strikethrough text        |

---

## 2. Capability Detection

### detect_color_depth() → ColorDepth

Detects the terminal's color depth from environment variables.

```
function detect_color_depth():
    colorterm = env("COLORTERM").lowercase()
    if colorterm in ["truecolor", "24bit"]:
        return TRUECOLOR

    term = env("TERM").lowercase()
    if colorterm == "256color" or term contains "256color":
        return COLOR_256

    if term is not empty and term != "dumb":
        return COLOR_16

    return MONOCHROME
```

### detect_terminal_size() → Size

```
function detect_terminal_size():
    try:
        (cols, rows) = os.get_terminal_size()
        return Size(width=cols, height=rows)
    catch:
        return Size(width=80, height=24)
```

### detect_unicode_support() → bool

```
function detect_unicode_support():
    for var in ["LC_ALL", "LANG", "LC_CTYPE"]:
        if env(var).lowercase() contains "utf":
            return true
    return false
```

### TerminalCapabilities
Aggregated result of all detection functions.

| Field           | Type       | Description              |
|-----------------|------------|--------------------------|
| color_depth     | ColorDepth | Detected color depth     |
| size            | Size       | Terminal dimensions      |
| unicode_support | bool       | UTF-8 support detected   |

---

## 3. Color Resolution

### ANSI_16_COLORS

The 16 standard ANSI terminal colors as RGB tuples:

| Index | Name           | RGB              |
|-------|----------------|------------------|
| 0     | Black          | (0, 0, 0)       |
| 1     | Red            | (128, 0, 0)     |
| 2     | Green          | (0, 128, 0)     |
| 3     | Yellow         | (128, 128, 0)   |
| 4     | Blue           | (0, 0, 128)     |
| 5     | Magenta        | (128, 0, 128)   |
| 6     | Cyan           | (0, 128, 128)   |
| 7     | White          | (192, 192, 192) |
| 8     | Bright Black   | (128, 128, 128) |
| 9     | Bright Red     | (255, 0, 0)     |
| 10    | Bright Green   | (0, 255, 0)     |
| 11    | Bright Yellow  | (255, 255, 0)   |
| 12    | Bright Blue    | (0, 0, 255)     |
| 13    | Bright Magenta | (255, 0, 255)   |
| 14    | Bright Cyan    | (0, 255, 255)   |
| 15    | Bright White   | (255, 255, 255) |

### color_distance(c1, c2) → float

Euclidean distance in RGB space.

```
function color_distance(c1: (r,g,b), c2: (r,g,b)):
    return sqrt((c1.r - c2.r)² + (c1.g - c2.g)² + (c1.b - c2.b)²)
```

**Example:** `color_distance((0,0,0), (255,255,255))` ≈ 441.67

### The 256-Color Palette

The 256-color palette consists of three regions:
1. **Indices 0–15:** The 16 standard ANSI colors (see above)
2. **Indices 16–231:** A 6×6×6 color cube. Channel values: `[0, 95, 135, 175, 215, 255]`. Index = `16 + 36*r_idx + 6*g_idx + b_idx`
3. **Indices 232–255:** A 24-step grayscale ramp. Value = `8 + 10 * (index - 232)`

### resolve_color(color, depth) → (r,g,b) | null

```
function resolve_color(color: ColorValue, depth: ColorDepth):
    rgb = (color.r, color.g, color.b)

    if depth == TRUECOLOR:
        return rgb

    if depth == COLOR_256:
        return nearest_match(rgb, palette_256)

    if depth == COLOR_16:
        return nearest_match(rgb, ANSI_16_COLORS)

    // MONOCHROME
    return null

function nearest_match(target, palette):
    best = palette[0]
    best_dist = infinity
    for each color in palette:
        d = color_distance(target, color)
        if d < best_dist:
            best_dist = d
            best = color
        if d == 0:
            break
    return best
```

**Example:**
```
resolve_color(ColorValue(137, 180, 250), COLOR_256) → (135, 175, 255)
resolve_color(ColorValue(255, 0, 0), COLOR_16) → (255, 0, 0)
resolve_color(ColorValue(100, 200, 50), MONOCHROME) → null
```

### interpolate_color(c1, c2, t) → ColorValue

Linear interpolation for animations.

```
function interpolate_color(c1, c2, t):
    t = clamp(t, 0.0, 1.0)
    r = round(c1.r + (c2.r - c1.r) * t)
    g = round(c1.g + (c2.g - c1.g) * t)
    b = round(c1.b + (c2.b - c1.b) * t)
    return ColorValue(r, g, b)
```

**Example:** `interpolate_color(CV(0,0,0), CV(200,100,50), 0.5)` → `CV(100,50,25)`

---

## 4. Theme Token System

### ThemeTokens

| Field        | Type                             | Description                          |
|--------------|----------------------------------|--------------------------------------|
| colors       | dict[string, ColorValue]         | Named colors (primary, secondary…)   |
| spacing      | dict[string, int]                | Spacing scale (xs, sm, md, lg, xl)   |
| border_glyphs| dict[string, dict[string,string]]| Named glyph sets (single, rounded…)  |
| typography   | dict[string, bool]               | Supported text decorations           |

**Default spacing scale:**

| Token | Value |
|-------|-------|
| xs    | 1     |
| sm    | 2     |
| md    | 4     |
| lg    | 8     |
| xl    | 16    |

**Border glyph keys:** `tl, tr, bl, br, h, v, t_down, t_up, t_right, t_left, cross`

**Typography keys:** `bold_supported, dim_supported, italic_supported`

### resolve_token(tokens, path) → Any

Dot-notation lookup into ThemeTokens.

```
function resolve_token(tokens: ThemeTokens, path: string):
    parts = path.split(".")
    if len(parts) < 2:
        raise KeyError

    category = parts[0]  // e.g. "colors"
    obj = tokens[category]
    for part in parts[1:]:
        obj = obj[part]
    return obj
```

**Examples:**
```
resolve_token(tokens, "colors.primary")        → ColorValue(137, 180, 250, "blue")
resolve_token(tokens, "spacing.md")            → 4
resolve_token(tokens, "border_glyphs.rounded.tl") → "╭"
resolve_token(tokens, "typography.bold_supported") → true
```

### Built-in Themes

Four themes are provided as serializable dicts:

| Theme             | Surface      | Primary        | Text            |
|-------------------|-------------|----------------|-----------------|
| Catppuccin Mocha  | (30,30,46)  | (137,180,250)  | (205,214,244)   |
| Dracula           | (40,42,54)  | (189,147,249)  | (248,248,242)   |
| Tokyo Night       | (26,27,38)  | (122,162,247)  | (192,202,245)   |
| High Contrast     | (0,0,0)     | (0,255,255)    | (255,255,255)   |

Each theme includes all 8 color tokens (primary, secondary, surface, text,
error, warning, success, border), the default spacing scale, 4 border glyph
sets (single, double, rounded, ascii), and typography support flags.

---

## 5. Box-Model Layout Engine

### BoxModel

| Field       | Type         | Default | Description                    |
|-------------|-------------|---------|--------------------------------|
| margin      | Spacing     | all 0   | Outer spacing                  |
| padding     | Spacing     | all 0   | Inner spacing                  |
| width       | int | null  | null    | Explicit width (null = auto)   |
| height      | int | null  | null    | Explicit height (null = auto)  |
| flex_grow   | float       | 0.0     | Flex grow factor               |
| flex_shrink | float       | 1.0     | Flex shrink factor             |

### FlexDirection (enum)

| Value  | Description              |
|--------|--------------------------|
| ROW    | Main axis is horizontal  |
| COLUMN | Main axis is vertical    |

### FlexContainer

| Field     | Type          | Default | Description                |
|-----------|---------------|---------|----------------------------|
| direction | FlexDirection | ROW     | Main axis direction        |
| gap       | int           | 0       | Space between children     |
| wrap      | bool          | false   | Whether children can wrap  |

### LayoutNode

| Field    | Type               | Description                        |
|----------|--------------------|------------------------------------|
| spec     | RenderableSpec     | The component spec for this node   |
| box      | BoxModel           | Box-model properties               |
| flex     | FlexContainer|null | Flex properties (null = leaf node)  |
| children | list[LayoutNode]   | Child nodes                        |

### compute_layout(node, constraints) → LayoutResult

The core layout algorithm:

```
function compute_layout(node, constraints):
    return _compute(node, constraints, Position(0, 0))

function _compute(node, constraints, offset):
    margin = node.box.margin
    padding = node.box.padding

    // Step 1: Apply margin to get inner origin
    inner_x = offset.x + margin.left
    inner_y = offset.y + margin.top
    avail_w = max(0, constraints.max_width - margin.horizontal)
    avail_h = max(0, constraints.max_height - margin.vertical)

    // Step 2: Determine own size
    own_w = node.box.width ?? avail_w
    own_h = node.box.height ?? avail_h
    own_w = clamp(own_w, constraints.min_width, avail_w)
    own_h = clamp(own_h, constraints.min_height, avail_h)

    // Step 3: Leaf node — just return size
    if no children or no flex container:
        return LayoutResult(
            position = Position(inner_x, inner_y),
            size = Size(own_w, own_h)
        )

    // Step 4: Flex container — distribute space
    is_row = (flex.direction == ROW)
    content_w = max(0, own_w - padding.horizontal)
    content_h = max(0, own_h - padding.vertical)
    total_gap = gap * (num_children - 1)
    main_available = (content_w if is_row else content_h) - total_gap

    // Step 5: Measure base sizes (explicit width/height + margin)
    for each child:
        if is_row:
            base_size = (child.box.width + child.margin.horizontal) ?? 0
        else:
            base_size = (child.box.height + child.margin.vertical) ?? 0
        total_flex_grow += child.box.flex_grow

    // Step 6: Distribute remaining space
    used = sum(base_sizes)
    remaining = max(0, main_available - used)

    // Step 7: Compute each child's layout
    cursor_x = inner_x + padding.left
    cursor_y = inner_y + padding.top

    for each child:
        extra = remaining * (child.flex_grow / total_flex_grow) if total_flex_grow > 0
        child_main_size = base_size + extra

        if is_row:
            child_constraints = BoxConstraints(0, child_main_size, 0, content_h)
            result = _compute(child, child_constraints, Position(cursor_x, cursor_y))
            cursor_x += result.size.width + child.margin.horizontal + gap
        else:
            child_constraints = BoxConstraints(0, content_w, 0, child_main_size)
            result = _compute(child, child_constraints, Position(cursor_x, cursor_y))
            cursor_y += result.size.height + child.margin.vertical + gap

    return LayoutResult(
        position = Position(inner_x, inner_y),
        size = Size(own_w, own_h),
        children = child_results
    )
```

**Example — 3-column row layout:**
```
Input:
  Container: width=60, height=10, flex=ROW, gap=2
  Children: 3 × { flex_grow=1.0 }

Output:
  Container: pos=(0,0), size=60×10
  Child 0: pos=(0,0), size=18×10
  Child 1: pos=(20,0), size=18×10
  Child 2: pos=(40,0), size=18×10
```

---

## 6. Animation Tick Scheduler

### AnimationSpec

| Field       | Type         | Description                         |
|-------------|-------------|--------------------------------------|
| fps         | float       | Target frames per second             |
| duration_ms | float|null  | Total duration in ms (null=infinite) |
| callback_id | string      | Unique identifier for this animation |

### SchedulerState (immutable)

| Field        | Type                        | Description                      |
|--------------|-----------------------------|----------------------------------|
| animations   | dict[string, AnimationSpec] | Registered animations            |
| frame_counts | dict[string, int]           | Current frame number per anim    |
| start_times  | dict[string, float]         | Start time in ms per anim        |

All functions return a **new** SchedulerState — the original is never mutated.

### create_scheduler() → SchedulerState

Returns an empty state.

### register_animation(state, spec) → SchedulerState

Adds the animation to state with frame_count=0 and start_time=-1 (not yet started).

### unregister_animation(state, callback_id) → SchedulerState

Removes the animation from state.

### tick(state, current_time_ms) → (SchedulerState, list[string])

The core scheduling algorithm:

```
function tick(state, current_time_ms):
    fired = []

    for each (callback_id, spec) in state.animations:
        start = state.start_times[callback_id]

        // Initialize start time on first tick
        if start < 0:
            start = current_time_ms
            state.start_times[callback_id] = current_time_ms

        elapsed = current_time_ms - start

        // Check if animation has expired
        if spec.duration_ms != null and elapsed >= spec.duration_ms:
            remove animation from state
            continue

        // Compute expected frame number
        expected_frame = floor(elapsed * spec.fps / 1000.0)

        // Fire if we've advanced past the current frame
        if expected_frame > state.frame_counts[callback_id]:
            fired.append(callback_id)
            state.frame_counts[callback_id] = expected_frame

    return (new_state, fired)
```

**Example:**
```
state = create_scheduler()
state = register_animation(state, AnimationSpec(fps=10, duration_ms=5000, id="spin"))

state, fired = tick(state, 0.0)     // fired = [] (initializes start)
state, fired = tick(state, 50.0)    // fired = [] (too early for frame 1)
state, fired = tick(state, 100.0)   // fired = ["spin"] (frame 1)
state, fired = tick(state, 150.0)   // fired = [] (still on frame 1)
state, fired = tick(state, 200.0)   // fired = ["spin"] (frame 2)
state, fired = tick(state, 5100.0)  // fired = [] ("spin" removed, past duration)
```

### is_animation_complete(state, callback_id, current_time_ms) → bool

```
function is_animation_complete(state, callback_id, current_time_ms):
    if callback_id not in state.animations:
        return true  // not registered = complete

    spec = state.animations[callback_id]
    if spec.duration_ms == null:
        return false  // infinite = never complete

    start = state.start_times[callback_id]
    if start < 0:
        return false  // not started yet

    return (current_time_ms - start) >= spec.duration_ms
```


---

## 7. Spec Diff / Change Detection

A system for recursively detecting differences between two `RenderableSpec` dictionary trees (snapshots) to support incremental rendering, debugging, and precise testing.

### ChangeKind (enum)
- `ADDED`: Present in the target dict but not the source.
- `REMOVED`: Present in the source dict but not the target.
- `MODIFIED`: Present in both dicts but has different values or types.

### SpecChange
Stores a structural leaf change.

| Field | Type | Description |
|-------|------|-------------|
| path  | string | Dot-separated path to the field (e.g. `children.0.title`) |
| kind  | ChangeKind | The change classification |
| old   | Any | The old value (or null if ADDED) |
| new   | Any | The new value (or null if REMOVED) |

### diff_specs(a, b, path="") → list[SpecChange]

Walks the keys of `a` and `b` recursively.
- If a key exists only in `a`, adds a `REMOVED` change.
- If a key exists only in `b`, adds an `ADDED` change.
- If a key exists in both:
  - If types differ, adds a `MODIFIED` change.
  - If both are lists, compares index-by-index recursively.
  - If both are dicts, compares keys recursively.
  - If they are primitive values and differ, adds a `MODIFIED` change.

---

## 8. Component Event Hooks

Allows passive specs to attach callback identifiers that trigger dynamic modifications at key lifecycle phases (e.g., prior to render or after resizing).

### HookPhase (enum)
- `PRE_RENDER`: Fires before compiling spec to layout.
- `POST_RENDER`: Fires after compilation is finished.
- `ON_RESIZE`: Fires when the terminal size changes.
- `ON_FOCUS`: Fires when a window gains focus.
- `ON_BLUR`: Fires when focus is lost.

### RenderHook

| Field | Type | Description |
|-------|------|-------------|
| phase | HookPhase | The execution phase |
| callback_id | string | String identifier for looking up the callback |
| priority | int | Sorting order (highest executes first) |

### invoke_hooks(hooks, phase, registry, spec, context) → list[dict]

Filters the hooks matching the phase, sorts them by priority descending, resolves the callable from the registry via `callback_id`, and executes the callback with `(spec, context)`. Returns the list of patch dictionaries.

---

## Portability Contract

All types in this module follow these rules:

1. **JSON-serializable:** Every dataclass has `to_dict()` → `from_dict()` round-trip
2. **No Rich/Textual imports:** Zero dependency on any rendering library
3. **No metaclasses or magic:** Plain dataclasses/structs only
4. **Pure functions:** All business logic is stateless; functions take inputs and return outputs
5. **Immutable scheduler:** SchedulerState is frozen; every operation returns a new state
6. **No execution baked into specs:** Callbacks are resolved at runtime via string identifiers to preserve portability


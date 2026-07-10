from __future__ import annotations
from termforge.core.types import ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.core.color import interpolate_color
from termforge.text.types import TextRun, TextSpan
from termforge.text.markup import parse_markup, strip_markup
from termforge.text.render import style_to_ansi, render_text
from termforge.animation.types import TransitionSpec, TransitionType

def line_to_tuples(line: str) -> list[tuple[str, StyleSpec | None]]:
    # Convert string (which might contain markup or ANSI) to (char, style)
    # If it is an ANSI string, we can strip it for simple transitions, 
    # but let's parse it using parse_markup if it contains markup,
    # or just treat it as plain text if it contains raw ANSI.
    # To be extremely clean, we can assume inputs to transitions are plain strings (or markup).
    # Let's parse as markup first to extract styles
    run = parse_markup(line)
    tuples = []
    for span in run.spans:
        for c in span.text:
            tuples.append((c, span.style))
    return tuples

def tuples_to_ansi(tuples: list[tuple[str, StyleSpec | None]], theme: ThemeTokens | None, depth: ColorDepth) -> str:
    parts = []
    current_style = None
    current_text = ""
    for c, style in tuples:
        if style == current_style:
            current_text += c
        else:
            if current_text:
                start_ansi, end_ansi = style_to_ansi(current_style, theme, depth)
                parts.append(f"{start_ansi}{current_text}{end_ansi}")
            current_text = c
            current_style = style
    if current_text:
        start_ansi, end_ansi = style_to_ansi(current_style, theme, depth)
        parts.append(f"{start_ansi}{current_text}{end_ansi}")
    return "".join(parts)

def render_fade(
    from_tuples: list[tuple[str, StyleSpec | None]],
    to_tuples: list[tuple[str, StyleSpec | None]],
    progress: float,
    theme: ThemeTokens | None = None
) -> list[tuple[str, StyleSpec | None]]:
    # Find background color for fading
    bg_color = ColorValue(0, 0, 0)
    if theme and theme.colors:
        surf = theme.colors.get("surface")
        if surf:
            bg_color = surf
            
    max_len = max(len(from_tuples), len(to_tuples))
    # Pad both to max_len
    from_padded = from_tuples + [(" ", None)] * (max_len - len(from_tuples))
    to_padded = to_tuples + [(" ", None)] * (max_len - len(to_tuples))
    
    result: list[tuple[str, StyleSpec | None]] = []
    for i in range(max_len):
        c_from, style_from = from_padded[i]
        c_to, style_to = to_padded[i]
        
        # Base styles
        sf = style_from if style_from else StyleSpec()
        st = style_to if style_to else StyleSpec()
        
        # Base colors (fallback to white/bg)
        fg_from = sf.fg if sf.fg else ColorValue(255, 255, 255)
        fg_to = st.fg if st.fg else ColorValue(255, 255, 255)
        
        if progress < 0.5:
            # Fade out from_tuples
            t = progress * 2.0 # 0.0 to 1.0
            interp_fg = interpolate_color(fg_from, bg_color, t)
            # Create style
            new_style = StyleSpec(
                fg=interp_fg,
                bg=sf.bg, # keep bg static or we could fade it too
                bold=sf.bold, dim=sf.dim, italic=sf.italic
            )
            result.append((c_from, new_style))
        else:
            # Fade in to_tuples
            t = (progress - 0.5) * 2.0 # 0.0 to 1.0
            interp_fg = interpolate_color(bg_color, fg_to, t)
            new_style = StyleSpec(
                fg=interp_fg,
                bg=st.bg,
                bold=st.bold, dim=st.dim, italic=st.italic
            )
            result.append((c_to, new_style))
            
    return result

def render_slide(
    from_tuples: list[tuple[str, StyleSpec | None]],
    to_tuples: list[tuple[str, StyleSpec | None]],
    progress: float,
    direction: TransitionType
) -> list[tuple[str, StyleSpec | None]]:
    width = max(len(from_tuples), len(to_tuples))
    from_padded = from_tuples + [(" ", None)] * (width - len(from_tuples))
    to_padded = to_tuples + [(" ", None)] * (width - len(to_tuples))
    
    shift = int(progress * width)
    
    if direction == TransitionType.SLIDE_LEFT:
        return from_padded[shift:] + to_padded[:shift]
    elif direction == TransitionType.SLIDE_RIGHT:
        return to_padded[width - shift :] + from_padded[: width - shift]
        
    return to_padded # Fallback

def render_wipe(
    from_tuples: list[tuple[str, StyleSpec | None]],
    to_tuples: list[tuple[str, StyleSpec | None]],
    progress: float
) -> list[tuple[str, StyleSpec | None]]:
    width = max(len(from_tuples), len(to_tuples))
    from_padded = from_tuples + [(" ", None)] * (width - len(from_tuples))
    to_padded = to_tuples + [(" ", None)] * (width - len(to_tuples))
    
    wipe_x = int(progress * width)
    return to_padded[:wipe_x] + from_padded[wipe_x:]

def render_transition(
    spec: TransitionSpec,
    progress: float,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR
) -> list[str]:
    # Ensure progress is clamped to 0..1
    progress = max(0.0, min(1.0, progress))
    
    from_lines = spec.from_content
    to_lines = spec.to_content
    max_rows = max(len(from_lines), len(to_lines))
    
    # Pad rows
    from_lines_padded = from_lines + [""] * (max_rows - len(from_lines))
    to_lines_padded = to_lines + [""] * (max_rows - len(to_lines))
    
    # Vertical slides (shift rows instead of columns)
    if spec.transition_type == TransitionType.SLIDE_UP:
        shift_rows = int(progress * max_rows)
        combined_rows = from_lines_padded[shift_rows:] + to_lines_padded[:shift_rows]
        return combined_rows
    elif spec.transition_type == TransitionType.SLIDE_DOWN:
        shift_rows = int(progress * max_rows)
        combined_rows = to_lines_padded[max_rows - shift_rows :] + from_lines_padded[: max_rows - shift_rows]
        return combined_rows
        
    # Column/pixel-level transitions
    rendered_lines = []
    for r in range(max_rows):
        from_tuples = line_to_tuples(from_lines_padded[r])
        to_tuples = line_to_tuples(to_lines_padded[r])
        
        if spec.transition_type == TransitionType.FADE:
            trans_tuples = render_fade(from_tuples, to_tuples, progress, theme)
        elif spec.transition_type == TransitionType.WIPE:
            trans_tuples = render_wipe(from_tuples, to_tuples, progress)
        else: # SLIDE_LEFT / SLIDE_RIGHT
            trans_tuples = render_slide(from_tuples, to_tuples, progress, spec.transition_type)
            
        rendered_lines.append(tuples_to_ansi(trans_tuples, theme, depth))
        
    return rendered_lines

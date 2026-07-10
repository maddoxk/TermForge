from __future__ import annotations
from termforge.core.types import ColorDepth, StyleSpec, ColorValue
from termforge.core.color import resolve_color, ANSI_16_COLORS, _PALETTE_256
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.types import TextSpec, TextRun, TextAlign, TextOverflow, TextSpan
from termforge.text.markup import parse_markup
from termforge.text.wrap import wrap_run, measure_text, get_string_width

def style_to_ansi(style: StyleSpec | None, theme: ThemeTokens | None, depth: ColorDepth) -> tuple[str, str]:
    if not style or depth == ColorDepth.MONOCHROME:
        return "", ""
        
    start_codes = []
    end_codes = []
    
    # Resolve color tokens
    fg = style.fg
    bg = style.bg
    
    if theme:
        if fg and fg.name and fg.name.startswith("colors."):
            resolved = resolve_token(theme, fg.name)
            if isinstance(resolved, ColorValue):
                fg = resolved
                
        if bg and bg.name and bg.name.startswith("colors."):
            resolved = resolve_token(theme, bg.name)
            if isinstance(resolved, ColorValue):
                bg = resolved

    # FG resolution
    if fg:
        rgb = resolve_color(fg, depth)
        if rgb:
            if depth == ColorDepth.TRUECOLOR:
                start_codes.append(f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m")
            elif depth == ColorDepth.COLOR_256:
                try:
                    idx = _PALETTE_256.index(rgb)
                    start_codes.append(f"\033[38;5;{idx}m")
                except ValueError:
                    start_codes.append(f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m")
            elif depth == ColorDepth.COLOR_16:
                try:
                    idx = ANSI_16_COLORS.index(rgb)
                    if idx < 8:
                        start_codes.append(f"\033[{30 + idx}m")
                    else:
                        start_codes.append(f"\033[{90 + (idx - 8)}m")
                except ValueError:
                    pass

    # BG resolution
    if bg:
        rgb = resolve_color(bg, depth)
        if rgb:
            if depth == ColorDepth.TRUECOLOR:
                start_codes.append(f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m")
            elif depth == ColorDepth.COLOR_256:
                try:
                    idx = _PALETTE_256.index(rgb)
                    start_codes.append(f"\033[48;5;{idx}m")
                except ValueError:
                    start_codes.append(f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m")
            elif depth == ColorDepth.COLOR_16:
                try:
                    idx = ANSI_16_COLORS.index(rgb)
                    if idx < 8:
                        start_codes.append(f"\033[{40 + idx}m")
                    else:
                        start_codes.append(f"\033[{100 + (idx - 8)}m")
                except ValueError:
                    pass

    # Attributes
    if style.bold:
        start_codes.append("\033[1m")
        end_codes.append("\033[22m")
    if style.dim:
        start_codes.append("\033[2m")
        end_codes.append("\033[22m")
    if style.italic:
        start_codes.append("\033[3m")
        end_codes.append("\033[23m")
    if style.underline:
        start_codes.append("\033[4m")
        end_codes.append("\033[24m")
    if style.strikethrough:
        start_codes.append("\033[9m")
        end_codes.append("\033[29m")
        
    if start_codes:
        end_codes.append("\033[0m")
        
    return "".join(start_codes), "".join(reversed(end_codes))

def render_text(spec: TextSpec, theme: ThemeTokens | None = None, depth: ColorDepth = ColorDepth.TRUECOLOR, available_width: int | None = None) -> list[str]:
    # 1. Parse content to TextRun
    if isinstance(spec.content, str):
        run = parse_markup(spec.content)
    else:
        run = spec.content
        
    # 2. Determine target width
    width = spec.max_width
    if width is None:
        width = available_width
    if width is None:
        # Default fallback if width is completely unspecified
        width = 80
        
    # 3. Handle word wrapping / truncation
    lines: list[TextRun] = []
    if spec.overflow == TextOverflow.WRAP:
        lines = wrap_run(run, width)
    elif spec.overflow == TextOverflow.ELLIPSIS or spec.overflow == TextOverflow.CLIP:
        # Truncate content to width
        from termforge.text.wrap import truncate_text
        # We can convert run to plain text, truncate, and then reconstruct a simple TextRun
        plain = "".join(span.text for span in run.spans)
        suffix = "…" if spec.overflow == TextOverflow.ELLIPSIS else ""
        truncated = truncate_text(plain, width, suffix)
        
        # Build a single TextRun with the truncated content and the original styles
        # Let's map truncated chars to original styles
        chars: list[tuple[str, StyleSpec | None]] = []
        for span in run.spans:
            for c in span.text:
                chars.append((c, span.style))
        
        truncated_chars = chars[:len(truncated)]
        # If truncated has suffix, give the suffix the style of the last char or None
        if len(truncated) > len(truncated_chars):
            last_style = chars[-1][1] if chars else None
            for s_char in suffix:
                truncated_chars.append((s_char, last_style))
                
        # Reconstruct TextRun
        spans = []
        current_span_text = ""
        current_span_style = None
        for c, style in truncated_chars:
            if style == current_span_style:
                current_span_text += c
            else:
                if current_span_text:
                    spans.append(TextSpan(text=current_span_text, style=current_span_style))
                current_span_text = c
                current_span_style = style
        if current_span_text:
            spans.append(TextSpan(text=current_span_text, style=current_span_style))
            
        lines = [TextRun(spans=spans)]
        
    # 4. Handle max_lines limit
    if spec.max_lines is not None:
        lines = lines[:spec.max_lines]
        
    # 5. Format each line (alignment & ANSI codes)
    rendered_lines = []
    for line in lines:
        line_w = measure_text(line)
        # Compute padding
        pad_left = 0
        pad_right = 0
        if line_w < width:
            if spec.align == TextAlign.CENTER:
                total_pad = width - line_w
                pad_left = total_pad // 2
                pad_right = total_pad - pad_left
            elif spec.align == TextAlign.RIGHT:
                pad_left = width - line_w
                
        # Render spans
        line_ansi = " " * pad_left
        for span in line.spans:
            if not span.text:
                continue
            start_ansi, end_ansi = style_to_ansi(span.style, theme, depth)
            line_ansi += f"{start_ansi}{span.text}{end_ansi}"
        line_ansi += " " * pad_right
        rendered_lines.append(line_ansi)
        
    return rendered_lines

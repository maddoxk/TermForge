from __future__ import annotations
from termforge.core.types import StyleSpec, ColorValue, ColorDepth
from termforge.core.theme import ThemeTokens
from termforge.text.render import style_to_ansi
from termforge.animation.types import SpinnerSpec, SpinnerStyle

SPINNER_FRAMES: dict[SpinnerStyle, list[str]] = {
    SpinnerStyle.DOTS: ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    SpinnerStyle.LINE: ["-", "\\", "|", "/"],
    SpinnerStyle.BRAILLE: ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"],
    SpinnerStyle.BOUNCE: ["⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"],
    SpinnerStyle.CLOCK: ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"],
    SpinnerStyle.MOON: ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"],
    SpinnerStyle.ARROWS: ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
    SpinnerStyle.PULSE: ["█", "▉", "▊", "▋", "▌", "▍", "▎", "▏", " ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"]
}

def get_spinner_frame(style: SpinnerStyle, frame_number: int) -> str:
    frames = SPINNER_FRAMES.get(style, SPINNER_FRAMES[SpinnerStyle.DOTS])
    return frames[frame_number % len(frames)]

def render_spinner(
    spec: SpinnerSpec,
    frame_number: int,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR
) -> str:
    frame = get_spinner_frame(spec.style, frame_number)
    
    style = StyleSpec(fg=ColorValue(0, 0, 0, name=f"colors.{spec.color_token}"))
    start_ansi, end_ansi = style_to_ansi(style, theme, depth)
    
    styled_frame = f"{start_ansi}{frame}{end_ansi}"
    if spec.label:
        return f"{styled_frame} {spec.label}"
    return styled_frame

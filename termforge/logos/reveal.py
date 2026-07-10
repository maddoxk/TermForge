from __future__ import annotations
from termforge.core.types import ColorDepth
from termforge.core.theme import ThemeTokens
from termforge.animation.types import TransitionSpec, TransitionType
from termforge.animation.transitions import render_transition
from termforge.borders.render import strip_ansi
from termforge.logos.types import LogoSpec, BannerSpec
from termforge.logos.render import render_logo
from termforge.logos.banner import render_banner

def render_logo_reveal(
    spec: LogoSpec | BannerSpec,
    transition_type: TransitionType,
    progress: float,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR
) -> list[str]:
    # 1. Render base logo content
    if isinstance(spec, BannerSpec):
        to_content = render_banner(spec, theme, depth)
    else:
        to_content = render_logo(spec, theme, depth)
        
    if not to_content:
        return []
        
    # 2. Build matching empty content
    from_content = []
    for line in to_content:
        from_content.append(" " * len(strip_ansi(line)))
        
    # 3. Build TransitionSpec and render it
    trans_spec = TransitionSpec(
        transition_type=transition_type,
        from_content=from_content,
        to_content=to_content
    )
    
    return render_transition(trans_spec, progress, theme, depth)

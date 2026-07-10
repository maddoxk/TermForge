from __future__ import annotations
from termforge.core.types import ColorDepth, ColorValue, StyleSpec
from termforge.text.render import style_to_ansi
from termforge.theme.types import ThemePack
from termforge.theme.contrast import check_contrast

def render_theme_preview(theme: ThemePack, depth: ColorDepth = ColorDepth.TRUECOLOR) -> list[str]:
    lines = []
    
    meta = theme.meta
    tokens = theme.tokens
    
    # 1. Header
    lines.append(f"=== Theme Preview: {meta.name} ===")
    lines.append(f"Author:      {meta.author}")
    lines.append(f"Description: {meta.description}")
    lines.append("")
    
    # 2. Color Palette
    lines.append("--- Color Palette ---")
    for name, val in tokens.colors.items():
        # Render a colored box
        style = StyleSpec(fg=val, bg=val)
        start_ansi, end_ansi = style_to_ansi(style, tokens, depth)
        hex_val = f"#{val.r:02x}{val.g:02x}{val.b:02x}"
        lines.append(f"  {start_ansi}    {end_ansi}  {name:<12} {hex_val} (RGB: {val.r},{val.g},{val.b})")
    lines.append("")
    
    # 3. Contrast Check
    lines.append("--- Contrast Audit (vs Surface) ---")
    lines.append("  Token        │ Ratio │ AA   │ AAA")
    lines.append("  ─────────────┼───────┼──────┼─────")
    
    contrast_results = check_contrast(theme)
    for res in contrast_results:
        aa = "PASS" if res["passes_aa"] else "FAIL"
        aaa = "PASS" if res["passes_aaa"] else "FAIL"
        
        # Color code the pass/fail
        green = "\033[32m"
        red = "\033[31m"
        reset = "\033[0m"
        
        aa_color = green if res["passes_aa"] else red
        aaa_color = green if res["passes_aaa"] else red
        
        aa_str = f"{aa_color}{aa:<4}{reset}"
        aaa_str = f"{aaa_color}{aaa:<4}{reset}"
        
        lines.append(f"  {res['fg_token']:<12} │ {res['ratio']:<5} │ {aa_str} │ {aaa_str}")
        
    return lines

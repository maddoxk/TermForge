from __future__ import annotations

# Alphanumeric character mappings for 3 fonts
# Key: char, Value: list of strings (height = 3 or 5)

FONT_SMALL: dict[str, list[str]] = {
    "T": ["┌┬┐", " │ ", " ┴ "],
    "E": ["├─ ", "├─ ", "└─⠂"],
    "R": ["├─┐", "├┬┘", "┴└─"],
    "M": ["┌┐┌┐", "│└┘│", "┴  ┴"],
    "F": ["├─ ", "├─ ", "┴  "],
    "O": ["┌─┐", "│ │", "└─┘"],
    "G": ["┌─┐", "│ ┬", "└─┘"],
    "S": ["┌─ ", "└─┐", " ─┘"],
    "A": ["┌─┐", "├─┤", "┴ ┴"],
    "N": ["┌┐ ", "│││", "┘└┘"],
    "D": ["├─┐", "│ │", "└─┘"],
    "L": ["│  ", "│  ", "└──"],
    " ": ["   ", "   ", "   "]
}

# Standard block font (height 5)
FONT_STANDARD: dict[str, list[str]] = {
    "T": ["███████", "   █   ", "   █   ", "   █   ", "   █   "],
    "E": ["███████", "█      ", "█████  ", "█      ", "███████"],
    "R": ["██████ ", "█     █", "██████ ", "█   █  ", "█    █ "],
    "M": ["██   ██", "███ ███", "█ █ █ █", "█   █ █", "█   █ █"],
    "F": ["███████", "█      ", "█████  ", "█      ", "█      "],
    "O": [" █████ ", "█     █", "█     █", "█     █", " █████ "],
    "G": [" █████ ", "█      ", "█  ████", "█     █", " █████ "],
    "S": [" ██████", "█      ", " █████ ", "      █", "██████ "],
    "A": ["  ███  ", " █   █ ", "███████", "█     █", "█     █"],
    "N": ["██    █", "███   █", "█ █   █", "█  █  █", "█   ███"],
    "D": ["██████ ", "█     █", "█     █", "█     █", "██████ "],
    "L": ["█      ", "█      ", "█      ", "█      ", "███████"],
    " ": ["       ", "       ", "       ", "       ", "       "]
}

# Slant font (height 5)
FONT_SLANT: dict[str, list[str]] = {
    "T": ["  ████████ ", "  __  ██  _", "     ██    ", "    ██     ", "   ██      "],
    "E": [" ████████ ", " ██       ", " ██████   ", " ██       ", " ████████ "],
    "R": [" ███████  ", " ██    ██ ", " ███████  ", " ██   ██  ", " ██    ██ "],
    "M": [" ██      ██ ", " ███    ███ ", " ██ ██ ██ ██", " ██  ██  ██", " ██      ██"],
    "F": [" ████████ ", " ██       ", " ██████   ", " ██       ", " ██       "],
    "O": ["   ██████  ", "  ██    ██ ", " ██      ██", "  ██    ██ ", "   ██████  "],
    "G": ["   ██████  ", "  ██    __ ", " ██   ████ ", "  ██    ██ ", "   ██████  "],
    "S": ["  ███████ ", " ██       ", "  ██████  ", "       ██ ", " ███████  "],
    "A": ["   ████   ", "  ██  ██  ", " ████████ ", " ██    ██ ", " ██    ██ "],
    "N": [" ██    ██ ", " ███   ██ ", " ██ ██ ██ ", " ██  ████ ", " ██    ██ "],
    "D": [" ███████  ", " ██    ██ ", " ██    ██ ", " ██    ██ ", " ███████  "],
    "L": [" ██       ", " ██       ", " ██       ", " ██       ", " ████████ "],
    " ": ["          ", "          ", "          ", "          ", "          "]
}

# Create fallback representations for letters not in FONT dicts
def get_char_art(char: str, font_name: str) -> list[str]:
    c = char.upper()
    if font_name == "small":
        if c in FONT_SMALL:
            return FONT_SMALL[c]
        # fallback simple representation
        return [f"{c}  ", f"{c}  ", f"{c}  "]
    elif font_name == "slant":
        if c in FONT_SLANT:
            return FONT_SLANT[c]
        return [f" {c}  ", f" {c}  ", f" {c}  ", f" {c}  ", f" {c}  "]
    else: # standard
        if c in FONT_STANDARD:
            return FONT_STANDARD[c]
        return [f" {c}  ", f" {c}  ", f" {c}  ", f" {c}  ", f" {c}  "]

def render_text_art(text: str, font_name: str = "standard") -> list[str]:
    if not text:
        return []
        
    font_name = font_name.lower()
    height = 3 if font_name == "small" else 5
    
    # Initialize empty line buffers
    lines = [""] * height
    
    for idx, char in enumerate(text):
        char_lines = get_char_art(char, font_name)
        for r in range(height):
            # Pad between letters
            sep = " " if idx > 0 else ""
            lines[r] += sep + char_lines[r]
            
    return lines

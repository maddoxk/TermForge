from termforge.text import TextSpec, TextOverflow, render_text
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT
from termforge.core.types import Size

def main():
    theme = load_theme_from_dict(TOKYO_NIGHT)
    
    spec = TextSpec(
        content="TermForge marquee animation ticker feature is now live!",
        overflow=TextOverflow.MARQUEE,
        max_width=25
    )
    
    print("--- Marquee Ticker Scrolling Showcase ---")
    for frame in [0, 5, 12, 22]:
        result = render_text(spec, theme=theme, available_width=25, frame_number=frame)
        print(f"Frame {frame:02d}: |{result[0]}|")

if __name__ == "__main__":
    main()

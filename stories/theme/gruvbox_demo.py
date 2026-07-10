from termforge.core.theme import load_theme_from_dict, GRUVBOX
from termforge.progress import ProgressSpec, render_progress
from termforge.core.types import Size

def main():
    theme = load_theme_from_dict(GRUVBOX)
    
    # Render progress bar using Gruvbox theme with custom color_config override
    spec = ProgressSpec(
        progress=0.75,
        color_config={
            "filled": "secondary",  # aqua
            "empty": "primary"      # gold
        }
    )
    
    result = render_progress(spec, Size(40, 1), theme)
    print("--- Gruvbox Theme Custom Progress Bar ---")
    print(result[0])

if __name__ == "__main__":
    main()

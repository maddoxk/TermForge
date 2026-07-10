from termforge.progress import ProgressSpec, render_progress
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT
from termforge.core.types import Size

def main():
    theme = load_theme_from_dict(TOKYO_NIGHT)
    
    specs = [
        ProgressSpec(progress=0.0, width=40),
        ProgressSpec(progress=0.5, width=40, head_char=">"),
        ProgressSpec(progress=1.0, width=40)
    ]
    
    for spec in specs:
        result = render_progress(spec, Size(40, 1), theme)
        print("\n".join(result))

if __name__ == "__main__":
    main()

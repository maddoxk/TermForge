from termforge.tabs import TabSpec, render_tabs
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT
from termforge.core.types import Size

def main():
    theme = load_theme_from_dict(TOKYO_NIGHT)
    
    spec = TabSpec(
        titles=["Overview", "Logs", "Settings"],
        active_index=0
    )
    
    result = render_tabs(spec, Size(40, 5), theme)
    print("\n".join(result))

if __name__ == "__main__":
    main()

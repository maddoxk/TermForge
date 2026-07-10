from termforge.dialog import DialogSpec, render_dialog
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT
from termforge.core.types import Size

def main():
    theme = load_theme_from_dict(TOKYO_NIGHT)
    
    spec = DialogSpec(
        title="Exit Confirmation",
        body="Are you sure you want to exit the application?",
        buttons=["Yes", "No"],
        focused_button_index=1
    )
    
    result = render_dialog(spec, Size(48, 6), theme)
    print("\n".join(result))

if __name__ == "__main__":
    main()

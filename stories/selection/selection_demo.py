from termforge.selection import SelectionListSpec, SelectionItemSpec, render_selection_list
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT
from termforge.core.types import Size

def main():
    theme = load_theme_from_dict(TOKYO_NIGHT)
    
    spec = SelectionListSpec(
        items=[
            SelectionItemSpec(label="Item A", selected=True),
            SelectionItemSpec(label="Item B", selected=False),
            SelectionItemSpec(label="Item C", selected=True),
        ],
        focused_index=1
    )
    
    result = render_selection_list(spec, Size(40, 10), theme)
    print("\n".join(result))

if __name__ == "__main__":
    main()

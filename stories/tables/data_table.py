from termforge.tables import TableSpec, ColumnSpec, render_table
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT
from termforge.core.types import Size
from termforge.text.types import TextAlign

def main():
    theme = load_theme_from_dict(TOKYO_NIGHT)
    spec = TableSpec(
        columns=[
            ColumnSpec(title="ID", width=4, align=TextAlign.RIGHT),
            ColumnSpec(title="Name", align=TextAlign.LEFT),
            ColumnSpec(title="Status", align=TextAlign.CENTER)
        ],
        rows=[
            ["1", "Alice", "Active"],
            ["2", "Bob", "Inactive"],
            ["100", "Charlie", "Pending"],
        ]
    )
    
    result = render_table(spec, Size(80, 20), theme)
    print("\n".join(result))

if __name__ == "__main__":
    main()

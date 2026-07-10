import pytest
from termforge.tables.types import TableSpec, ColumnSpec
from termforge.tables.render import render_table
from termforge.core.types import Size
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT
from termforge.text.types import TextAlign

def test_column_spec_serialization():
    col = ColumnSpec(title="Age", width=5, align=TextAlign.CENTER, padding_left=2, padding_right=3)
    d = col.to_dict()
    assert d["title"] == "Age"
    assert d["width"] == 5
    assert d["align"] == "center"
    assert d["padding_left"] == 2
    assert d["padding_right"] == 3

    col2 = ColumnSpec.from_dict(d)
    assert col2.title == "Age"
    assert col2.width == 5
    assert col2.align == TextAlign.CENTER
    assert col2.padding_left == 2
    assert col2.padding_right == 3

def test_render_table_with_padding():
    theme = load_theme_from_dict(TOKYO_NIGHT)
    spec = TableSpec(
        columns=[
            ColumnSpec(title="A", padding_left=2, padding_right=1),
            ColumnSpec(title="B", padding_left=1, padding_right=2)
        ],
        rows=[
            ["1", "2"]
        ]
    )
    result = render_table(spec, Size(80, 20), theme)
    # col 0: inner_w=1, title="A" -> content="A" -> padded="  A "
    # col 1: inner_w=1, title="B" -> content="B" -> padded=" B  "
    # Join with " │ ":
    # header: "  A  │  B  " (Wait: "  A " + " │ " + " B  " = "  A  │  B  ")
    # separator: outer_w = 4 and 4 -> "────┼────"
    # row 0: "  1  │  2  "
    assert result[0] == "  A  │  B  "
    assert result[1] == "─────┼─────"
    assert result[2] == "  1  │  2  "

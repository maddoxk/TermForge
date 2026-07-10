"""Tests for Selection List — Issue #131: Custom Spacing and Alignment Settings."""
from termforge.core.types import Size
from termforge.core.theme import load_theme_from_dict, CATPPUCCIN_MOCHA
from termforge.selection.types import SelectionListSpec, SelectionItemSpec
from termforge.selection.render import render_selection_list
from termforge.text.types import TextAlign


def _make_theme():
    return load_theme_from_dict(CATPPUCCIN_MOCHA)


def _make_spec(**kwargs):
    items = [
        SelectionItemSpec(label="Option A"),
        SelectionItemSpec(label="Option B", selected=True),
        SelectionItemSpec(label="Option C"),
    ]
    return SelectionListSpec(items=items, focused_index=0, **kwargs)


def test_default_alignment_is_left():
    spec = _make_spec()
    assert spec.item_align == TextAlign.LEFT
    assert spec.item_spacing == 0


def test_serialization_roundtrip_defaults():
    spec = _make_spec()
    d = spec.to_dict()
    assert d["item_align"] == "left"
    assert d["item_spacing"] == 0
    spec2 = SelectionListSpec.from_dict(d)
    assert spec2.item_align == TextAlign.LEFT
    assert spec2.item_spacing == 0


def test_serialization_roundtrip_center():
    spec = _make_spec(item_align=TextAlign.CENTER, item_spacing=1)
    d = spec.to_dict()
    assert d["item_align"] == "center"
    assert d["item_spacing"] == 1
    spec2 = SelectionListSpec.from_dict(d)
    assert spec2.item_align == TextAlign.CENTER
    assert spec2.item_spacing == 1


def test_right_alignment():
    spec = _make_spec(item_align=TextAlign.RIGHT)
    theme = _make_theme()
    size = Size(width=20, height=10)
    lines = render_selection_list(spec, size, theme)
    # Focused item has '> [ ] ' prefix (6 chars), label padded to right in remaining 14 chars
    focused_line = lines[0]
    # Label 'Option A' should be right-aligned in available space
    # prefix = "> [ ] " (6 chars), rest is 14 chars wide
    rest = focused_line[6:]
    assert rest == "Option A".rjust(14)


def test_center_alignment():
    spec = _make_spec(item_align=TextAlign.CENTER)
    theme = _make_theme()
    size = Size(width=20, height=10)
    lines = render_selection_list(spec, size, theme)
    focused_line = lines[0]
    rest = focused_line[6:]
    assert rest == "Option A".center(14)


def test_item_spacing_inserts_blank_lines():
    spec = _make_spec(item_spacing=1)
    theme = _make_theme()
    size = Size(width=30, height=20)
    lines = render_selection_list(spec, size, theme)
    # With 3 items and spacing=1, we get: item, blank, item, blank, item = 5 lines
    assert len(lines) == 5
    assert lines[1] == ""
    assert lines[3] == ""


def test_item_spacing_2():
    spec = _make_spec(item_spacing=2)
    theme = _make_theme()
    size = Size(width=30, height=20)
    lines = render_selection_list(spec, size, theme)
    # 3 items, 2 blanks between each: item, blank, blank, item, blank, blank, item = 7
    assert len(lines) == 7
    assert lines[1] == ""
    assert lines[2] == ""


def test_height_limit_respected_with_spacing():
    spec = _make_spec(item_spacing=2)
    theme = _make_theme()
    # Height of 4 means only first item + 2 blanks + half of second
    size = Size(width=30, height=4)
    lines = render_selection_list(spec, size, theme)
    assert len(lines) <= 4


def test_truncation_still_works():
    spec = _make_spec()
    theme = _make_theme()
    size = Size(width=10, height=10)
    lines = render_selection_list(spec, size, theme)
    for line in lines:
        assert len(line) <= 10

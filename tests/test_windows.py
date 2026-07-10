import pytest
from termforge.core import Size, FlexDirection
from termforge.windows.types import WindowSpec, PaneSpec, ModalSpec
from termforge.windows.compositor import compose_panes, apply_scroll, z_sort, render_window

def test_window_types_serialization():
    spec = WindowSpec(title="Dashboard", focused=True, z_index=2)
    spec_dict = spec.to_dict()
    assert spec_dict["spec_type"] == "window"
    assert spec_dict["title"] == "Dashboard"
    assert spec_dict["focused"] is True
    assert spec_dict["z_index"] == 2
    
    spec_back = WindowSpec.from_dict(spec_dict)
    assert spec_back.title == "Dashboard"
    assert spec_back.focused is True
    assert spec_back.z_index == 2

    pane = PaneSpec(direction=FlexDirection.COLUMN, ratios=[1.0, 2.0], gap=1)
    pane_dict = pane.to_dict()
    assert pane_dict["direction"] == "column"
    assert pane_dict["ratios"] == [1.0, 2.0]
    assert pane_dict["gap"] == 1

def test_compose_panes_row():
    # 2 children split 1:2, width 32, height 10, gap 2
    # gaps space = 2
    # rem_w = 30 -> child 0 gets 10, child 1 gets 20
    child0 = WindowSpec(title="C0")
    child1 = WindowSpec(title="C1")
    pane = PaneSpec(direction=FlexDirection.ROW, children=[child0, child1], ratios=[1.0, 2.0], gap=2)
    
    results = compose_panes(pane, Size(32, 10))
    assert len(results) == 2
    
    pos0, size0, spec0 = results[0]
    assert pos0.x == 0
    assert size0.width == 10
    assert size0.height == 10
    
    pos1, size1, spec1 = results[1]
    assert pos1.x == 12 # 10 + gap 2
    assert size1.width == 20
    assert size1.height == 10

def test_apply_scroll():
    content = ["1", "2", "3", "4", "5"]
    # Viewport height = 3
    assert apply_scroll(content, 0, 3) == ["1", "2", "3"]
    assert apply_scroll(content, 2, 3) == ["3", "4", "5"]
    assert apply_scroll(content, 4, 3) == ["3", "4", "5"] # clamps to end

def test_z_sort():
    w1 = WindowSpec(title="w1", z_index=5)
    w2 = WindowSpec(title="w2", z_index=1)
    w3 = WindowSpec(title="w3", z_index=10)
    sorted_ws = z_sort([w1, w2, w3])
    assert sorted_ws[0].title == "w2"
    assert sorted_ws[1].title == "w1"
    assert sorted_ws[2].title == "w3"

def test_render_window_scroll():
    spec = WindowSpec(title="ScrollBox", width=10, height=5, scroll_y=2)
    content = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
    lines = render_window(spec, content)
    # width=10, height=5 -> inner_w=8, inner_h=3
    # scroll_y=2 means lines 2..4 (Line 3, Line 4, Line 5)
    assert len(lines) == 5
    assert "Line 3" in lines[1]
    assert "Line 4" in lines[2]
    assert "Line 5" in lines[3]

def test_window_drop_shadow():
    spec = WindowSpec(title="ShadowBox", width=10, height=5, shadow=True)
    content = ["Content 1", "Content 2", "Content 3"]
    lines = render_window(spec, content)
    assert len(lines) == 6
    assert lines[5].startswith("  ")
    assert "█" in lines[5]

def test_window_padding_serialization():
    """WindowSpec.padding and .margin round-trip through to_dict/from_dict."""
    spec = WindowSpec(title="Padded", padding=2, margin=1)
    d = spec.to_dict()
    assert d["padding"] == 2
    assert d["margin"] == 1
    spec2 = WindowSpec.from_dict(d)
    assert spec2.padding == 2
    assert spec2.margin == 1

def test_window_padding_shrinks_inner_area():
    """Inner padding with padding=1 on a 12x8 window should still produce 12 wide output."""
    spec = WindowSpec(title="PadTest", width=12, height=8, padding=1)
    content = ["Hello", "World"]
    lines = render_window(spec, content)
    # Total height = 8 (no margin); width = 12
    assert len(lines) == 8
    # Strip ANSI for plain width measurement
    import re
    for line in lines:
        plain = re.sub(r'\x1b\[[^m]*m', '', line)
        assert len(plain) == 12, f"Expected 12, got {len(plain)}: {repr(plain)}"

def test_window_margin_expands_outer_dimensions():
    """Outer margin=2 on a 10x5 window adds 2 rows top+bottom and 2 cols left+right."""
    spec = WindowSpec(title="MarginTest", width=10, height=5, margin=2)
    content = ["Line1", "Line2"]
    lines = render_window(spec, content)
    # Expected rows: 2 (top margin) + 5 (window) + 2 (bottom margin) = 9
    assert len(lines) == 9
    # Expected cols: 2 (left margin) + 10 (window) + 2 (right margin) = 14
    import re
    for line in lines:
        plain = re.sub(r'\x1b\[[^m]*m', '', line)
        assert len(plain) == 14, f"Expected 14, got {len(plain)}: {repr(plain)}"

def test_window_padding_and_margin_combined():
    """padding=1 + margin=1 work together without overlap."""
    spec = WindowSpec(title="Both", width=14, height=8, padding=1, margin=1)
    content = ["Content"]
    lines = render_window(spec, content)
    # rows: 1 (top margin) + 8 (window) + 1 (bottom margin) = 10
    assert len(lines) == 10
    import re
    for line in lines:
        plain = re.sub(r'\x1b\[[^m]*m', '', line)
        # cols: 1 (left margin) + 14 (window) + 1 (right margin) = 16
        assert len(plain) == 16, f"Expected 16, got {len(plain)}: {repr(plain)}"


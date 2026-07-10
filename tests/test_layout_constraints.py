import pytest
from termforge.core import (
    BoxConstraints,
    BoxModel,
    LayoutNode,
    LayoutConstraintError,
    RenderableSpec,
    compute_layout,
)
from termforge.core.layout import FlexContainer, FlexDirection

def test_invalid_min_max_constraints():
    node = LayoutNode(spec=RenderableSpec(spec_type="text"))
    with pytest.raises(LayoutConstraintError) as exc_info:
        compute_layout(node, BoxConstraints(min_width=50, max_width=40, min_height=0, max_height=10))
    assert "min_width 50 exceeds max_width 40" in str(exc_info.value)

def test_negative_dimensions():
    node = LayoutNode(spec=RenderableSpec(spec_type="text"), box=BoxModel(width=-5))
    with pytest.raises(LayoutConstraintError) as exc_info:
        compute_layout(node, BoxConstraints(0, 100, 0, 100))
    assert "Invalid negative width: -5" in str(exc_info.value)

def test_over_constrained_flex_row():
    # Parent row with max_width 20, containing two rigid child windows of width 15 and 10 (total 25)
    # flex_shrink is 0 for both children
    child1 = LayoutNode(spec=RenderableSpec(spec_type="window"), box=BoxModel(width=15, flex_shrink=0.0))
    child2 = LayoutNode(spec=RenderableSpec(spec_type="window"), box=BoxModel(width=10, flex_shrink=0.0))
    
    parent = LayoutNode(
        spec=RenderableSpec(spec_type="pane"),
        flex=FlexContainer(direction=FlexDirection.ROW),
        children=[child1, child2]
    )
    
    with pytest.raises(LayoutConstraintError) as exc_info:
        compute_layout(parent, BoxConstraints(0, 20, 0, 10))
    assert "Over-constrained row: Minimum required width 25 exceeds available width 20" in str(exc_info.value)

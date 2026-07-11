"""Tests for Issue #144: Spec Diff / Change Detection."""
import json
import pytest
from termforge.core.diff import (
    ChangeKind, SpecChange, diff_specs, has_changed, filter_changes
)


# ---------------------------------------------------------------------------
# SpecChange data model
# ---------------------------------------------------------------------------

def test_spec_change_to_dict():
    c = SpecChange(path="title", kind=ChangeKind.MODIFIED, old="Old", new="New")
    d = c.to_dict()
    assert d == {"path": "title", "kind": "modified", "old": "Old", "new": "New"}


def test_spec_change_from_dict():
    d = {"path": "width", "kind": "added", "old": None, "new": 80}
    c = SpecChange.from_dict(d)
    assert c.path == "width"
    assert c.kind == ChangeKind.ADDED
    assert c.old is None
    assert c.new == 80


def test_spec_change_json_roundtrip():
    c = SpecChange(path="children.0.title", kind=ChangeKind.REMOVED, old="X", new=None)
    d = c.to_dict()
    j = json.dumps(d)
    d2 = json.loads(j)
    c2 = SpecChange.from_dict(d2)
    assert c2.path == c.path
    assert c2.kind == c.kind
    assert c2.old == c.old


# ---------------------------------------------------------------------------
# diff_specs — flat dicts
# ---------------------------------------------------------------------------

def test_no_changes_identical():
    assert diff_specs({"x": 1, "y": 2}, {"x": 1, "y": 2}) == []


def test_modified_field():
    changes = diff_specs({"title": "Old"}, {"title": "New"})
    assert len(changes) == 1
    assert changes[0].path == "title"
    assert changes[0].kind == ChangeKind.MODIFIED
    assert changes[0].old == "Old"
    assert changes[0].new == "New"


def test_added_field():
    changes = diff_specs({"x": 1}, {"x": 1, "y": 2})
    assert len(changes) == 1
    assert changes[0].path == "y"
    assert changes[0].kind == ChangeKind.ADDED
    assert changes[0].old is None
    assert changes[0].new == 2


def test_removed_field():
    changes = diff_specs({"x": 1, "y": 2}, {"x": 1})
    assert len(changes) == 1
    assert changes[0].path == "y"
    assert changes[0].kind == ChangeKind.REMOVED
    assert changes[0].old == 2
    assert changes[0].new is None


def test_multiple_changes():
    a = {"title": "Old", "width": 80, "height": 24}
    b = {"title": "New", "width": 80, "height": 30}
    changes = diff_specs(a, b)
    assert len(changes) == 2
    paths = {c.path for c in changes}
    assert "title" in paths
    assert "height" in paths


def test_empty_dicts():
    assert diff_specs({}, {}) == []


def test_a_empty():
    changes = diff_specs({}, {"x": 1})
    assert len(changes) == 1
    assert changes[0].kind == ChangeKind.ADDED


def test_b_empty():
    changes = diff_specs({"x": 1}, {})
    assert len(changes) == 1
    assert changes[0].kind == ChangeKind.REMOVED


# ---------------------------------------------------------------------------
# diff_specs — nested dicts
# ---------------------------------------------------------------------------

def test_nested_modified():
    a = {"y_axis": {"min_val": 0.0, "max_val": 10.0}}
    b = {"y_axis": {"min_val": 0.0, "max_val": 20.0}}
    changes = diff_specs(a, b)
    assert len(changes) == 1
    assert changes[0].path == "y_axis.max_val"
    assert changes[0].old == 10.0
    assert changes[0].new == 20.0


def test_deeply_nested():
    a = {"a": {"b": {"c": 1}}}
    b = {"a": {"b": {"c": 2}}}
    changes = diff_specs(a, b)
    assert len(changes) == 1
    assert changes[0].path == "a.b.c"


def test_nested_no_change():
    a = {"border": {"style": "single", "title": "X"}}
    b = {"border": {"style": "single", "title": "X"}}
    assert diff_specs(a, b) == []


def test_path_prefix_in_result():
    changes = diff_specs({"x": 1}, {"x": 2}, path="parent")
    assert changes[0].path == "parent.x"


# ---------------------------------------------------------------------------
# diff_specs — lists
# ---------------------------------------------------------------------------

def test_list_element_modified():
    a = {"data": [1.0, 2.0, 3.0]}
    b = {"data": [1.0, 9.0, 3.0]}
    changes = diff_specs(a, b)
    assert len(changes) == 1
    assert changes[0].path == "data.1"
    assert changes[0].old == 2.0
    assert changes[0].new == 9.0


def test_list_element_added():
    a = {"data": [1.0, 2.0]}
    b = {"data": [1.0, 2.0, 3.0]}
    changes = diff_specs(a, b)
    assert len(changes) == 1
    assert changes[0].path == "data.2"
    assert changes[0].kind == ChangeKind.ADDED


def test_list_element_removed():
    a = {"data": [1.0, 2.0, 3.0]}
    b = {"data": [1.0, 2.0]}
    changes = diff_specs(a, b)
    assert len(changes) == 1
    assert changes[0].kind == ChangeKind.REMOVED


def test_list_no_change():
    a = {"tags": ["x", "y"]}
    b = {"tags": ["x", "y"]}
    assert diff_specs(a, b) == []


def test_nested_list_of_dicts():
    a = {"children": [{"title": "A", "width": 40}]}
    b = {"children": [{"title": "B", "width": 40}]}
    changes = diff_specs(a, b)
    assert len(changes) == 1
    assert changes[0].path == "children.0.title"


# ---------------------------------------------------------------------------
# diff_specs — type mismatch
# ---------------------------------------------------------------------------

def test_type_mismatch_treated_as_modified():
    a = {"x": 1}
    b = {"x": "one"}
    changes = diff_specs(a, b)
    assert len(changes) == 1
    assert changes[0].kind == ChangeKind.MODIFIED
    assert changes[0].old == 1
    assert changes[0].new == "one"


# ---------------------------------------------------------------------------
# diff_specs — ignore_keys
# ---------------------------------------------------------------------------

def test_ignore_keys():
    a = {"spec_type": "window", "title": "A"}
    b = {"spec_type": "pane",   "title": "A"}
    changes = diff_specs(a, b, ignore_keys=frozenset({"spec_type"}))
    assert changes == []


def test_ignore_keys_still_catches_other_changes():
    a = {"spec_type": "window", "title": "Old"}
    b = {"spec_type": "pane",   "title": "New"}
    changes = diff_specs(a, b, ignore_keys=frozenset({"spec_type"}))
    assert len(changes) == 1
    assert changes[0].path == "title"


# ---------------------------------------------------------------------------
# Real WindowSpec round-trip
# ---------------------------------------------------------------------------

def test_window_spec_diff():
    from termforge.windows.types import WindowSpec
    before = WindowSpec(title="Old", width=80, height=24)
    after  = WindowSpec(title="New", width=80, height=30)
    changes = diff_specs(before.to_dict(), after.to_dict())
    paths = {c.path for c in changes}
    assert "title" in paths
    assert "height" in paths
    assert "width" not in paths


def test_identical_window_specs_no_changes():
    from termforge.windows.types import WindowSpec
    spec = WindowSpec(title="Same", width=60, height=20)
    assert diff_specs(spec.to_dict(), spec.to_dict()) == []


def test_pane_spec_children_diff():
    from termforge.windows.types import WindowSpec, PaneSpec
    from termforge.core import FlexDirection
    child_a = WindowSpec(title="Child A", width=40, height=10)
    child_b = WindowSpec(title="Child B", width=40, height=10)
    pane_a = PaneSpec(direction=FlexDirection.ROW, children=[child_a])
    pane_b = PaneSpec(direction=FlexDirection.ROW, children=[child_b])
    changes = diff_specs(pane_a.to_dict(), pane_b.to_dict())
    child_title_change = [c for c in changes if "children.0.title" in c.path]
    assert len(child_title_change) == 1
    assert child_title_change[0].old == "Child A"
    assert child_title_change[0].new == "Child B"


# ---------------------------------------------------------------------------
# has_changed
# ---------------------------------------------------------------------------

def test_has_changed_false():
    assert not has_changed({"x": 1}, {"x": 1})


def test_has_changed_true():
    assert has_changed({"x": 1}, {"x": 2})


def test_has_changed_ignore_keys():
    assert not has_changed({"t": "a", "x": 1}, {"t": "b", "x": 1},
                           ignore_keys=frozenset({"t"}))


# ---------------------------------------------------------------------------
# filter_changes
# ---------------------------------------------------------------------------

def test_filter_by_kind():
    a = {"x": 1, "z": 3}
    b = {"x": 2, "y": 99}
    changes = diff_specs(a, b)
    mods = filter_changes(changes, kind=ChangeKind.MODIFIED)
    assert all(c.kind == ChangeKind.MODIFIED for c in mods)
    added = filter_changes(changes, kind=ChangeKind.ADDED)
    assert all(c.kind == ChangeKind.ADDED for c in added)


def test_filter_by_path_prefix():
    a = {"children": [{"title": "A"}], "title": "Root"}
    b = {"children": [{"title": "B"}], "title": "Root2"}
    changes = diff_specs(a, b)
    child_changes = filter_changes(changes, path_prefix="children")
    assert all(c.path.startswith("children") for c in child_changes)


def test_filter_combined():
    a = {"children": [{"title": "A"}], "width": 80}
    b = {"children": [{"title": "B"}], "width": 90}
    changes = diff_specs(a, b)
    results = filter_changes(changes, kind=ChangeKind.MODIFIED, path_prefix="width")
    assert len(results) == 1
    assert results[0].path == "width"


# ---------------------------------------------------------------------------
# Portability: full JSON round-trip of SpecChange list
# ---------------------------------------------------------------------------

def test_changes_list_fully_json_serializable():
    a = {"title": "Old", "width": 80, "children": [{"x": 1}]}
    b = {"title": "New", "width": 80, "children": [{"x": 2}], "extra": True}
    changes = diff_specs(a, b)
    serialized = json.dumps([c.to_dict() for c in changes])
    restored = [SpecChange.from_dict(d) for d in json.loads(serialized)]
    assert len(restored) == len(changes)
    for orig, rest in zip(changes, restored):
        assert orig.path == rest.path
        assert orig.kind == rest.kind

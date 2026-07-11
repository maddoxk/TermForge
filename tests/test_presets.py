"""Tests for Issue #138: Named Layout Presets / Template System."""
import pytest
from termforge.config.presets import get_preset, list_presets
from termforge.windows.types import WindowSpec, PaneSpec
from termforge.core import FlexDirection
from termforge.borders.types import BorderStyle
from termforge.text.types import TextOverflow


# ---------------------------------------------------------------------------
# list_presets
# ---------------------------------------------------------------------------

def test_list_presets_returns_all_five():
    presets = list_presets()
    names = {p["name"] for p in presets}
    assert "dashboard" in names
    assert "split-pane" in names
    assert "split-pane-v" in names
    assert "modal-dialog" in names
    assert "log-viewer" in names


def test_list_presets_have_descriptions():
    for p in list_presets():
        assert "name" in p
        assert "description" in p
        assert len(p["description"]) > 0


def test_get_preset_unknown_raises():
    with pytest.raises(ValueError, match="Unknown preset"):
        get_preset("nonexistent-preset")


# ---------------------------------------------------------------------------
# Preset: dashboard
# ---------------------------------------------------------------------------

def test_dashboard_preset_returns_pane():
    spec = get_preset("dashboard")
    assert isinstance(spec, PaneSpec)
    assert spec.direction == FlexDirection.COLUMN
    assert len(spec.children) == 3


def test_dashboard_preset_portability():
    """Dashboard spec must JSON-serialize and deserialize cleanly."""
    spec = get_preset("dashboard", title="MyApp", width=100, height=30)
    d = spec.to_dict()
    assert d["spec_type"] == "pane"
    assert d["direction"] == "column"
    # Roundtrip
    spec2 = PaneSpec.from_dict(d)
    assert spec2.direction == FlexDirection.COLUMN
    assert len(spec2.children) == 3


def test_dashboard_custom_params():
    spec = get_preset("dashboard", title="Admin", width=160, height=50,
                      header_text="Admin Panel", border_style="double")
    assert isinstance(spec, PaneSpec)
    header = spec.children[0]
    assert isinstance(header, WindowSpec)
    assert header.border_style == BorderStyle.DOUBLE


# ---------------------------------------------------------------------------
# Preset: split-pane
# ---------------------------------------------------------------------------

def test_split_pane_returns_row_pane():
    spec = get_preset("split-pane")
    assert isinstance(spec, PaneSpec)
    assert spec.direction == FlexDirection.ROW
    assert len(spec.children) == 2


def test_split_pane_portability():
    spec = get_preset("split-pane", ratios=[1, 2], gap=2,
                      left_title="Explorer", right_title="Editor")
    d = spec.to_dict()
    assert d["spec_type"] == "pane"
    assert d["ratios"] == [1, 2]
    assert d["gap"] == 2
    spec2 = PaneSpec.from_dict(d)
    assert spec2.ratios == [1, 2]


def test_split_pane_titles():
    spec = get_preset("split-pane", left_title="Files", right_title="Preview")
    left, right = spec.children
    assert isinstance(left, WindowSpec)
    assert isinstance(right, WindowSpec)
    assert left.title == "Files"
    assert right.title == "Preview"


# ---------------------------------------------------------------------------
# Preset: split-pane-v
# ---------------------------------------------------------------------------

def test_split_pane_v_returns_column_pane():
    spec = get_preset("split-pane-v")
    assert isinstance(spec, PaneSpec)
    assert spec.direction == FlexDirection.COLUMN
    assert len(spec.children) == 2


def test_split_pane_v_portability():
    spec = get_preset("split-pane-v", ratios=[2, 1], top_title="Code", bottom_title="Terminal")
    d = spec.to_dict()
    assert d["direction"] == "column"
    spec2 = PaneSpec.from_dict(d)
    assert spec2.ratios == [2, 1]


# ---------------------------------------------------------------------------
# Preset: modal-dialog
# ---------------------------------------------------------------------------

def test_modal_dialog_returns_window():
    spec = get_preset("modal-dialog")
    assert isinstance(spec, WindowSpec)


def test_modal_dialog_portability():
    spec = get_preset("modal-dialog", title="Confirm", message="Delete file?",
                      width=40, height=8, buttons=["Yes", "No"])
    d = spec.to_dict()
    assert d["spec_type"] == "window"
    assert d["title"] == "Confirm"
    assert "Yes" in d["tags"]
    assert "No" in d["tags"]
    spec2 = WindowSpec.from_dict(d)
    assert spec2.title == "Confirm"
    assert "Yes" in spec2.tags


def test_modal_dialog_rounded_border_default():
    spec = get_preset("modal-dialog")
    assert spec.border_style == BorderStyle.ROUNDED


def test_modal_dialog_padding():
    spec = get_preset("modal-dialog")
    assert spec.padding == 1


# ---------------------------------------------------------------------------
# Preset: log-viewer
# ---------------------------------------------------------------------------

def test_log_viewer_returns_window():
    spec = get_preset("log-viewer")
    assert isinstance(spec, WindowSpec)


def test_log_viewer_portability():
    spec = get_preset("log-viewer", title="App Logs", width=100, height=25,
                      scroll_y=10, text_overflow="truncate")
    d = spec.to_dict()
    assert d["spec_type"] == "window"
    assert d["title"] == "App Logs"
    assert d["scroll_y"] == 10
    assert d["text_overflow"] == "truncate"
    spec2 = WindowSpec.from_dict(d)
    assert spec2.text_overflow == TextOverflow.TRUNCATE
    assert spec2.scroll_y == 10


def test_log_viewer_default_truncate():
    spec = get_preset("log-viewer")
    assert spec.text_overflow == TextOverflow.TRUNCATE


# ---------------------------------------------------------------------------
# Portability: all presets must be JSON-serializable
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name", ["dashboard", "split-pane", "split-pane-v", "modal-dialog", "log-viewer"])
def test_all_presets_json_serializable(name):
    """Every preset must produce a spec that round-trips through to_dict/from_dict."""
    import json
    from termforge.core.types import RenderableSpec
    spec = get_preset(name)
    d = spec.to_dict()
    # Must be JSON-serializable (portability contract)
    json_str = json.dumps(d)
    d2 = json.loads(json_str)
    # Must deserialize back to a RenderableSpec
    spec2 = RenderableSpec.from_dict(d2)
    assert spec2 is not None

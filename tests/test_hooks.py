"""Tests for Issue #146: Component Event Hooks."""
import json
import pytest
from termforge.core.hooks import (
    HookPhase, RenderHook, invoke_hooks, apply_patches
)
from termforge.windows.types import WindowSpec, PaneSpec


def test_render_hook_to_dict():
    hook = RenderHook(phase=HookPhase.PRE_RENDER, callback_id="test_cb", priority=10)
    d = hook.to_dict()
    assert d == {
        "phase": "pre_render",
        "callback_id": "test_cb",
        "priority": 10
    }


def test_render_hook_from_dict():
    d = {
        "phase": "post_render",
        "callback_id": "another_cb",
        "priority": 5
    }
    hook = RenderHook.from_dict(d)
    assert hook.phase == HookPhase.POST_RENDER
    assert hook.callback_id == "another_cb"
    assert hook.priority == 5


def test_render_hook_json_roundtrip():
    hook = RenderHook(phase=HookPhase.ON_RESIZE, callback_id="resize_cb", priority=0)
    d = hook.to_dict()
    j = json.dumps(d)
    restored = RenderHook.from_dict(json.loads(j))
    assert restored.phase == hook.phase
    assert restored.callback_id == hook.callback_id
    assert restored.priority == hook.priority


def test_invoke_hooks_order_and_registry():
    called = []

    def cb_low(spec, ctx):
        called.append("low")
        return {"low_key": "low_val"}

    def cb_high(spec, ctx):
        called.append("high")
        return {"high_key": "high_val"}

    hooks = [
        RenderHook(phase=HookPhase.PRE_RENDER, callback_id="low_id", priority=1),
        RenderHook(phase=HookPhase.PRE_RENDER, callback_id="high_id", priority=10),
        # Different phase, should not run
        RenderHook(phase=HookPhase.POST_RENDER, callback_id="ignored_id", priority=5),
    ]

    registry = {
        "low_id": cb_low,
        "high_id": cb_high,
        "ignored_id": lambda spec, ctx: {"ignored": True}
    }

    patches = invoke_hooks(hooks, HookPhase.PRE_RENDER, registry, spec=None, context={"meta": 42})
    assert called == ["high", "low"]  # Priority high (10) runs first
    assert patches == [
        {"high_key": "high_val"},
        {"low_key": "low_val"}
    ]


def test_apply_patches():
    original = {"title": "Original", "width": 80}
    patches = [
        {"width": 100},
        {"title": "Patched"}
    ]
    res = apply_patches(original, patches)
    assert res == {"title": "Patched", "width": 100}


def test_window_spec_with_hooks_serialization():
    hook1 = RenderHook(phase=HookPhase.PRE_RENDER, callback_id="h1")
    hook2 = RenderHook(phase=HookPhase.POST_RENDER, callback_id="h2")
    spec = WindowSpec(title="HookedWindow", hooks=[hook1, hook2])

    d = spec.to_dict()
    assert "hooks" in d
    assert len(d["hooks"]) == 2

    # Roundtrip
    j = json.dumps(d)
    restored = WindowSpec.from_dict(json.loads(j))
    assert len(restored.hooks) == 2
    assert restored.hooks[0].callback_id == "h1"
    assert restored.hooks[0].phase == HookPhase.PRE_RENDER
    assert restored.hooks[1].callback_id == "h2"
    assert restored.hooks[1].phase == HookPhase.POST_RENDER


def test_pane_spec_with_hooks_serialization():
    hook = RenderHook(phase=HookPhase.ON_RESIZE, callback_id="h3")
    spec = PaneSpec(hooks=[hook])

    d = spec.to_dict()
    assert "hooks" in d
    assert len(d["hooks"]) == 1

    # Roundtrip
    j = json.dumps(d)
    restored = PaneSpec.from_dict(json.loads(j))
    assert len(restored.hooks) == 1
    assert restored.hooks[0].callback_id == "h3"
    assert restored.hooks[0].phase == HookPhase.ON_RESIZE

"""Story: core/hooks_demo — showcase Component Lifecycle Event Hooks.

Demonstrates attaching hooks to a WindowSpec, resolving callbacks from a
registry at render time, executing PRE_RENDER and POST_RENDER hooks,
and performing dynamic property updates.
"""
from __future__ import annotations
import json
from termforge.core.hooks import HookPhase, RenderHook, invoke_hooks, apply_patches
from termforge.windows.types import WindowSpec


def highlight_on_overdue(spec: WindowSpec, context: dict[str, Any]) -> dict[str, Any]:
    """PRE_RENDER hook callback: highlights the window if context value is high."""
    val = context.get("cpu_pct", 0)
    if val > 80:
        return {
            "title": f"⚠️ ALERT: CPU at {val}%!",
            "border_style": "double",
            "focused": True,
        }
    return {}


def log_render_completion(spec: WindowSpec, context: dict[str, Any]) -> dict[str, Any]:
    """POST_RENDER hook callback: logs or modifies state after rendering."""
    # We can return an updated tag to display inside/on the border
    return {
        "tags": spec.tags + ["RENDERED"]
    }


def main() -> None:
    print("=== TermForge Component Event Hooks Demo ===\n")

    # 1. Build spec with hooks
    spec = WindowSpec(
        title="Monitor Window",
        tags=["System"],
        hooks=[
            RenderHook(phase=HookPhase.PRE_RENDER, callback_id="check_cpu", priority=10),
            RenderHook(phase=HookPhase.POST_RENDER, callback_id="log_rendered", priority=1),
        ]
    )

    print("--- 1. Original Spec ---")
    print(f"  Title:        {spec.title}")
    print(f"  Border style: {spec.border_style}")
    print(f"  Focused:      {spec.focused}")
    print(f"  Tags:         {spec.tags}")
    print(f"  Hooks:        {[h.callback_id for h in spec.hooks]}")
    print()

    # 2. Set up callback registry
    registry = {
        "check_cpu": highlight_on_overdue,
        "log_rendered": log_render_completion,
    }

    # 3. Simulate Render flow under NORMAL conditions (CPU = 45%)
    print("--- 2. Render flow under normal CPU (45%) ---")
    ctx_normal = {"cpu_pct": 45}

    # Run PRE_RENDER hooks
    pre_patches = invoke_hooks(spec.hooks, HookPhase.PRE_RENDER, registry, spec, ctx_normal)
    spec_dict = apply_patches(spec.to_dict(), pre_patches)
    spec_pre = WindowSpec.from_dict(spec_dict)

    # Run POST_RENDER hooks
    post_patches = invoke_hooks(spec_pre.hooks, HookPhase.POST_RENDER, registry, spec_pre, ctx_normal)
    spec_dict = apply_patches(spec_pre.to_dict(), post_patches)
    spec_final_normal = WindowSpec.from_dict(spec_dict)

    print(f"  Final Title:        {spec_final_normal.title}")
    print(f"  Final Border style: {spec_final_normal.border_style}")
    print(f"  Final Focused:      {spec_final_normal.focused}")
    print(f"  Final Tags:         {spec_final_normal.tags}")
    print()

    # 4. Simulate Render flow under ALERT conditions (CPU = 92%)
    print("--- 3. Render flow under alert CPU (92%) ---")
    ctx_alert = {"cpu_pct": 92}

    # Run PRE_RENDER hooks
    pre_patches = invoke_hooks(spec.hooks, HookPhase.PRE_RENDER, registry, spec, ctx_alert)
    spec_dict = apply_patches(spec.to_dict(), pre_patches)
    spec_pre = WindowSpec.from_dict(spec_dict)

    # Run POST_RENDER hooks
    post_patches = invoke_hooks(spec_pre.hooks, HookPhase.POST_RENDER, registry, spec_pre, ctx_alert)
    spec_dict = apply_patches(spec_pre.to_dict(), post_patches)
    spec_final_alert = WindowSpec.from_dict(spec_dict)

    print(f"  Final Title:        {spec_final_alert.title}")
    print(f"  Final Border style: {spec_final_alert.border_style}")
    print(f"  Final Focused:      {spec_final_alert.focused}")
    print(f"  Final Tags:         {spec_final_alert.tags}")
    print()

    # 5. Verify Portability
    print("--- 4. Portability / JSON check ---")
    j = json.dumps(spec.to_dict())
    print(f"  JSON length: {len(j)} bytes")
    restored = WindowSpec.from_dict(json.loads(j))
    print(f"  Restored Hook count: {len(restored.hooks)}")
    print(f"  Restored Hook phases: {[h.phase.value for h in restored.hooks]}")
    print("  Portability: OK")


if __name__ == "__main__":
    main()

"""TermForge component event hooks module — lifecycle hooks for passive specs.

Hooks allow attaching pure-data callback references to specs that execute
during render or layout lifecycle phases. Callbacks are looked up from a
caller-provided registry.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class HookPhase(str, Enum):
    """Phases at which a Hook can execute."""
    PRE_RENDER  = "pre_render"
    POST_RENDER = "post_render"
    ON_RESIZE   = "on_resize"
    ON_FOCUS    = "on_focus"
    ON_BLUR     = "on_blur"


@dataclass
class RenderHook:
    """A pure-data description of a lifecycle event callback.

    Attributes:
        phase: The HookPhase when this hook should run.
        callback_id: A unique identifier for the callback function, resolved
            at execution time using a caller-provided registry.
        priority: Execution priority order (higher priority runs first).
    """
    phase: HookPhase
    callback_id: str
    priority: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict with keys ``phase``, ``callback_id``, ``priority``.
        """
        return {
            "phase": self.phase.value,
            "callback_id": self.callback_id,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RenderHook:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict with keys ``phase``, ``callback_id``, ``priority``.

        Returns:
            A new :class:`RenderHook` instance.
        """
        return cls(
            phase=HookPhase(d["phase"]),
            callback_id=d["callback_id"],
            priority=d.get("priority", 0),
        )


def invoke_hooks(
    hooks: list[RenderHook],
    phase: HookPhase,
    registry: dict[str, Callable[[Any, dict[str, Any]], dict[str, Any]]],
    spec: Any,
    context: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Invoke all hooks matching the specified phase.

    Looks up callables from `registry` by `callback_id`, executes them
    with `(spec, context)`, and returns a list of dictionaries representing
    property updates/patches to be applied to the spec.

    Args:
        hooks: List of RenderHook spec instances.
        phase: The current lifecycle phase to trigger.
        registry: A map from callback ID strings to callable hook implementations.
            Signature: (spec, context) -> patch_dict
        spec: The RenderableSpec instance that owns the hooks.
        context: Execution metadata dict supplied by the rendering environment.

    Returns:
        A list of dictionary patches returned by the active hooks, sorted
        by hook priority (descending).
    """
    ctx = context if context is not None else {}
    active_hooks = [h for h in hooks if h.phase == phase]
    # Sort by priority descending
    active_hooks.sort(key=lambda h: h.priority, reverse=True)

    patches: list[dict[str, Any]] = []
    for hook in active_hooks:
        callback = registry.get(hook.callback_id)
        if callback is not None:
            patch = callback(spec, ctx)
            if isinstance(patch, dict) and patch:
                patches.append(patch)

    return patches


def apply_patches(spec_dict: dict[str, Any], patches: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply a list of dictionary patches to a spec dictionary.

    Args:
        spec_dict: The original serialized spec dictionary.
        patches: A list of patch dicts to merge into the spec.

    Returns:
        A new dictionary with patches merged.
    """
    result = dict(spec_dict)
    for patch in patches:
        result.update(patch)
    return result

"""Animation tick scheduler — pure functions, immutable state, no Rich imports.

Provides a frame-based scheduler that any component can hook into for
animations (spinners, transitions, chart streaming, logo reveals).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

# Type alias for animation callbacks
FrameCallback = Callable[[int, float], bool]
"""Callable taking (frame_number, elapsed_ms) → bool (True = keep running)."""


@dataclass(frozen=True)
class AnimationSpec:
    """Specification for a registered animation."""

    fps: float
    duration_ms: float | None  # None = infinite
    callback_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "fps": self.fps,
            "duration_ms": self.duration_ms,
            "callback_id": self.callback_id,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> AnimationSpec:
        return cls(
            fps=d["fps"],
            duration_ms=d.get("duration_ms"),
            callback_id=d["callback_id"],
        )


@dataclass(frozen=True)
class SchedulerState:
    """Immutable scheduler state — never mutated, always replaced."""

    animations: dict[str, AnimationSpec] = field(default_factory=dict)
    frame_counts: dict[str, int] = field(default_factory=dict)
    start_times: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "animations": {k: v.to_dict() for k, v in self.animations.items()},
            "frame_counts": dict(self.frame_counts),
            "start_times": dict(self.start_times),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SchedulerState:
        return cls(
            animations={
                k: AnimationSpec.from_dict(v) for k, v in d.get("animations", {}).items()
            },
            frame_counts=dict(d.get("frame_counts", {})),
            start_times=dict(d.get("start_times", {})),
        )


def create_scheduler() -> SchedulerState:
    """Create a fresh, empty scheduler state."""
    return SchedulerState()


def register_animation(
    state: SchedulerState, spec: AnimationSpec
) -> SchedulerState:
    """Register an animation — returns a *new* state (immutable)."""
    new_animations = dict(state.animations)
    new_frame_counts = dict(state.frame_counts)
    new_start_times = dict(state.start_times)

    new_animations[spec.callback_id] = spec
    new_frame_counts[spec.callback_id] = 0
    # Start time is set to -1 to indicate "not started yet";
    # the first tick() call will set the real start time.
    new_start_times[spec.callback_id] = -1.0

    return SchedulerState(
        animations=new_animations,
        frame_counts=new_frame_counts,
        start_times=new_start_times,
    )


def unregister_animation(
    state: SchedulerState, callback_id: str
) -> SchedulerState:
    """Remove an animation — returns a *new* state."""
    new_animations = dict(state.animations)
    new_frame_counts = dict(state.frame_counts)
    new_start_times = dict(state.start_times)

    new_animations.pop(callback_id, None)
    new_frame_counts.pop(callback_id, None)
    new_start_times.pop(callback_id, None)

    return SchedulerState(
        animations=new_animations,
        frame_counts=new_frame_counts,
        start_times=new_start_times,
    )


def tick(
    state: SchedulerState, current_time_ms: float
) -> tuple[SchedulerState, list[str]]:
    """Advance the scheduler by one tick.

    Returns:
        (new_state, callbacks_to_fire): The updated state and a list of
        callback_ids whose frame should fire this tick.

    Algorithm:
    1. For each registered animation:
       a. If start_time == -1, initialize it to current_time_ms.
       b. Compute elapsed_ms = current_time_ms - start_time.
       c. If duration_ms is set and elapsed_ms >= duration_ms, mark complete
          and remove.
       d. Compute expected_frame = floor(elapsed_ms * fps / 1000).
       e. If expected_frame > frame_count, fire the callback and bump
          frame_count to expected_frame.
    2. Return updated state and list of fired callback_ids.
    """
    new_animations = dict(state.animations)
    new_frame_counts = dict(state.frame_counts)
    new_start_times = dict(state.start_times)
    fired: list[str] = []

    for cid, spec in state.animations.items():
        start = new_start_times.get(cid, -1.0)
        if start < 0:
            new_start_times[cid] = current_time_ms
            start = current_time_ms

        elapsed = current_time_ms - start

        # Check duration
        if spec.duration_ms is not None and elapsed >= spec.duration_ms:
            new_animations.pop(cid, None)
            new_frame_counts.pop(cid, None)
            new_start_times.pop(cid, None)
            continue

        # Compute expected frame
        if spec.fps > 0:
            expected_frame = int(elapsed * spec.fps / 1000.0)
        else:
            expected_frame = 0

        current_frame = new_frame_counts.get(cid, 0)
        if expected_frame > current_frame:
            fired.append(cid)
            new_frame_counts[cid] = expected_frame

    return (
        SchedulerState(
            animations=new_animations,
            frame_counts=new_frame_counts,
            start_times=new_start_times,
        ),
        fired,
    )


def is_animation_complete(
    state: SchedulerState, callback_id: str, current_time_ms: float
) -> bool:
    """Check whether an animation has completed (or was never registered)."""
    if callback_id not in state.animations:
        return True
    spec = state.animations[callback_id]
    if spec.duration_ms is None:
        return False
    start = state.start_times.get(callback_id, -1.0)
    if start < 0:
        return False
    return (current_time_ms - start) >= spec.duration_ms

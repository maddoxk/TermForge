"""TermForge v2.1 reactive state, live stream, and animation interpolation engine.

Provides developer-friendly state binding, live terminal streaming loops,
and value animation transitions.
"""
from __future__ import annotations

import sys
import time
from typing import Any, Callable, Generic, TypeVar
from termforge.core.types import Size, ColorDepth, RenderableSpec
from termforge.core.theme import ThemeTokens


T = TypeVar("T")


class State(Generic[T]):
    """Reactive state container for user variables.

    Attributes:
        value: Current internal data value.
    """

    def __init__(self, initial_value: T, on_change: Callable[[T], None] | None = None) -> None:
        self._value = initial_value
        self._listeners: list[Callable[[T], None]] = []
        if on_change:
            self._listeners.append(on_change)

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: T) -> None:
        if self._value != new_value:
            self._value = new_value
            for listener in self._listeners:
                listener(new_value)

    def subscribe(self, callback: Callable[[T], None]) -> None:
        """Subscribe a listener callback to value mutations."""
        if callback not in self._listeners:
            self._listeners.append(callback)


class View:
    """Reactive component view wrapper bound to user state or spec builder callbacks.

    Args:
        builder: Callable returning a RenderableSpec component.
    """

    def __init__(self, builder: Callable[[], RenderableSpec]) -> None:
        self.builder = builder

    def draw(
        self,
        width: int = 80,
        height: int = 24,
        theme: ThemeTokens | None = None,
        depth: ColorDepth | None = None,
    ) -> str:
        """Render the current state of the view into a formatted string."""
        from termforge import draw
        spec = self.builder()
        return draw(spec, width=width, height=height, theme=theme, depth=depth)


def stream(
    render_callback: Callable[[int], RenderableSpec],
    fps: float = 10.0,
    duration_sec: float | None = None,
    width: int = 80,
    height: int = 24,
    theme: ThemeTokens | None = None,
    depth: ColorDepth | None = None,
) -> None:
    """Run an automatic terminal live stream loop rendering components at a target FPS.

    Args:
        render_callback: Callable taking frame_index (int) -> RenderableSpec.
        fps: Target frames per second (default 10.0).
        duration_sec: Optional duration limit in seconds (None runs until interrupted).
        width: Terminal viewport width.
        height: Terminal viewport height.
        theme: Theme tokens.
        depth: Color depth tier.
    """
    from termforge import draw

    interval = 1.0 / max(1.0, fps)
    start_time = time.time()
    frame_idx = 0

    # Hide cursor and enable clear screen
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            frame_start = time.time()
            if duration_sec is not None and (frame_start - start_time) >= duration_sec:
                break

            spec = render_callback(frame_idx)
            content = draw(spec, width=width, height=height, theme=theme, depth=depth)

            # Move cursor home and draw frame
            sys.stdout.write("\033[H\033[J")
            sys.stdout.write(content)
            sys.stdout.write("\n")
            sys.stdout.flush()

            frame_idx += 1
            elapsed = time.time() - frame_start
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    finally:
        # Restore cursor
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()


def animate_val(
    start: float,
    end: float,
    duration: float = 1.0,
    fps: float = 10.0,
    spec_factory: Callable[[float], RenderableSpec] | None = None,
) -> list[RenderableSpec | float]:
    """Generate a sequence of interpolated values or component specs for smooth animations.

    Args:
        start: Starting numerical value.
        end: Ending numerical value.
        duration: Animation duration in seconds (default 1.0).
        fps: Target frames per second (default 10.0).
        spec_factory: Optional function mapping interpolated float value -> RenderableSpec.

    Returns:
        List of component specs or interpolated values across frame steps.
    """
    total_frames = max(1, int(duration * fps))
    results: list[RenderableSpec | float] = []

    for f in range(total_frames + 1):
        t = f / float(total_frames)
        val = start + (end - start) * t
        if spec_factory:
            results.append(spec_factory(val))
        else:
            results.append(val)

    return results

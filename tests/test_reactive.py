"""Tests for reactive State, View, stream, and animate_val features."""
import termforge as tf


def test_reactive_state_and_view():
    status = tf.State("IDLE")
    progress = tf.State(0.0)

    callbacks_fired = []
    status.subscribe(lambda v: callbacks_fired.append(f"status:{v}"))

    view = tf.View(lambda: tf.CardSpec(
        title=status.value,
        content=f"Progress: {int(progress.value * 100)}%"
    ))

    # Initial draw
    out1 = view.draw(width=40, height=5)
    assert "IDLE" in out1
    assert "Progress: 0%" in out1

    # Mutate state
    status.value = "RUNNING"
    progress.value = 0.50

    # Draw updated view
    out2 = view.draw(width=40, height=5)
    assert "RUNNING" in out2
    assert "Progress: 50%" in out2
    assert callbacks_fired == ["status:RUNNING"]


def test_animate_val_interpolation():
    frames = tf.animate_val(start=0.0, end=100.0, duration=1.0, fps=5.0)
    assert len(frames) == 6  # 0.0, 20.0, 40.0, 60.0, 80.0, 100.0
    assert frames[0] == 0.0
    assert frames[-1] == 100.0


def test_animate_val_spec_factory():
    specs = tf.animate_val(
        start=0.0,
        end=1.0,
        duration=0.5,
        fps=2.0,
        spec_factory=lambda p: tf.ProgressSpec(progress=p, width=20)
    )
    assert len(specs) == 2
    assert isinstance(specs[0], tf.ProgressSpec)
    assert specs[0].progress == 0.0
    assert specs[-1].progress == 1.0


def test_stream_execution():
    frame_count = []

    def mock_render(idx: int):
        frame_count.append(idx)
        return tf.TextSpec(content=f"Frame {idx}")

    # Run stream for 0.1 sec at 10 fps
    tf.stream(mock_render, fps=10.0, duration_sec=0.15, width=20, height=1)
    assert len(frame_count) >= 1

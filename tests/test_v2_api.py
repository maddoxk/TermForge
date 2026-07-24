"""Tests for TermForge v2.0.0 developer friendly top-level API."""
import termforge as tf


def test_top_level_exports():
    assert tf.__version__ == "2.0.0"
    assert callable(tf.render)
    assert callable(tf.draw)


def test_top_level_draw_card():
    card = tf.CardSpec(title="V2 Release", content="Welcome to TermForge v2.0.0!")
    output = tf.draw(card, width=40, height=5)
    assert "V2 Release" in output
    assert "Welcome to TermForge v2.0.0!" in output


def test_top_level_render_badge():
    badge = tf.BadgeSpec(text="OK", severity="success")
    lines = tf.render(badge, width=15, height=1)
    assert len(lines) == 1
    assert "[ OK ]" in lines[0]


def test_top_level_draw_progress():
    progress = tf.ProgressSpec(progress=0.75, width=20)
    output = tf.draw(progress, width=20, height=1)
    assert "75%" in output

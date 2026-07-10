"""TermForge text module — styled text primitives, markup, wrapping."""
from termforge.text.types import (
    TextAlign,
    TextOverflow,
    TextSpan,
    TextRun,
    TextSpec,
)
from termforge.text.markup import (
    parse_markup,
    strip_markup,
)
from termforge.text.wrap import (
    char_width,
    get_string_width,
    measure_text,
    wrap_text,
    truncate_text,
    wrap_run,
)

from termforge.text.render import (
    style_to_ansi,
    render_text,
    apply_overflow_cascade,
)

__all__ = [
    "TextAlign",
    "TextOverflow",
    "TextSpan",
    "TextRun",
    "TextSpec",
    "parse_markup",
    "strip_markup",
    "char_width",
    "get_string_width",
    "measure_text",
    "wrap_text",
    "truncate_text",
    "wrap_run",
    "style_to_ansi",
    "render_text",
    "apply_overflow_cascade",
]

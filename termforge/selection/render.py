from __future__ import annotations
from termforge.core.types import Size
from termforge.core.theme import ThemeTokens
from termforge.selection.types import SelectionListSpec
from termforge.text.types import TextAlign


def _align_text(text: str, width: int, align: TextAlign) -> str:
    """Pad text to `width` chars using the given alignment."""
    if align == TextAlign.CENTER:
        return text.center(width)
    elif align == TextAlign.RIGHT:
        return text.rjust(width)
    else:  # LEFT (default)
        return text.ljust(width)


def render_selection_list(spec: SelectionListSpec, max_size: Size, theme: ThemeTokens) -> list[str]:
    lines = []
    for i, item in enumerate(spec.items):
        is_focused = (i == spec.focused_index)
        box = "[x]" if item.selected else "[ ]"
        pointer = "> " if is_focused else "  "

        # Compute available width for the label (minus pointer + box + space)
        prefix = f"{pointer}{box} "
        avail_label_w = max(0, max_size.width - len(prefix))

        # Apply alignment to label within available space
        label = _align_text(item.label, avail_label_w, spec.item_align)

        line = f"{prefix}{label}"

        # Hard-truncate to max width
        if len(line) > max_size.width:
            line = line[:max_size.width - 1] + "…"
        lines.append(line)

        # item_spacing: blank lines between each item (but not after the last)
        if spec.item_spacing > 0 and i < len(spec.items) - 1:
            for _ in range(spec.item_spacing):
                lines.append("")

    return lines[:max_size.height]

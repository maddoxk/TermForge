#!/usr/bin/env python3
"""Story: Layout Demo — renders a simple 3-column flex layout as ASCII boxes.

Demonstrates compute_layout() by building a flex row with three columns,
then drawing them as ASCII-art rectangles in a character grid.
No Rich/Textual imports — plain print output.
"""
from __future__ import annotations

from termforge.core.types import BoxConstraints, Position, RenderableSpec, Size, Spacing
from termforge.core.layout import (
    BoxModel,
    FlexContainer,
    FlexDirection,
    LayoutNode,
    compute_layout,
)


def draw_layout(result, width: int, height: int, labels: list[str] | None = None) -> list[str]:
    """Render a LayoutResult tree into a 2D character grid."""
    grid = [[" "] * width for _ in range(height)]

    def draw_box(lr, depth: int = 0, label: str = "") -> None:
        x, y = lr.position.x, lr.position.y
        w, h = lr.size.width, lr.size.height

        if w <= 0 or h <= 0:
            return

        chars = "+-|"  # corner, horizontal, vertical
        corner = "+"
        horiz = "-"
        vert = "|"

        # Top edge
        for col in range(x, min(x + w, width)):
            if 0 <= y < height:
                grid[y][col] = horiz
        # Bottom edge
        by = y + h - 1
        for col in range(x, min(x + w, width)):
            if 0 <= by < height:
                grid[by][col] = horiz
        # Left edge
        for row in range(y, min(y + h, height)):
            if 0 <= x < width:
                grid[row][x] = vert
        # Right edge
        rx = x + w - 1
        for row in range(y, min(y + h, height)):
            if 0 <= rx < width:
                grid[row][rx] = vert
        # Corners
        for cy, cx in [(y, x), (y, x + w - 1), (y + h - 1, x), (y + h - 1, x + w - 1)]:
            if 0 <= cy < height and 0 <= cx < width:
                grid[cy][cx] = corner

        # Label inside box
        if label and h > 1 and w > 2:
            label_y = y + h // 2
            label_x = x + 1
            for i, ch in enumerate(label[: w - 2]):
                if 0 <= label_y < height and 0 <= label_x + i < width:
                    grid[label_y][label_x + i] = ch

        for i, child in enumerate(lr.children):
            child_label = ""
            if labels and depth == 0 and i < len(labels):
                child_label = labels[i]
            draw_box(child, depth + 1, child_label)

    draw_box(result, label="")
    # Draw child labels
    if labels:
        for i, child in enumerate(result.children):
            if i < len(labels):
                lbl = labels[i]
                cy = child.position.y + child.size.height // 2
                cx = child.position.x + 1
                for j, ch in enumerate(lbl[: child.size.width - 2]):
                    if 0 <= cy < height and 0 <= cx + j < width:
                        grid[cy][cx + j] = ch

    return ["".join(row) for row in grid]


def main() -> None:
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║              TermForge Layout Engine Demo                       ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    # --- Demo 1: Three-column row layout ---
    print("1. Flex Row — Three Equal Columns (flex_grow=1)")
    print("   Container: 60×10, gap=2")
    print()

    columns = [
        LayoutNode(
            spec=RenderableSpec(spec_type="box"),
            box=BoxModel(flex_grow=1.0),
        )
        for _ in range(3)
    ]
    container = LayoutNode(
        spec=RenderableSpec(spec_type="container"),
        box=BoxModel(width=60, height=10),
        flex=FlexContainer(direction=FlexDirection.ROW, gap=2),
        children=columns,
    )
    constraints = BoxConstraints(min_width=0, max_width=60, min_height=0, max_height=10)
    result = compute_layout(container, constraints)

    lines = draw_layout(result, 60, 10, labels=["Col-1", "Col-2", "Col-3"])
    for line in lines:
        print(f"   {line}")
    print()

    # --- Demo 2: Column layout ---
    print("2. Flex Column — Two Stacked Rows (flex_grow=1)")
    print("   Container: 40×12, gap=1")
    print()

    rows = [
        LayoutNode(
            spec=RenderableSpec(spec_type="box"),
            box=BoxModel(flex_grow=1.0),
        )
        for _ in range(2)
    ]
    container2 = LayoutNode(
        spec=RenderableSpec(spec_type="container"),
        box=BoxModel(width=40, height=12),
        flex=FlexContainer(direction=FlexDirection.COLUMN, gap=1),
        children=rows,
    )
    constraints2 = BoxConstraints(min_width=0, max_width=40, min_height=0, max_height=12)
    result2 = compute_layout(container2, constraints2)

    lines2 = draw_layout(result2, 40, 12, labels=["Row-1", "Row-2"])
    for line in lines2:
        print(f"   {line}")
    print()

    # --- Demo 3: Fixed-width sidebar + flexible main ---
    print("3. Sidebar Layout — Fixed 15-wide sidebar + flexible main")
    print("   Container: 60×8, gap=1")
    print()

    sidebar = LayoutNode(
        spec=RenderableSpec(spec_type="box"),
        box=BoxModel(width=15, height=8),
    )
    main_content = LayoutNode(
        spec=RenderableSpec(spec_type="box"),
        box=BoxModel(flex_grow=1.0),
    )
    container3 = LayoutNode(
        spec=RenderableSpec(spec_type="container"),
        box=BoxModel(width=60, height=8),
        flex=FlexContainer(direction=FlexDirection.ROW, gap=1),
        children=[sidebar, main_content],
    )
    constraints3 = BoxConstraints(min_width=0, max_width=60, min_height=0, max_height=8)
    result3 = compute_layout(container3, constraints3)

    lines3 = draw_layout(result3, 60, 8, labels=["Sidebar", "Main Content"])
    for line in lines3:
        print(f"   {line}")
    print()

    # Summary
    print("Layout positions computed by compute_layout():")
    for i, child in enumerate(result.children):
        print(
            f"  Child {i}: pos=({child.position.x},{child.position.y}) "
            f"size={child.size.width}×{child.size.height}"
        )
    print()


if __name__ == "__main__":
    main()

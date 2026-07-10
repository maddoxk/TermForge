"""Box-model layout engine — pure functions, no Rich imports.

Implements a simplified flex-like layout with margin, padding, flex_grow,
flex_shrink, gap, and wrapping.
"""
from __future__ import annotations
import logging
import os

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from termforge.core.types import (
    BoxConstraints,
    LayoutResult,
    Position,
    RenderableSpec,
    Size,
    Spacing,
)


class FlexDirection(Enum):
    """Main axis direction for flex layout."""

    ROW = "row"
    COLUMN = "column"


@dataclass
class BoxModel:
    """Box-model properties for a layout node."""

    margin: Spacing = field(default_factory=Spacing)
    padding: Spacing = field(default_factory=Spacing)
    width: int | None = None
    height: int | None = None
    flex_grow: float = 0.0
    flex_shrink: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "margin": self.margin.to_dict(),
            "padding": self.padding.to_dict(),
            "flex_grow": self.flex_grow,
            "flex_shrink": self.flex_shrink,
        }
        if self.width is not None:
            d["width"] = self.width
        if self.height is not None:
            d["height"] = self.height
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BoxModel:
        return cls(
            margin=Spacing.from_dict(d.get("margin", {})),
            padding=Spacing.from_dict(d.get("padding", {})),
            width=d.get("width"),
            height=d.get("height"),
            flex_grow=d.get("flex_grow", 0.0),
            flex_shrink=d.get("flex_shrink", 1.0),
        )


@dataclass
class FlexContainer:
    """Flex container properties attached to a LayoutNode."""

    direction: FlexDirection = FlexDirection.ROW
    gap: int = 0
    wrap: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "direction": self.direction.value,
            "gap": self.gap,
            "wrap": self.wrap,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> FlexContainer:
        return cls(
            direction=FlexDirection(d.get("direction", "row")),
            gap=d.get("gap", 0),
            wrap=d.get("wrap", False),
        )


@dataclass
class LayoutNode:
    """A node in the layout tree."""

    spec: RenderableSpec
    box: BoxModel = field(default_factory=BoxModel)
    flex: FlexContainer | None = None
    children: list[LayoutNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "spec": self.spec.to_dict(),
            "box": self.box.to_dict(),
            "children": [c.to_dict() for c in self.children],
        }
        if self.flex is not None:
            d["flex"] = self.flex.to_dict()
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> LayoutNode:
        return cls(
            spec=RenderableSpec.from_dict(d["spec"]),
            box=BoxModel.from_dict(d.get("box", {})),
            flex=FlexContainer.from_dict(d["flex"]) if "flex" in d else None,
            children=[LayoutNode.from_dict(c) for c in d.get("children", [])],
        )


def _clamp(value: int, lo: int, hi: int) -> int:
    """Clamp value to [lo, hi]."""
    return max(lo, min(hi, value))


def _get_logger() -> logging.Logger:
    logger = logging.getLogger("termforge.core.layout")
    if not logger.handlers:
        log_file = os.environ.get("TERMFORGE_LOG_FILE", "termforge.log")
        log_level_str = os.environ.get("TERMFORGE_LOG_LEVEL", "WARNING").upper()
        log_level = getattr(logging, log_level_str, logging.WARNING)
        
        logger.setLevel(log_level)
        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def compute_layout(node: LayoutNode, constraints: BoxConstraints) -> LayoutResult:
    """Compute absolute positions and sizes for a layout tree.

    Algorithm:
    1. For leaf nodes (no children): use explicit width/height from BoxModel,
       or fall back to minimum constraint, clamped to constraints, plus padding.
    2. For flex containers: distribute available space along the main axis
       proportionally to flex_grow. Handle gap between children.
    3. Apply margin by offsetting positions.
    4. Returns a tree of LayoutResult with absolute positions.
    """
    return _compute(node, constraints, Position(x=0, y=0))


def _compute(
    node: LayoutNode, constraints: BoxConstraints, offset: Position
) -> LayoutResult:
    margin = node.box.margin
    padding = node.box.padding

    # Effective origin after margin
    inner_x = offset.x + margin.left
    inner_y = offset.y + margin.top

    # Available space inside margin
    avail_w = constraints.max_width - margin.horizontal
    avail_h = constraints.max_height - margin.vertical

    if avail_w < 0:
        avail_w = 0
    if avail_h < 0:
        avail_h = 0

    # Determine own size
    if node.box.width is not None:
        own_w = _clamp(node.box.width, constraints.min_width, avail_w) if avail_w > 0 else node.box.width
    else:
        own_w = avail_w

    if node.box.height is not None:
        own_h = _clamp(node.box.height, constraints.min_height, avail_h) if avail_h > 0 else node.box.height
    else:
        own_h = avail_h

    if own_w <= 0 or own_h <= 0:
        logger = _get_logger()
        logger.warning(f"Component '{node.spec.spec_type}' collapsed to size {own_w}x{own_h}!")

    # Leaf node
    if not node.children or node.flex is None:
        w = _clamp(own_w, constraints.min_width, constraints.max_width)
        h = _clamp(own_h, constraints.min_height, constraints.max_height)
        if w <= 0 or h <= 0:
            logger = _get_logger()
            logger.warning(f"Component '{node.spec.spec_type}' collapsed to size {w}x{h}!")
        return LayoutResult(
            position=Position(x=inner_x, y=inner_y),
            size=Size(width=w, height=h),
        )

    # Flex container
    flex = node.flex
    is_row = flex.direction == FlexDirection.ROW
    gap = flex.gap

    # Content area inside padding
    content_w = own_w - padding.horizontal
    content_h = own_h - padding.vertical
    if content_w < 0:
        content_w = 0
    if content_h < 0:
        content_h = 0

    n = len(node.children)
    total_gap = gap * (n - 1) if n > 1 else 0

    if is_row:
        main_available = content_w - total_gap
    else:
        main_available = content_h - total_gap

    if main_available < 0:
        main_available = 0

    # First pass: measure each child's base size and collect flex_grow
    child_base_sizes: list[int] = []
    total_flex_grow = 0.0

    for child in node.children:
        cm = child.box.margin
        if is_row:
            if child.box.width is not None:
                base = child.box.width + cm.horizontal
            else:
                base = 0
        else:
            if child.box.height is not None:
                base = child.box.height + cm.vertical
            else:
                base = 0
        child_base_sizes.append(base)
        total_flex_grow += child.box.flex_grow

    used = sum(child_base_sizes)
    remaining = main_available - used
    if remaining < 0:
        remaining = 0

    # Second pass: distribute remaining space and compute child layouts
    total_extra_distributed = sum(
        int(remaining * (child.box.flex_grow / total_flex_grow))
        for child in node.children
        if total_flex_grow > 0 and child.box.flex_grow > 0
    )
    if total_flex_grow > 0 and total_extra_distributed != remaining:
        logger = _get_logger()
        logger.warning(
            f"Layout rounding error: distributed {total_extra_distributed} cells of remaining {remaining} cells "
            f"for container '{node.spec.spec_type}'."
        )

    child_results: list[LayoutResult] = []
    cursor_x = inner_x + padding.left
    cursor_y = inner_y + padding.top

    for i, child in enumerate(node.children):
        # Determine main-axis size for this child
        extra = 0
        if total_flex_grow > 0 and child.box.flex_grow > 0:
            extra = int(remaining * (child.box.flex_grow / total_flex_grow))

        if is_row:
            child_max_w = child_base_sizes[i] + extra
            if child_max_w <= 0 and child.box.width is None:
                child_max_w = int(remaining / n) if total_flex_grow == 0 else extra
            child_constraints = BoxConstraints(
                min_width=0,
                max_width=max(child_max_w, 0),
                min_height=0,
                max_height=content_h,
            )
            child_result = _compute(child, child_constraints, Position(x=cursor_x, y=cursor_y))
            cursor_x += child_result.size.width + child.box.margin.horizontal + gap
        else:
            child_max_h = child_base_sizes[i] + extra
            if child_max_h <= 0 and child.box.height is None:
                child_max_h = int(remaining / n) if total_flex_grow == 0 else extra
            child_constraints = BoxConstraints(
                min_width=0,
                max_width=content_w,
                min_height=0,
                max_height=max(child_max_h, 0),
            )
            child_result = _compute(child, child_constraints, Position(x=cursor_x, y=cursor_y))
            cursor_y += child_result.size.height + child.box.margin.vertical + gap

        child_results.append(child_result)

    return LayoutResult(
        position=Position(x=inner_x, y=inner_y),
        size=Size(width=own_w, height=own_h),
        children=child_results,
    )

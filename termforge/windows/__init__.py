"""TermForge windows module — composable containers, scroll, focus, z-order."""
from termforge.windows.types import WindowSpec, PaneSpec, ModalSpec
from termforge.windows.compositor import compose_panes, apply_scroll, z_sort, render_window

__all__ = [
    "WindowSpec",
    "PaneSpec",
    "ModalSpec",
    "compose_panes",
    "apply_scroll",
    "z_sort",
    "render_window",
]

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec
from termforge.core import FlexDirection
from termforge.borders.types import BorderStyle
from termforge.text.types import TextOverflow, TextAlign
from termforge.core.hooks import RenderHook

@dataclass
class WindowSpec(RenderableSpec):
    title: str = "Window"
    border_style: BorderStyle = BorderStyle.SINGLE
    width: int | None = None
    height: int | None = None
    scroll_y: int = 0
    focused: bool = False
    z_index: int = 0
    content: RenderableSpec | None = None
    shadow: bool = False
    tags: list[str] = field(default_factory=list)
    padding: int = 0
    margin: int = 0
    text_overflow: TextOverflow | None = None  # if set, cascades to child TextSpec.overflow
    title_align: TextAlign = TextAlign.CENTER   # alignment of title in the top border
    title_pad: int = 1                          # spaces to pad on each side of the title text
    show_scrollbar: bool = False
    scrollbar_style: str | None = None
    hooks: list[RenderHook] = field(default_factory=list)
    spec_type: str = "window"


    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "title": self.title,
            "border_style": self.border_style.value,
            "width": self.width,
            "height": self.height,
            "scroll_y": self.scroll_y,
            "focused": self.focused,
            "z_index": self.z_index,
            "content": self.content.to_dict() if self.content else None,
            "shadow": self.shadow,
            "tags": self.tags,
            "padding": self.padding,
            "margin": self.margin,
            "text_overflow": self.text_overflow.value if self.text_overflow else None,
            "title_align": self.title_align.value,
            "title_pad": self.title_pad,
            "show_scrollbar": self.show_scrollbar,
            "scrollbar_style": self.scrollbar_style,
            "hooks": [h.to_dict() for h in self.hooks],
        }


    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> WindowSpec:
        content_dict = d.get("content")
        content = RenderableSpec.from_dict(content_dict) if content_dict else None
        overflow_val = d.get("text_overflow")
        return cls(
            title=d.get("title", "Window"),
            border_style=BorderStyle(d.get("border_style", "single")),
            width=d.get("width"),
            height=d.get("height"),
            scroll_y=d.get("scroll_y", 0),
            focused=d.get("focused", False),
            z_index=d.get("z_index", 0),
            content=content,
            shadow=d.get("shadow", False),
            tags=d.get("tags", []),
            padding=d.get("padding", 0),
            margin=d.get("margin", 0),
            text_overflow=TextOverflow(overflow_val) if overflow_val else None,
            title_align=TextAlign(d.get("title_align", "center")),
            title_pad=d.get("title_pad", 1),
            show_scrollbar=d.get("show_scrollbar", False),
            scrollbar_style=d.get("scrollbar_style"),
            hooks=[RenderHook.from_dict(h) for h in d.get("hooks", [])],
        )


@dataclass
class PaneSpec(RenderableSpec):
    direction: FlexDirection = FlexDirection.ROW
    children: list[RenderableSpec] = field(default_factory=list)
    ratios: list[float] | None = None
    gap: int = 0
    text_overflow: TextOverflow | None = None  # if set, cascades to child TextSpec.overflow
    hooks: list[RenderHook] = field(default_factory=list)
    spec_type: str = "pane"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "direction": self.direction.value,
            "children": [c.to_dict() for c in self.children],
            "ratios": self.ratios,
            "gap": self.gap,
            "text_overflow": self.text_overflow.value if self.text_overflow else None,
            "hooks": [h.to_dict() for h in self.hooks],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> PaneSpec:
        overflow_val = d.get("text_overflow")
        return cls(
            direction=FlexDirection(d.get("direction", "row")),
            children=[RenderableSpec.from_dict(c) for c in d.get("children", [])],
            ratios=d.get("ratios"),
            gap=d.get("gap", 0),
            text_overflow=TextOverflow(overflow_val) if overflow_val else None,
            hooks=[RenderHook.from_dict(h) for h in d.get("hooks", [])],
        )

@dataclass
class ModalSpec(RenderableSpec):
    content: RenderableSpec | None = None
    backdrop: bool = True
    width: int = 40
    height: int = 10
    spec_type: str = "modal"

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_type": self.spec_type,
            "content": self.content.to_dict() if self.content else None,
            "backdrop": self.backdrop,
            "width": self.width,
            "height": self.height
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ModalSpec:
        content_dict = d.get("content")
        content = RenderableSpec.from_dict(content_dict) if content_dict else None
        return cls(
            content=content,
            backdrop=d.get("backdrop", True),
            width=d.get("width", 40),
            height=d.get("height", 10)
        )

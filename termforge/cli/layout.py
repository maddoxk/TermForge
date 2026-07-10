from __future__ import annotations
import sys
import os
from typing import Any
from termforge.core.types import RenderableSpec, Size, Position, BoxConstraints, Spacing, LayoutResult, ColorDepth
from termforge.core.layout import LayoutNode, BoxModel, FlexContainer, FlexDirection, compute_layout
from termforge.core.theme import ThemeTokens

def spec_to_layout_node(spec: RenderableSpec) -> LayoutNode:
    width = getattr(spec, "width", None)
    height = getattr(spec, "height", None)
    
    padding_top = 0
    padding_bottom = 0
    padding_left = 0
    padding_right = 0
    
    if spec.spec_type in ("window", "border", "modal"):
        padding_top = 1
        padding_bottom = 1
        padding_left = 1
        padding_right = 1
        
    box = BoxModel(
        width=width,
        height=height,
        padding=Spacing(top=padding_top, bottom=padding_bottom, left=padding_left, right=padding_right)
    )
    
    flex = None
    children = []
    if spec.spec_type == "pane":
        direction = FlexDirection.ROW if getattr(spec, "direction", "row") == "row" else FlexDirection.COLUMN
        flex = FlexContainer(
            direction=direction,
            gap=getattr(spec, "gap", 0)
        )
        ratios = getattr(spec, "ratios", None) or [1.0] * len(getattr(spec, "children", []))
        for i, child_spec in enumerate(getattr(spec, "children", [])):
            child_node = spec_to_layout_node(child_spec)
            child_node.box.flex_grow = ratios[i] if i < len(ratios) else 1.0
            children.append(child_node)
    elif spec.spec_type in ("window", "border", "modal"):
        flex = FlexContainer(
            direction=FlexDirection.COLUMN,
            gap=0
        )
        content_spec = getattr(spec, "content", None)
        if content_spec:
            child_node = spec_to_layout_node(content_spec)
            child_node.box.flex_grow = 1.0
            children.append(child_node)
            
    return LayoutNode(
        spec=spec,
        box=box,
        flex=flex,
        children=children
    )

def draw_layout_result(
    result: LayoutResult,
    spec: RenderableSpec,
    grid: list[list[str]],
    theme: ThemeTokens | None = None,
    depth: ColorDepth | None = None
) -> None:
    x = result.position.x
    y = result.position.y
    w = result.size.width
    h = result.size.height
    
    start_ansi, end_ansi = "", ""
    if depth is not None and theme is not None:
        from termforge.core.types import StyleSpec, ColorValue
        from termforge.text.render import style_to_ansi
        color_name = "colors.border" if spec.spec_type == "window" else "colors.primary"
        style = StyleSpec(fg=ColorValue(0, 0, 0, name=color_name))
        start_ansi, end_ansi = style_to_ansi(style, theme, depth)
    
    def set_cell(cy: int, cx: int, char: str) -> None:
        if 0 <= cy < len(grid) and 0 <= cx < len(grid[0]):
            if start_ansi or end_ansi:
                grid[cy][cx] = f"{start_ansi}{char}{end_ansi}"
            else:
                grid[cy][cx] = char

    for i in range(x, x + w):
        set_cell(y, i, "-")
        set_cell(y + h - 1, i, "-")
                
    for j in range(y, y + h):
        set_cell(j, x, "|")
        set_cell(j, x + w - 1, "|")
                
    set_cell(y, x, "+")
    set_cell(y, x + w - 1, "+")
    set_cell(y + h - 1, x, "+")
    set_cell(y + h - 1, x + w - 1, "+")
        
    label = f"{spec.spec_type} ({w}x{h})"
    label_x = x + 2
    label_y = y + 1
    if label_y < y + h - 1 and 0 <= label_y < len(grid):
        for idx, char in enumerate(label):
            target_x = label_x + idx
            if target_x < x + w - 1 and target_x < len(grid[0]):
                set_cell(label_y, target_x, char)
                
    if hasattr(spec, "content") and spec.content is not None and result.children:
        draw_layout_result(result.children[0], spec.content, grid, theme, depth)
    elif hasattr(spec, "children") and spec.children and result.children:
        for idx, child_spec in enumerate(spec.children):
            if idx < len(result.children):
                draw_layout_result(result.children[idx], child_spec, grid, theme, depth)

def validate_layout(result: LayoutResult, spec: RenderableSpec, errors: list[str]) -> None:
    w = result.size.width
    h = result.size.height
    if w <= 0 or h <= 0:
        errors.append(f"Constraint Error: Component '{spec.spec_type}' collapsed to size {w}x{h}!")
        
    if hasattr(spec, "content") and spec.content is not None and result.children:
        validate_layout(result.children[0], spec.content, errors)
    elif hasattr(spec, "children") and spec.children and result.children:
        for idx, child_spec in enumerate(spec.children):
            if idx < len(result.children):
                validate_layout(result.children[idx], child_spec, errors)

def render_once(path: str, strict: bool, color_depth: str | None = None) -> bool:
    from termforge.config.loader import load_config_yaml, load_config_json, load_config_toml, config_to_specs
    from termforge.core.types import ColorDepth, ColorValue
    
    target_depth = None
    if color_depth is not None:
        depth_map = {
            "truecolor": ColorDepth.TRUECOLOR,
            "color_256": ColorDepth.COLOR_256,
            "color_16": ColorDepth.COLOR_16,
            "monochrome": ColorDepth.MONOCHROME
        }
        target_depth = depth_map.get(color_depth, ColorDepth.TRUECOLOR)
    
    ext = os.path.splitext(path)[1].lower()
    if ext in (".yaml", ".yml"):
        config = load_config_yaml(path)
    elif ext == ".json":
        config = load_config_json(path)
    elif ext == ".toml":
        config = load_config_toml(path)
    else:
        print(f"Error: Unsupported file format {ext}")
        return False
        
    specs = config_to_specs(config)
    if not specs:
        print("No components found in layout config.")
        return True
        
    theme_name = config.theme or "nord"
    from termforge.theme.builtin import BUILTIN_THEMES
    theme_pack = BUILTIN_THEMES.get(theme_name)
    theme_tokens = theme_pack.tokens if theme_pack else None
    
    color_warnings: list[str] = []
    
    for root_spec in specs:
        node = spec_to_layout_node(root_spec)
        
        max_w = getattr(root_spec, "width", 80) or 80
        max_h = getattr(root_spec, "height", 24) or 24
        constraints = BoxConstraints(min_width=0, max_width=max_w, min_height=0, max_height=max_h)
        
        result = compute_layout(node, constraints)
        
        errors: list[str] = []
        validate_layout(result, root_spec, errors)
        
        if theme_tokens and target_depth is not None:
            def check_node_colors(s: RenderableSpec) -> None:
                for prop_name in ("text_color", "border_color"):
                    val = getattr(s, prop_name, None)
                    if val:
                        from termforge.core.color import resolve_color
                        from termforge.theme.contrast import resolve_token
                        try:
                            token_path = f"colors.{val}" if not val.startswith("colors.") else val
                            color_val = resolve_token(theme_tokens, token_path)
                            if isinstance(color_val, ColorValue):
                                rgb = resolve_color(color_val, target_depth)
                                if rgb is None:
                                    color_warnings.append(f"Color Warning: Token '{val}' resolves to empty/null at depth {target_depth.name}")
                        except KeyError:
                            pass
                if hasattr(s, "content") and s.content is not None:
                    check_node_colors(s.content)
                if hasattr(s, "children") and s.children:
                    for child in s.children:
                        check_node_colors(child)
            check_node_colors(root_spec)
            
        grid = [[" " for _ in range(max_w)] for _ in range(max_h)]
        draw_layout_result(result, root_spec, grid, theme_tokens, target_depth)
        
        print(f"\n--- Visualizing Layout for {root_spec.spec_type.upper()} ({max_w}x{max_h}) ---")
        for row in grid:
            print("".join(row))
            
        if errors:
            print("\n⚠️  Layout Validation Warnings:")
            for err in errors:
                print(f"  - {err}")
            if strict:
                sys.exit(1)
                
    if color_warnings:
        print("\n⚠️  Color Depth Simulation Warnings:")
        for warn in color_warnings:
            print(f"  - {warn}")
            
    return True

def main() -> None:
    import argparse
    import time
    
    parser = argparse.ArgumentParser(description="TermForge Layout Visualizer & Validator")
    parser.add_argument("path", help="Path to layout config file (yaml/json/toml)")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if layout validation fails")
    parser.add_argument("--watch", "--hot-reload", action="store_true", help="Watch file for modifications and reload layout preview")
    parser.add_argument("--color-depth", choices=["truecolor", "color_256", "color_16", "monochrome"], default=None, help="Color depth tier to simulate (default: None)")
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: File {args.path} does not exist.")
        sys.exit(1)
        
    if not args.watch:
        render_once(args.path, args.strict, args.color_depth)
        return
        
    print(f"Watching {args.path} for changes... Press Ctrl+C to stop.")
    last_mtime = 0.0
    
    try:
        while True:
            try:
                mtime = os.path.getmtime(args.path)
            except OSError:
                time.sleep(0.2)
                continue
                
            if mtime != last_mtime:
                last_mtime = mtime
                sys.stdout.write("\033[H\033[2J")
                sys.stdout.flush()
                print(f"Reloading layout preview for {args.path}...")
                try:
                    render_once(args.path, strict=False, color_depth=args.color_depth)
                except Exception as e:
                    print(f"\n❌ Syntax/parsing error in configuration: {e}")
                    
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nStopping watcher.")
        sys.exit(0)

if __name__ == "__main__":
    main()

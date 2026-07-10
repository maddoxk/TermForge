from __future__ import annotations
import sys
import os
import yaml  # type: ignore
import json
from termforge.config.loader import load_config_yaml, load_config_json, load_config_toml, config_to_specs
from termforge.cli.layout import spec_to_layout_node
from termforge.core.types import BoxConstraints, LayoutResult
from termforge.core.layout import LayoutNode, compute_layout

try:
    import tomllib  # type: ignore
except ImportError:
    tomllib = None

def print_tree(node: LayoutNode, result: LayoutResult, prefix: str = "", is_last: bool = True) -> None:
    marker = "└─ " if is_last else "├─ "
    spec_type = node.spec.spec_type
    pos = f"pos=({result.position.x},{result.position.y})"
    size = f"size={result.size.width}x{result.size.height}"
    
    sys.stdout.write(f"{prefix}{marker}{spec_type.capitalize()} ({spec_type}) [{pos} {size}]\n")
    
    child_prefix = prefix + ("   " if is_last else "│  ")
    n = len(node.children)
    for i, child in enumerate(node.children):
        if i < len(result.children):
            print_tree(child, result.children[i], prefix=child_prefix, is_last=(i == n - 1))

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="TermForge CLI Layout Hierarchy Inspector")
    parser.add_argument("path", help="Path to layout config file (yaml/json/toml)")
    parser.add_argument("--width", type=int, default=80, help="Simulated terminal width columns (default: 80)")
    parser.add_argument("--height", type=int, default=24, help="Simulated terminal height rows (default: 24)")
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: File {args.path} does not exist.")
        sys.exit(1)
        
    ext = os.path.splitext(args.path)[1].lower()
    try:
        if ext in (".yaml", ".yml"):
            config = load_config_yaml(args.path)
        elif ext == ".json":
            config = load_config_json(args.path)
        elif ext == ".toml":
            config = load_config_toml(args.path)
        else:
            print(f"Error: Unsupported file format {ext}")
            sys.exit(1)
    except Exception as e:
        print(f"Error parsing layout config: {e}")
        sys.exit(1)
        
    specs = config_to_specs(config)
    constraints = BoxConstraints(
        min_width=0,
        max_width=args.width,
        min_height=0,
        max_height=args.height
    )
    
    print(f"Layout Hierarchy Inspection for {args.path} ({args.width}x{args.height}):")
    for i, spec in enumerate(specs):
        layout_node = spec_to_layout_node(spec)
        layout_result = compute_layout(layout_node, constraints)
        print_tree(layout_node, layout_result, prefix="", is_last=(i == len(specs) - 1))
        
    sys.exit(0)

if __name__ == "__main__":
    main()

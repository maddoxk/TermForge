from __future__ import annotations
import sys
import os
from termforge.config.loader import load_config_yaml, load_config_json, load_config_toml, config_to_specs
from termforge.cli.layout import spec_to_layout_node, validate_layout
from termforge.core.types import BoxConstraints
from termforge.core.layout import compute_layout

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="TermForge Layout Responsive Breakpoint Simulator")
    parser.add_argument("path", help="Path to layout config file (yaml/json/toml)")
    parser.add_argument("--min-width", type=int, default=40, help="Minimum width to simulate (default: 40)")
    parser.add_argument("--max-width", type=int, default=120, help="Maximum width to simulate (default: 120)")
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
            print(f"Error: Unsupported format {ext}")
            sys.exit(1)
            
        specs = config_to_specs(config)
        if not specs:
            print("No components found in layout config.")
            sys.exit(0)
            
        print(f"Simulating Responsive Widths from {args.min_width} to {args.max_width} columns...")
        print("-" * 65)
        
        breakpoints = []
        
        for w in range(args.min_width, args.max_width + 1):
            for root_spec in specs:
                node = spec_to_layout_node(root_spec)
                max_h = getattr(root_spec, "height", 24) or 24
                constraints = BoxConstraints(min_width=0, max_width=w, min_height=0, max_height=max_h)
                result = compute_layout(node, constraints)
                
                errors: list[str] = []
                validate_layout(result, root_spec, errors)
                if errors:
                    breakpoints.append((w, errors))
                    break
                    
        if breakpoints:
            print("⚠️  Responsive Layout Breakpoints Detected:")
            for w, errs in breakpoints:
                print(f"  - Width {w:3}: {errs[0]}")
            sys.exit(0)
        else:
            print("✅ Layout is fully responsive across the simulated range! No collapses detected.")
            sys.exit(0)
            
    except Exception as e:
        print(f"Error simulating responsive layout: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

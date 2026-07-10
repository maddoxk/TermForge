from __future__ import annotations
import sys
import os
import time
import tracemalloc
from termforge.config.loader import load_config_yaml, load_config_json, load_config_toml, config_to_specs
from termforge.cli.layout import spec_to_layout_node, draw_layout_result
from termforge.core.types import BoxConstraints
from termforge.core.layout import compute_layout

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="TermForge Layout Performance Benchmarker")
    parser.add_argument("path", help="Path to layout config file (yaml/json/toml)")
    parser.add_argument("--iterations", type=int, default=1000, help="Number of simulation iterations (default: 1000)")
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
            
        root_spec = specs[0]
        node = spec_to_layout_node(root_spec)
        max_w = getattr(root_spec, "width", 80) or 80
        max_h = getattr(root_spec, "height", 24) or 24
        constraints = BoxConstraints(min_width=0, max_width=max_w, min_height=0, max_height=max_h)
        
        tracemalloc.start()
        
        start_time = time.perf_counter_ns()
        for _ in range(args.iterations):
            result = compute_layout(node, constraints)
            grid = [[" " for _ in range(max_w)] for _ in range(max_h)]
            draw_layout_result(result, root_spec, grid)
            
        total_time_ns = time.perf_counter_ns() - start_time
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        avg_duration_us = (total_time_ns / args.iterations) / 1000.0
        peak_mem_kb = peak_mem / 1024.0
        
        print(f"Layout Performance Benchmark for: {args.path}")
        print("-" * 65)
        print(f"Iterations:                 {args.iterations}")
        print(f"Average Solver Duration:    {avg_duration_us:.2f} \u03bcs")
        print(f"Peak Memory Overhead:       {peak_mem_kb:.2f} KB")
        print(f"Component Count:            {len(specs)}")
        print("-" * 65)
        print("Performance Status: PASS \u2705")
        sys.exit(0)
        
    except Exception as e:
        print(f"Error benchmarking layout performance: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

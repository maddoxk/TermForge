from __future__ import annotations
import sys
import os
import yaml  # type: ignore
import json
from termforge.config.validator import validate_config, LineNumberLoader

try:
    import tomllib  # type: ignore
except ImportError:
    tomllib = None

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="TermForge Declarative Configuration Validator (Linter)")
    parser.add_argument("path", help="Path to layout or theme config file (yaml/json/toml)")
    parser.add_argument("--check-cyclic", action="store_true", help="Audit the configuration for circular component references")
    parser.add_argument("--check-bounds", action="store_true", help="Audit the configuration for layout size/boundary overflows")
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: File {args.path} does not exist.")
        sys.exit(1)
        
    ext = os.path.splitext(args.path)[1].lower()
    try:
        if ext in (".yaml", ".yml"):
            with open(args.path, "r", encoding="utf-8") as f:
                data = yaml.load(f, Loader=LineNumberLoader)
        elif ext == ".json":
            with open(args.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif ext == ".toml":
            with open(args.path, "rb") as f:
                if tomllib:
                    data = tomllib.load(f)
                else:
                    raise ImportError("TOML support requires Python 3.11+ (tomllib)")
        else:
            print(f"Error: Unsupported file format {ext}")
            sys.exit(1)
    except Exception as e:
        print(f"Error parsing configuration file: {e}")
        sys.exit(1)
        
    errors = validate_config(data, check_cyclic=args.check_cyclic, check_bounds=args.check_bounds)
    fatal_errors = [e for e in errors if "Error:" in e]
    warnings = [e for e in errors if "Warning:" in e]
    
    if errors:
        if fatal_errors:
            print(f"❌ Configuration validation failed for {args.path}:")
            for err in errors:
                print(f"  {err}")
            sys.exit(1)
        else:
            print(f"⚠️  Configuration {args.path} validated with warnings:")
            for err in warnings:
                print(f"  {err}")
            sys.exit(0)
    else:
        print(f"✅ Configuration {args.path} validated successfully (0 errors, 0 warnings).")
        sys.exit(0)

if __name__ == "__main__":
    main()

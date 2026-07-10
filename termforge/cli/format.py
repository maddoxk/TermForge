from __future__ import annotations
import sys
import os
from termforge.config.formatter import format_config_file

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="TermForge Layout Configuration Formatter")
    parser.add_argument("path", help="Path to layout config file (yaml/json/toml)")
    parser.add_argument("--write", "-w", action="store_true", help="Write formatted output back to the file.")
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: File {args.path} does not exist.")
        sys.exit(1)
        
    try:
        formatted = format_config_file(args.path, write=args.write)
        if args.write:
            print(f"✅ Successfully formatted and updated {args.path}")
        else:
            sys.stdout.write(formatted)
    except Exception as e:
        print(f"Error formatting layout config: {e}")
        sys.exit(1)
        
    sys.exit(0)

if __name__ == "__main__":
    main()

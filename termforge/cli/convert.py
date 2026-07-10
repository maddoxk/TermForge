from __future__ import annotations
import sys
import os
from termforge.config.converter import convert_config_file

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="TermForge Layout Configuration Format Translator")
    parser.add_argument("input_path", help="Path to input layout config file (yaml/json/toml)")
    parser.add_argument("output_path", help="Path to output layout config file (yaml/json/toml)")
    args = parser.parse_args()
    
    if not os.path.exists(args.input_path):
        print(f"Error: Input file {args.input_path} does not exist.")
        sys.exit(1)
        
    try:
        convert_config_file(args.input_path, args.output_path)
        print(f"✅ Successfully converted {args.input_path} to {args.output_path}")
    except Exception as e:
        print(f"Error translating config format: {e}")
        sys.exit(1)
        
    sys.exit(0)

if __name__ == "__main__":
    main()

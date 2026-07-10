from __future__ import annotations
import sys
import os
import json
from termforge.config.schema import generate_json_schema

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="TermForge JSON Schema Exporter")
    parser.add_argument("--output", "-o", help="Optional path to output file. Prints to stdout if not specified.")
    args = parser.parse_args()
    
    schema = generate_json_schema()
    payload = json.dumps(schema, indent=2)
    
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(payload)
            print(f"✅ Successfully wrote JSON Schema to {args.output}")
        except Exception as e:
            print(f"Error writing schema to file: {e}")
            sys.exit(1)
    else:
        sys.stdout.write(payload + "\n")
        
    sys.exit(0)

if __name__ == "__main__":
    main()

from __future__ import annotations
import sys
import os
import yaml  # type: ignore
import json
from termforge.config.loader import serialize_toml

MINIMAL_CONFIG = {
    "theme": "nord",
    "components": [
        {
            "spec_type": "window",
            "properties": {
                "title": "Hello World",
                "border_style": "rounded"
            },
            "children": [
                {
                    "spec_type": "text",
                    "properties": {
                        "text": "Welcome to TermForge!",
                        "align": "center"
                    }
                }
            ]
        }
    ]
}

DASHBOARD_CONFIG = {
    "theme": "dracula",
    "components": [
        {
            "spec_type": "pane",
            "properties": {
                "direction": "column"
            },
            "children": [
                {
                    "spec_type": "window",
                    "properties": {
                        "title": "Main Table",
                        "height": 10
                    },
                    "children": [
                        {
                            "spec_type": "text",
                            "properties": {
                                "text": "Data Table Placeholder"
                            }
                        }
                    ]
                },
                {
                    "spec_type": "pane",
                    "properties": {
                        "direction": "row"
                    },
                    "children": [
                        {
                            "spec_type": "window",
                            "properties": {
                                "title": "Chart Pane",
                                "flex_grow": 1.0
                            },
                            "children": [
                                {
                                    "spec_type": "text",
                                    "properties": {
                                        "text": "Line Chart Placeholder"
                                    }
                                }
                            ]
                        },
                        {
                            "spec_type": "window",
                            "properties": {
                                "title": "Summary Panel",
                                "width": 30
                            },
                            "children": [
                                {
                                    "spec_type": "text",
                                    "properties": {
                                        "text": "Stats Panel Placeholder"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

EDITOR_CONFIG = {
    "theme": "catppuccin_mocha",
    "components": [
        {
            "spec_type": "pane",
            "properties": {
                "direction": "row"
            },
            "children": [
                {
                    "spec_type": "window",
                    "properties": {
                        "title": "Explorer",
                        "width": 25
                    },
                    "children": [
                        {
                            "spec_type": "text",
                            "properties": {
                                "text": "Directory Tree"
                            }
                        }
                    ]
                },
                {
                    "spec_type": "window",
                    "properties": {
                        "title": "File Editor",
                        "flex_grow": 1.0
                    },
                    "children": [
                        {
                            "spec_type": "text",
                            "properties": {
                                "text": "Editor Buffer Content"
                            }
                        }
                    ]
                }
            ]
        }
    ]
}

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="TermForge Layout Configuration Scaffolder")
    parser.add_argument("path", help="Target path to output file layout stub")
    parser.add_argument("--type", "-t", choices=["minimal", "dashboard", "editor"], default="minimal", help="Template type structure (default: minimal)")
    parser.add_argument("--format", "-f", choices=["yaml", "toml", "json"], help="Output configuration file format (yaml/toml/json)")
    args = parser.parse_args()
    
    fmt = args.format
    if not fmt:
        ext = os.path.splitext(args.path)[1].lower()
        if ext in (".yaml", ".yml"):
            fmt = "yaml"
        elif ext == ".toml":
            fmt = "toml"
        elif ext == ".json":
            fmt = "json"
        else:
            fmt = "yaml"
            
    templates = {
        "minimal": MINIMAL_CONFIG,
        "dashboard": DASHBOARD_CONFIG,
        "editor": EDITOR_CONFIG
    }
    
    config_dict = templates[args.type]
    
    try:
        dirname = os.path.dirname(args.path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
            
        if fmt == "yaml":
            with open(args.path, "w", encoding="utf-8") as f:
                f.write(f"# TermForge {args.type.capitalize()} Layout Configuration\n")
                yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
        elif fmt == "json":
            with open(args.path, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2)
        elif fmt == "toml":
            with open(args.path, "w", encoding="utf-8") as f:
                f.write(f"# TermForge {args.type.capitalize()} Layout Configuration\n")
                f.write(serialize_toml(config_dict))
        else:
            print(f"Error: Unsupported format {fmt}")
            sys.exit(1)
            
        print(f"✅ Successfully initialized {args.type} layout configuration at {args.path}")
    except Exception as e:
        print(f"Error scaffolding configuration: {e}")
        sys.exit(1)
        
    sys.exit(0)

if __name__ == "__main__":
    main()

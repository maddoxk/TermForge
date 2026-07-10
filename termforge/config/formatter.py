from __future__ import annotations
import os
import json
import yaml  # type: ignore
from typing import Any
from termforge.config.loader import serialize_toml

try:
    import tomllib  # type: ignore
except ImportError:
    tomllib = None

KEY_ORDER = ["theme", "title", "keybindings", "components", "spec_type", "properties", "children"]
PROP_ORDER = [
    "width", "height", "text", "align", "image_path", "fidelity", 
    "border_style", "shadow", "status_tags", "direction", "gap", 
    "ratios", "margin", "padding", "flex_grow", "flex_shrink"
]

def sort_config_dict(d: Any) -> Any:
    if isinstance(d, list):
        return [sort_config_dict(item) for item in d]
    elif isinstance(d, dict):
        sorted_d = {}
        def key_sorter(k: str) -> tuple[int, str]:
            if k in KEY_ORDER:
                return (KEY_ORDER.index(k), k)
            if k in PROP_ORDER:
                return (len(KEY_ORDER) + PROP_ORDER.index(k), k)
            return (len(KEY_ORDER) + len(PROP_ORDER), k)
            
        keys = sorted(d.keys(), key=key_sorter)
        for k in keys:
            sorted_d[k] = sort_config_dict(d[k])
        return sorted_d
    return d

def format_config_file(path: str, write: bool = False) -> str:
    """Format and sort configuration dictionary keys systematically."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} does not exist.")
        
    ext = os.path.splitext(path)[1].lower()
    formatted: str = ""
    
    if ext in (".yaml", ".yml"):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        sorted_data = sort_config_dict(data)
        formatted = str(yaml.dump(sorted_data, default_flow_style=False, sort_keys=False))
    elif ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        sorted_data = sort_config_dict(data)
        formatted = json.dumps(sorted_data, indent=2) + "\n"
    elif ext == ".toml":
        with open(path, "rb") as f:
            if tomllib:
                data = tomllib.load(f)
            else:
                raise ImportError("TOML support requires Python 3.11+ (tomllib)")
        sorted_data = sort_config_dict(data)
        formatted = serialize_toml(sorted_data) + "\n"
    else:
        raise ValueError(f"Unsupported file format {ext}")
        
    if write:
        with open(path, "w", encoding="utf-8") as f:
            f.write(formatted)
            
    return formatted

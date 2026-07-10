from __future__ import annotations
import os
from termforge.config.loader import (
    load_config_yaml, load_config_json, load_config_toml,
    config_to_specs, save_config_to_file
)

def convert_config_file(input_path: str, output_path: str) -> None:
    """Read a TermForge configuration file and write it back in a different format."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} does not exist.")
        
    input_ext = os.path.splitext(input_path)[1].lower()
    if input_ext in (".yaml", ".yml"):
        config = load_config_yaml(input_path)
    elif input_ext == ".json":
        config = load_config_json(input_path)
    elif input_ext == ".toml":
        config = load_config_toml(input_path)
    else:
        raise ValueError(f"Unsupported input extension: {input_ext}")
        
    specs = config_to_specs(config)
    
    output_ext = os.path.splitext(output_path)[1].lower()
    if output_ext in (".yaml", ".yml"):
        fmt = "yaml"
    elif output_ext == ".json":
        fmt = "json"
    elif output_ext == ".toml":
        fmt = "toml"
    else:
        raise ValueError(f"Unsupported output extension: {output_ext}")
        
    save_config_to_file(
        spec=specs,
        path=output_path,
        format=fmt,
        theme=config.theme,
        title=config.title
    )

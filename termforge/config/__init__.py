"""TermForge config module — declarative YAML/TOML/JSON specs loader."""
from termforge.config.types import ComponentConfig, LayoutConfig
from termforge.config.loader import load_config_yaml, load_config_json, load_config_toml, config_to_specs, save_config_to_file
from termforge.config.validator import validate_config, LineNumberLoader
from termforge.config.input import InputBindingSpec, InputRouter
from termforge.config.schema import generate_json_schema
from termforge.config.formatter import format_config_file
from termforge.config.converter import convert_config_file

__all__ = [
    "ComponentConfig",
    "LayoutConfig",
    "load_config_yaml",
    "load_config_json",
    "load_config_toml",
    "config_to_specs",
    "save_config_to_file",
    "validate_config",
    "LineNumberLoader",
    "InputBindingSpec",
    "InputRouter",
    "generate_json_schema",
    "format_config_file",
    "convert_config_file",
]

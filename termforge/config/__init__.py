"""TermForge config module — declarative YAML/TOML/JSON specs loader."""
from termforge.config.types import ComponentConfig, LayoutConfig
from termforge.config.loader import load_config_yaml, load_config_json, load_config_toml, config_to_specs

__all__ = [
    "ComponentConfig",
    "LayoutConfig",
    "load_config_yaml",
    "load_config_json",
    "load_config_toml",
    "config_to_specs",
]

from __future__ import annotations
import json
import yaml  # type: ignore
from typing import Any
from termforge.core.types import RenderableSpec
from termforge.config.types import LayoutConfig, ComponentConfig

# Try importing tomllib (Python 3.11+)
try:
    import tomllib  # type: ignore
except ImportError:
    # simple fallback mapping if tomllib not present
    tomllib = None

def load_config_yaml(path: str) -> LayoutConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return LayoutConfig.from_dict(data)

def load_config_json(path: str) -> LayoutConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return LayoutConfig.from_dict(data)

def load_config_toml(path: str) -> LayoutConfig:
    with open(path, "rb") as f:
        if tomllib:
            data = tomllib.load(f)
        else:
            # Fallback raise
            raise ImportError("TOML support requires Python 3.11+ (tomllib)")
    return LayoutConfig.from_dict(data)

def map_component(config: ComponentConfig) -> RenderableSpec:
    from termforge.text.types import TextSpec
    from termforge.image.types import ImageSpec
    from termforge.charts.types import ChartSpec
    from termforge.borders.types import BorderSpec
    from termforge.windows.types import WindowSpec, PaneSpec, ModalSpec
    from termforge.logos.types import LogoSpec, BannerSpec
    from termforge.animation.types import SpinnerSpec, TransitionSpec
    
    spec_classes = {
        "text": TextSpec,
        "image": ImageSpec,
        "chart": ChartSpec,
        "border": BorderSpec,
        "window": WindowSpec,
        "pane": PaneSpec,
        "modal": ModalSpec,
        "logo": LogoSpec,
        "banner": BannerSpec,
        "spinner": SpinnerSpec,
        "transition": TransitionSpec
    }
    
    spec_type = config.spec_type.lower()
    cls: Any = spec_classes.get(spec_type)
    if not cls:
        raise ValueError(f"Unknown component type: {spec_type}")
        
    # Reconstruct from properties dictionary
    spec: Any = cls.from_dict(config.properties)
    
    # Process children recursively
    if spec_type in ("window", "border", "modal"):
        if config.children:
            spec.content = map_component(config.children[0])
    elif spec_type == "pane":
        spec.children = [map_component(c) for c in config.children]
        
    from typing import cast
    return cast(RenderableSpec, spec)

def config_to_specs(config: LayoutConfig) -> list[RenderableSpec]:
    return [map_component(c) for c in config.components]

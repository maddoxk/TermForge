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
    from termforge.keyvalue.types import KeyValueItemSpec, KeyValueGridSpec
    from termforge.keylegend.types import KeyLegendSpec
    from termforge.logging.types import LogStreamerSpec
    from termforge.navigation.types import BreadcrumbsSpec
    from termforge.menu.types import MenuBarSpec
    from termforge.statusbar.types import StatusBarSpec
    from termforge.tooltip.types import TooltipSpec
    from termforge.toast.types import ToastSpec
    from termforge.search.types import SearchBarSpec
    from termforge.checklist.types import ChecklistSpec
    from termforge.combobox.types import ComboboxSpec
    from termforge.toggle.types import ToggleSwitchSpec
    from termforge.slider.types import SliderSpec
    from termforge.radio.types import RadioButtonSpec
    
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
        "transition": TransitionSpec,
        "keyvalue_grid": KeyValueGridSpec,
        "keyvalue_item": KeyValueItemSpec,
        "key_legend": KeyLegendSpec,
        "log_streamer": LogStreamerSpec,
        "breadcrumbs": BreadcrumbsSpec,
        "menu_bar": MenuBarSpec,
        "status_bar": StatusBarSpec,
        "tooltip": TooltipSpec,
        "toast": ToastSpec,
        "search_bar": SearchBarSpec,
        "checklist": ChecklistSpec,
        "combobox": ComboboxSpec,
        "toggle_switch": ToggleSwitchSpec,
        "slider": SliderSpec,
        "radio_button": RadioButtonSpec,
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

def spec_to_component(spec: RenderableSpec) -> ComponentConfig:
    d = spec.to_dict()
    spec_type = d.pop("spec_type", spec.spec_type)
    
    children_configs = []
    # If the spec is a window, border, or modal, pop 'content' and serialize recursively
    if hasattr(spec, "content") and isinstance(spec.content, RenderableSpec):
        d.pop("content", None)
        children_configs.append(spec_to_component(spec.content))
    # If the spec is a pane, pop 'children' and serialize recursively
    elif hasattr(spec, "children") and isinstance(spec.children, list) and all(isinstance(c, RenderableSpec) for c in spec.children):
        d.pop("children", None)
        for child in spec.children:
            children_configs.append(spec_to_component(child))
            
    return ComponentConfig(
        spec_type=spec_type,
        properties=d,
        children=children_configs
    )

def toml_value(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    elif isinstance(v, (int, float)):
        return str(v)
    elif isinstance(v, str):
        escaped = v.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
        return f'"{escaped}"'
    elif isinstance(v, list):
        if not v:
            return "[]"
        items = [toml_value(x) for x in v]
        return "[" + ", ".join(items) + "]"
    elif isinstance(v, dict):
        parts = []
        for k, val in v.items():
            if val is not None:
                parts.append(f"{k} = {toml_value(val)}")
        return "{ " + ", ".join(parts) + " }"
    return f'"{v}"'

def serialize_toml(data: dict[str, Any], parent_key: str = "") -> str:
    lines = []
    
    # 1. Primitives (including inline tables/lists)
    for k, v in data.items():
        if v is None:
            continue
        if not isinstance(v, list):
            lines.append(f"{k} = {toml_value(v)}")
        elif v and not isinstance(v[0], dict):
            lines.append(f"{k} = {toml_value(v)}")
            
    # 2. Array of tables (lists of dicts)
    for k, v in data.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            current_key = f"{parent_key}.{k}" if parent_key else k
            for item in v:
                lines.append(f"\n[[{current_key}]]")
                lines.append(serialize_toml(item, parent_key=current_key))
                
    return "\n".join(lines)

def save_config_to_file(
    spec: RenderableSpec | list[RenderableSpec],
    path: str,
    format: str = "yaml",
    theme: str | None = None,
    title: str | None = None
) -> None:
    specs = spec if isinstance(spec, list) else [spec]
    components = [spec_to_component(s) for s in specs]
    layout_config = LayoutConfig(
        components=components,
        theme=theme,
        title=title
    )
    
    data = layout_config.to_dict()
    format_lower = format.lower()
    
    if format_lower == "yaml":
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    elif format_lower == "json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    elif format_lower == "toml":
        with open(path, "w", encoding="utf-8") as f:
            f.write(serialize_toml(data))
    else:
        raise ValueError(f"Unsupported format: {format}")

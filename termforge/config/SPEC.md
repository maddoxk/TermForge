# TermForge Configuration Specification

This specification defines the declarative layout schema mapping configurations to spec instances.

## 1. Schema Definition

Declarative files (JSON, YAML, TOML) map 1:1 to ComponentConfigs.

### `ComponentConfig`
- `spec_type`: string (e.g., `"window"`, `"pane"`, `"text"`, `"chart"`, `"logo"`)
- `properties`: key-value map of parameters mapping to the spec class fields.
- `children`: list of nested `ComponentConfig` elements.

### `LayoutConfig`
- `components`: list of root `ComponentConfig` elements.
- `theme`: string | null (name of the theme pack, e.g., `"catppuccin_mocha"`)
- `title`: string | null

---

## 2. Parsing Algorithm

Converts ComponentConfig nodes recursively into typed `RenderableSpec` subclasses.

#### Pseudocode:
```
function map_component(config: ComponentConfig) -> RenderableSpec:
    cls = get_class_for_type(config.spec_type)
    spec = cls.from_dict(config.properties)
    
    if is_container(config.spec_type):
        if config.spec_type == "pane":
            spec.children = [map_component(c) for c in config.children]
        else:
            # window, border, modal
            if length(config.children) > 0:
                spec.content = map_component(config.children[0])
                
    return spec
```

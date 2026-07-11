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

---

## 3. Exporter Algorithm

Converts spec hierarchies back to structural ComponentConfig nodes and saves them in TOML, YAML, or JSON.

#### Pseudocode:
```
function spec_to_component(spec: RenderableSpec) -> ComponentConfig:
    properties = spec.to_dict()
    spec_type = properties.pop("spec_type")
    
    children = []
    if has_field(spec, "content") and spec.content is not null:
        properties.pop("content")
        children.append(spec_to_component(spec.content))
    elif has_field(spec, "children"):
        properties.pop("children")
        for child in spec.children:
            children.append(spec_to_component(child))
            
    return ComponentConfig(spec_type, properties, children)

---

## 4. Declarative Forms & Validation

Allows collecting user inputs via a structured form of text inputs, textareas, or checkboxes, with built-in validation constraints.

### FieldType (enum)
- `TEXT`: Standard single-line text input field.
- `CHECKBOX`: Boolean selection checkbox.
- `TEXTAREA`: Multi-line text block field.

### FormFieldSpec

| Field | Type | Description |
|-------|------|-------------|
| name | string | Internal key for the field data |
| label | string | User-facing display label |
| field_type | FieldType | Input field type (default TEXT) |
| placeholder | string | Optional helper text |
| default_value | Any | Default value for the field |
| validation_rules | dict | Validation constraints (required, choices, numeric, etc.) |

### FormSpec

| Field | Type | Description |
|-------|------|-------------|
| title | string | Optional form title |
| fields | list[FormFieldSpec] | List of fields in the form |

### `validate(data)` -> (is_valid: bool, errors: dict[str, str])
Runs validation constraints across data:
- `required`: Non-null and non-empty string.
- `choices`: Must exist inside allowed values list.
- `numeric`: Must parse as a float/int.
- `min_length`: String must satisfy minimum character length.
- `max_length`: String must satisfy maximum character length.
- `regex`: String must match regular expression pattern.


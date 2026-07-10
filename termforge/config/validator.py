from __future__ import annotations
import os
import yaml  # type: ignore
import json
from typing import Any
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.theme.contrast import check_contrast, ColorValue
from termforge.theme.types import ThemePack

class LineNumberLoader(yaml.SafeLoader):
    def construct_mapping(self, node: Any, deep: bool = False) -> Any:
        mapping = super().construct_mapping(node, deep=deep)
        mapping["__line__"] = node.start_mark.line + 1
        return mapping

def validate_properties(properties: dict[str, Any], spec_type: str, line: int, errors: list[str]) -> None:
    for prop in ("width", "height"):
        if prop in properties:
            val = properties[prop]
            if val is not None:
                if not isinstance(val, int) or val < 0:
                    errors.append(f"[Line {line}] Error: Property '{prop}' in '{spec_type}' must be a non-negative integer, got {val}")
                    
    if "gap" in properties:
        val = properties["gap"]
        if val is not None:
            if not isinstance(val, int) or val < 0:
                errors.append(f"[Line {line}] Error: Property 'gap' in '{spec_type}' must be a non-negative integer, got {val}")

def validate_component(comp: dict[str, Any], errors: list[str]) -> None:
    line = comp.get("__line__", 1)
    if "spec_type" not in comp:
        errors.append(f"[Line {line}] Error: Missing 'spec_type' in component configuration.")
        return
        
    spec_type = comp["spec_type"]
    known_types = {
        "text", "image", "chart", "border", "window",
        "pane", "modal", "logo", "banner", "spinner", "transition"
    }
    if spec_type.lower() not in known_types:
        errors.append(f"[Line {line}] Error: Unknown component type: '{spec_type}'")
        
    properties = comp.get("properties", {})
    validate_properties(properties, spec_type, line, errors)
    
    children = comp.get("children", [])
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                validate_component(child, errors)
    elif isinstance(children, dict):
        validate_component(children, errors)

def validate_theme_contrast(theme_pack: ThemePack, line: int, errors: list[str]) -> None:
    results = check_contrast(theme_pack)
    for res in results:
        if not res["passes_aa"]:
            errors.append(
                f"[Line {line}] Warning: Contrast ratio for '{res['fg_token']}' on '{res['bg_token']}' is {res['ratio']}, "
                f"which fails WCAG AA standards (minimum 4.5)."
            )

def check_circular_references(obj: Any, visited: dict[int, str], path: list[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, (dict, list)):
        return errors
        
    obj_id = id(obj)
    if obj_id in visited:
        cycle_start = visited[obj_id]
        cycle_path = " -> ".join(path + [cycle_start])
        return [f"Error: Circular reference detected in component graph: {cycle_path}"]
        
    if isinstance(obj, dict):
        spec_type = obj.get("spec_type", "unknown")
        line = obj.get("__line__", "?")
        label = f"{spec_type} (line {line})"
        
        new_visited = dict(visited)
        new_visited[obj_id] = label
        
        for k, v in obj.items():
            if k == "__line__":
                continue
            errors.extend(check_circular_references(v, new_visited, path + [f"{label}.{k}"]))
            
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            errors.extend(check_circular_references(item, visited, path + [f"[{idx}]"]))
            
    return errors

def validate_config(data: dict[str, Any], check_cyclic: bool = False) -> list[str]:
    errors: list[str] = []
    line = data.get("__line__", 1)
    
    cyclic_errors = check_circular_references(data, {}, [])
    if cyclic_errors:
        # If user explicitly wants cyclic checking, report it; otherwise it is still fatal
        errors.extend(cyclic_errors)
        return errors
        
    if "meta" in data and "tokens" in data:
        try:
            theme_pack = ThemePack.from_dict(data)
            validate_theme_contrast(theme_pack, line, errors)
        except Exception as e:
            errors.append(f"[Line {line}] Error: Invalid ThemePack format: {e}")
        return errors
        
    if "components" in data:
        components = data["components"]
        if not isinstance(components, list):
            errors.append(f"[Line {line}] Error: 'components' must be a list.")
        else:
            for comp in components:
                if isinstance(comp, dict):
                    validate_component(comp, errors)
                    
    theme_name = data.get("theme")
    if theme_name:
        if theme_name in BUILTIN_THEMES:
            validate_theme_contrast(BUILTIN_THEMES[theme_name], line, errors)
        else:
            if os.path.exists(theme_name):
                try:
                    with open(theme_name, "r", encoding="utf-8") as f:
                        theme_data = yaml.load(f, Loader=LineNumberLoader)
                    theme_pack = ThemePack.from_dict(theme_data)
                    validate_theme_contrast(theme_pack, line, errors)
                except Exception as e:
                    errors.append(f"[Line {line}] Error: Referenced theme file '{theme_name}' is invalid: {e}")
            else:
                errors.append(f"[Line {line}] Error: Referenced theme '{theme_name}' is not a built-in theme or a valid file.")
                
    return errors

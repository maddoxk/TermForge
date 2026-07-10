from __future__ import annotations
from typing import Any

def generate_json_schema() -> dict[str, Any]:
    """Generate Draft-07 JSON Schema for TermForge declarative layout configurations."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "TermForgeLayoutConfig",
        "type": "object",
        "properties": {
            "theme": {"type": ["string", "null"]},
            "title": {"type": ["string", "null"]},
            "keybindings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"},
                        "action": {"type": "string"}
                    },
                    "required": ["key", "action"]
                }
            },
            "components": {
                "type": "array",
                "items": {"$ref": "#/definitions/ComponentConfig"}
            }
        },
        "required": ["components"],
        "definitions": {
            "ComponentConfig": {
                "type": "object",
                "properties": {
                    "spec_type": {
                        "type": "string",
                        "enum": [
                            "text", "image", "chart", "border", "window",
                            "pane", "modal", "logo", "banner", "spinner", "transition"
                        ]
                    },
                    "properties": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "align": {"type": "string", "enum": ["left", "center", "right"]},
                            "width": {"type": "integer", "minimum": 0},
                            "height": {"type": "integer", "minimum": 0},
                            "image_path": {"type": "string"},
                            "fidelity": {"type": "string", "enum": ["half_block", "ascii"]},
                            "title": {"type": "string"},
                            "border_style": {"type": "string", "enum": ["single", "double", "rounded", "heavy", "ascii"]},
                            "shadow": {"type": "boolean"},
                            "status_tags": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "direction": {"type": "string", "enum": ["row", "column"]},
                            "gap": {"type": "integer", "minimum": 0},
                            "ratios": {
                                "type": "array",
                                "items": {"type": "number"}
                            },
                            "margin": {"$ref": "#/definitions/Spacing"},
                            "padding": {"$ref": "#/definitions/Spacing"},
                            "flex_grow": {"type": "number", "minimum": 0.0},
                            "flex_shrink": {"type": "number", "minimum": 0.0}
                        }
                    },
                    "children": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/ComponentConfig"}
                    }
                },
                "required": ["spec_type"]
            },
            "Spacing": {
                "type": "object",
                "properties": {
                    "top": {"type": "integer", "minimum": 0},
                    "bottom": {"type": "integer", "minimum": 0},
                    "left": {"type": "integer", "minimum": 0},
                    "right": {"type": "integer", "minimum": 0}
                }
            }
        }
    }
    return schema

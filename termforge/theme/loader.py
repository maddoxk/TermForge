from __future__ import annotations
import json
import yaml  # type: ignore
from termforge.theme.types import ThemePack

def load_theme_yaml(path: str) -> ThemePack:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return ThemePack.from_dict(data)

def load_theme_json(path: str) -> ThemePack:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return ThemePack.from_dict(data)

def save_theme_yaml(theme: ThemePack, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(theme.to_dict(), f, sort_keys=False)

def save_theme_json(theme: ThemePack, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(theme.to_dict(), f, indent=2)

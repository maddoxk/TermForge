from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from termforge.core.theme import ThemeTokens

@dataclass
class ThemeMeta:
    name: str
    author: str
    version: str
    description: str
    dark: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "author": self.author,
            "version": self.version,
            "description": self.description,
            "dark": self.dark
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ThemeMeta:
        return cls(
            name=d["name"],
            author=d["author"],
            version=d["version"],
            description=d["description"],
            dark=d.get("dark", True)
        )

@dataclass
class ThemePack:
    meta: ThemeMeta
    tokens: ThemeTokens

    def to_dict(self) -> dict[str, Any]:
        from termforge.core.theme import theme_to_dict
        return {
            "meta": self.meta.to_dict(),
            "tokens": theme_to_dict(self.tokens)
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ThemePack:
        from termforge.core.theme import load_theme_from_dict
        return cls(
            meta=ThemeMeta.from_dict(d["meta"]),
            tokens=load_theme_from_dict(d["tokens"])
        )

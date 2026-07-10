import pytest
import tempfile
import os
from termforge.config.types import LayoutConfig, ComponentConfig
from termforge.config.loader import load_config_yaml, config_to_specs
from termforge.windows.types import WindowSpec, PaneSpec
from termforge.text.types import TextSpec

def test_config_serialization():
    comp = ComponentConfig(
        spec_type="window",
        properties={"title": "Main Window", "width": 80},
        children=[ComponentConfig(spec_type="text", properties={"content": "Hello"})]
    )
    config = LayoutConfig(components=[comp], theme="dracula")
    
    config_dict = config.to_dict()
    assert config_dict["theme"] == "dracula"
    assert config_dict["components"][0]["spec_type"] == "window"
    assert len(config_dict["components"][0]["children"]) == 1

def test_config_mapping():
    comp = ComponentConfig(
        spec_type="window",
        properties={"title": "Sidebar", "width": 20},
        children=[ComponentConfig(spec_type="text", properties={"content": "Hello"})]
    )
    config = LayoutConfig(components=[comp])
    specs = config_to_specs(config)
    
    assert len(specs) == 1
    assert isinstance(specs[0], WindowSpec)
    assert specs[0].title == "Sidebar"
    assert isinstance(specs[0].content, TextSpec)
    assert specs[0].content.content == "Hello"

def test_yaml_config_loading():
    yaml_content = """
theme: catppuccin_mocha
title: Dashboard Layout
components:
  - spec_type: window
    properties:
      title: Info Panel
      width: 40
      height: 10
    children:
      - spec_type: text
        properties:
          content: "[bold]TermForge[/bold] Dashboard"
          align: center
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(yaml_content)
        path = f.name
        
    try:
        config = load_config_yaml(path)
        assert config.theme == "catppuccin_mocha"
        assert config.title == "Dashboard Layout"
        assert len(config.components) == 1
        
        specs = config_to_specs(config)
        assert isinstance(specs[0], WindowSpec)
        assert specs[0].title == "Info Panel"
        assert isinstance(specs[0].content, TextSpec)
    finally:
        if os.path.exists(path):
            os.remove(path)

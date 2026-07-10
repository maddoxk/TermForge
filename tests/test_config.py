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

def test_save_config_to_file():
    from termforge.config.loader import save_config_to_file, load_config_toml, load_config_yaml, load_config_json
    spec = WindowSpec(
        title="Settings Window",
        width=50,
        height=15,
        content=TextSpec(content="Hello Export")
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Save as TOML
        toml_path = os.path.join(tmpdir, "layout.toml")
        save_config_to_file(spec, toml_path, format="toml", theme="nord", title="Settings Layout")
        
        # Load back and verify
        config_toml = load_config_toml(toml_path)
        assert config_toml.theme == "nord"
        assert config_toml.title == "Settings Layout"
        specs_toml = config_to_specs(config_toml)
        assert len(specs_toml) == 1
        assert specs_toml[0].title == "Settings Window"
        assert specs_toml[0].width == 50
        assert specs_toml[0].content.content == "Hello Export"
        
        # 2. Save as YAML
        yaml_path = os.path.join(tmpdir, "layout.yaml")
        save_config_to_file(spec, yaml_path, format="yaml", theme="dracula")
        
        config_yaml = load_config_yaml(yaml_path)
        assert config_yaml.theme == "dracula"
        specs_yaml = config_to_specs(config_yaml)
        assert specs_yaml[0].title == "Settings Window"
        
        # 3. Save as JSON
        json_path = os.path.join(tmpdir, "layout.json")
        save_config_to_file(spec, json_path, format="json", theme="tokyo_night")
        
        config_json = load_config_json(json_path)
        assert config_json.theme == "tokyo_night"
        specs_json = config_to_specs(config_json)
        assert specs_json[0].title == "Settings Window"

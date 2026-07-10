import os
import tempfile
import yaml
from termforge.config import load_config_yaml, InputRouter, InputBindingSpec

def test_declarative_keybindings_loading():
    yaml_content = """
theme: dracula
title: Console App
keybindings:
  - key: q
    action: quit
  - key: ctrl+c
    action: quit
  - key: tab
    action: focus_next
components:
  - spec_type: window
    properties:
      title: Main Window
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(yaml_content)
        path = f.name
        
    try:
        config = load_config_yaml(path)
        assert config.theme == "dracula"
        assert config.title == "Console App"
        assert len(config.keybindings) == 3
        
        bindings = config.keybindings
        assert bindings[0].key == "q"
        assert bindings[0].action == "quit"
        assert bindings[1].key == "ctrl+c"
        assert bindings[1].action == "quit"
        assert bindings[2].key == "tab"
        assert bindings[2].action == "focus_next"
        
        # Test routing
        router = InputRouter(bindings=bindings)
        assert router.route("q") == "quit"
        assert router.route("Q") == "quit"
        assert router.route(" ctrl+c ") == "quit"
        assert router.route("tab") == "focus_next"
        assert router.route("escape") is None
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_multikey_combo_routing():
    bindings = [
        InputBindingSpec(key="ctrl+k c", action="create_window"),
        InputBindingSpec(key="ctrl+k d", action="delete_window"),
        InputBindingSpec(key="escape", action="cancel"),
        InputBindingSpec(key="g g", action="scroll_top")
    ]
    router = InputRouter(bindings=bindings)
    
    # 1. Test multi-key combo "ctrl+k c"
    assert router.route("ctrl+k") is None
    assert router.route("c") == "create_window"
    
    # 2. Test multi-key combo "ctrl+k d"
    assert router.route("ctrl+k") is None
    assert router.route("d") == "delete_window"
    
    # 3. Test failed chord reset & fallback (starts with invalid second key)
    assert router.route("ctrl+k") is None
    assert router.route("x") is None
    
    # 4. Test "escape" (single key)
    assert router.route("escape") == "cancel"
    
    # 5. Test "g g"
    assert router.route("g") is None
    assert router.route("g") == "scroll_top"

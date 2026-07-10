#!/usr/bin/env python3
import sys
import os
import tempfile
from termforge.core import Size, ColorDepth
from termforge.config.loader import load_config_yaml, config_to_specs
from termforge.windows.types import WindowSpec, PaneSpec
from termforge.windows.compositor import compose_panes, render_window
from termforge.text.types import TextSpec
from termforge.text.render import render_text
from termforge.charts.types import ChartSpec
from termforge.charts.chart import render_chart

def create_yaml_config() -> str:
    yaml_content = """
theme: catppuccin_mocha
title: Declarative Layout Demo
components:
  - spec_type: window
    properties:
      title: System Dashboard
      width: 60
      height: 12
    children:
      - spec_type: pane
        properties:
          direction: row
          ratios: [1.0, 2.0]
          gap: 0
        children:
          - spec_type: text
            properties:
              content: "[bold]CPU Load[/bold]\\nCore 1: 45%\\nCore 2: 60%\\nCore 3: 12%"
              align: left
          - spec_type: chart
            properties:
              chart_type: bar
              series:
                - name: cpu_usage
                  data: [45.0, 60.0, 12.0]
              width: 38
              height: 10
              show_legend: false
"""
    fd, path = tempfile.mkstemp(suffix=".yaml")
    with os.fdopen(fd, "w") as f:
        f.write(yaml_content)
    return path

def main() -> None:
    path = create_yaml_config()
    try:
        # Load and parse config
        config = load_config_yaml(path)
        specs = config_to_specs(config)
        
        main_window_spec = specs[0]
        assert isinstance(main_window_spec, WindowSpec)
        
        # Render nested layout manually to composite
        # Main window has width 60, height 12 -> inner_w=58, inner_h=10
        inner_size = Size(58, 10)
        
        pane_spec = main_window_spec.content
        assert isinstance(pane_spec, PaneSpec)
        
        # 1. Compose panes
        layouts = compose_panes(pane_spec, inner_size)
        
        # 2. Render children
        # Left pane (text)
        pos_l, size_l, spec_l = layouts[0]
        assert isinstance(spec_l, TextSpec)
        spec_l.max_width = size_l.width
        spec_l.max_lines = size_l.height
        lines_l = render_text(spec_l, available_width=size_l.width)
        # Pad lines_l to size_l.height
        lines_l += [" " * size_l.width] * (size_l.height - len(lines_l))
        
        # Right pane (chart)
        pos_r, size_r, spec_r = layouts[1]
        assert isinstance(spec_r, ChartSpec)
        spec_r.width = size_r.width
        spec_r.height = size_r.height
        lines_r = render_chart(spec_r)
        lines_r += [" " * size_r.width] * (size_r.height - len(lines_r))
        
        # 3. Composite body lines
        body_lines = []
        for r in range(inner_size.height):
            # Left pane line + right pane line
            body_lines.append(lines_l[r] + lines_r[r])
            
        # 4. Render outer Window Spec enclosing the composited body lines
        final_screen = render_window(main_window_spec, body_lines, depth=ColorDepth.TRUECOLOR)
        
        print("--- Declarative Config Rendered Layout ---")
        for line in final_screen:
            print(line)
            
    finally:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    main()

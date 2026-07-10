from __future__ import annotations
from termforge.core.types import Size
from termforge.core.theme import ThemeTokens
from termforge.tree.types import TreeSpec, TreeNodeSpec
from termforge.text.types import TextSpec
from termforge.text.render import render_text

def render_tree(spec: TreeSpec, max_size: Size, theme: ThemeTokens) -> list[str]:
    lines = []
    
    def traverse(nodes: list[TreeNodeSpec], depth: int, is_last_list: list[bool]) -> None:
        for i, node in enumerate(nodes):
            is_last = (i == len(nodes) - 1)
            
            prefix = ""
            for j in range(depth):
                if is_last_list[j]:
                    prefix += " " * spec.indent_size
                else:
                    prefix += "│" + " " * (spec.indent_size - 1)
                    
            if depth > 0:
                if is_last:
                    prefix += "└" + "─" * (spec.indent_size - 1)
                else:
                    prefix += "├" + "─" * (spec.indent_size - 1)
                    
            icon = "📂 " if node.children and node.expanded else "📁 " if node.children else "📄 "
            
            # Simple text rendering
            line = prefix + icon + node.label
            if len(line) > max_size.width:
                line = line[:max_size.width - 1] + "…"
                
            lines.append(line)
            
            if node.expanded and node.children:
                traverse(node.children, depth + 1, is_last_list + [is_last])
                
    traverse(spec.root_nodes, 0, [])
    
    return lines[:max_size.height]

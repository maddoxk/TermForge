from termforge.tree import TreeSpec, TreeNodeSpec, render_tree
from termforge.core.theme import load_theme_from_dict, TOKYO_NIGHT
from termforge.core.types import Size

def main():
    theme = load_theme_from_dict(TOKYO_NIGHT)
    
    spec = TreeSpec(
        root_nodes=[
            TreeNodeSpec(
                label="Project",
                expanded=True,
                children=[
                    TreeNodeSpec(
                        label="src",
                        expanded=True,
                        children=[
                            TreeNodeSpec(label="main.py"),
                            TreeNodeSpec(label="utils.py")
                        ]
                    ),
                    TreeNodeSpec(label="README.md")
                ]
            )
        ]
    )
    
    result = render_tree(spec, Size(40, 20), theme)
    print("\n".join(result))

if __name__ == "__main__":
    main()

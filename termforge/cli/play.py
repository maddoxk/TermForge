import sys
import os

def main() -> None:
    print("Initializing TermForge Component Playground Shell...")
    print("Preloading modules: core, text, image, charts, borders, windows, animation, logos, config, theme")
    print("Type help() or exit() to leave the REPL.")
    
    # Import everything so it is available in the REPL
    import termforge
    from termforge.core import ColorDepth, detect_capabilities
    from termforge.theme.builtin import BUILTIN_THEMES
    
    local_vars = {
        "termforge": termforge,
        "ColorDepth": ColorDepth,
        "detect_capabilities": detect_capabilities,
        "BUILTIN_THEMES": BUILTIN_THEMES,
    }
    
    import code
    sys.exit(code.interact(banner="--- TermForge Interactive Playground REPL ---", local=local_vars))

if __name__ == "__main__":
    main()

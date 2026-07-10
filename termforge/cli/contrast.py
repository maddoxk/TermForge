from __future__ import annotations
import sys
import os
import time
from termforge.theme.loader import load_theme_yaml, load_theme_json
from termforge.theme.contrast import check_contrast

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="TermForge Theme WCAG Contrast Validator")
    parser.add_argument("path", help="Path to custom theme pack configuration file (yaml/json)")
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: File {args.path} does not exist.")
        sys.exit(1)
        
    ext = os.path.splitext(args.path)[1].lower()
    
    try:
        start_time = time.perf_counter()
        if ext in (".yaml", ".yml"):
            theme = load_theme_yaml(args.path)
        elif ext == ".json":
            theme = load_theme_json(args.path)
        else:
            print(f"Error: Unsupported format {ext}")
            sys.exit(1)
            
        results = check_contrast(theme)
        elapsed = (time.perf_counter() - start_time) * 1000.0
        
        print(f"Contrast Audit for Theme: {theme.meta.name} ({elapsed:.2f}ms)")
        print("-" * 65)
        
        all_passed = True
        for res in results:
            fg = res["fg_token"]
            bg = res["bg_token"]
            ratio = res["ratio"]
            passes_aa = res["passes_aa"]
            passes_aaa = res["passes_aaa"]
            
            status = "AAA" if passes_aaa else ("AA" if passes_aa else "Fail")
            if not passes_aa:
                all_passed = False
                
            print(f"Token: {fg:<12} on {bg:<8} | Ratio: {ratio:<6} | Compliance: {status}")
            
        print("-" * 65)
        if all_passed:
            print("Status: AA Compliance Passed ✅")
            sys.exit(0)
        else:
            print("Status: Contrast Verification Failed ❌ (AA standards not met)")
            sys.exit(1)
    except Exception as e:
        print(f"Error checking theme contrast: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

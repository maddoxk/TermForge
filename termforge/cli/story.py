from __future__ import annotations
import sys
import os
import subprocess
import argparse
import difflib

def find_stories() -> list[tuple[str, str, str]]:
    # Returns list of tuples: (module_name, story_name, path_to_py_file)
    stories_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "stories"))
    results = []
    for root, _, files in os.walk(stories_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, stories_dir)
                parts = rel_path.split(os.sep)
                if len(parts) >= 2:
                    module_name = parts[0]
                    story_name = os.path.splitext(parts[1])[0]
                    results.append((module_name, story_name, path))
    return sorted(results)

def run_story_captured(path: str) -> str:
    # Run the python script with PAGER=cat and capture stdout
    env = dict(os.environ)
    env["PAGER"] = "cat"
    env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    # Run with same python interpreter
    res = subprocess.run([sys.executable, path], capture_output=True, text=True, env=env)
    if res.returncode != 0:
        raise RuntimeError(f"Story {path} exited with code {res.returncode}. Stderr: {res.stderr}")
    return res.stdout

def main() -> None:
    parser = argparse.ArgumentParser(description="TermForge Storybook CLI")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate golden files for all stories")
    args = parser.parse_args()
    
    stories = find_stories()
    if not stories:
        print("No stories found.")
        sys.exit(0)
        
    print(f"Found {len(stories)} stories.")
    failed = False
    
    for mod, name, path in stories:
        golden_path = os.path.splitext(path)[0] + ".golden.txt"
        
        try:
            output = run_story_captured(path)
        except Exception as e:
            print(f"❌ {mod}/{name} failed to execute: {e}")
            failed = True
            continue
            
        if args.regenerate:
            with open(golden_path, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"✅ {mod}/{name} golden file regenerated.")
        else:
            if not os.path.exists(golden_path):
                print(f"⚠️ {mod}/{name} golden file missing. Regenerating automatically...")
                with open(golden_path, "w", encoding="utf-8") as f:
                    f.write(output)
                continue
                
            with open(golden_path, "r", encoding="utf-8") as f:
                golden_content = f.read()
                
            if output == golden_content:
                print(f"✅ {mod}/{name} passed.")
            else:
                print(f"❌ {mod}/{name} golden mismatch!")
                # Show diff
                diff = difflib.unified_diff(
                    golden_content.splitlines(),
                    output.splitlines(),
                    fromfile="golden",
                    tofile="actual"
                )
                print("\n".join(diff))
                print()
                failed = True
                
    if failed:
        sys.exit(1)
    else:
        print("\nAll storybooks passed successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()

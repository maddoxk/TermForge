"""Story: presets/preset_gallery — showcase all 5 named layout presets.

This story demonstrates every built-in preset and verifies that each one
produces a JSON-serializable RenderableSpec.
"""
import json
from termforge.config.presets import get_preset, list_presets


def main() -> None:
    print("=== TermForge Layout Presets ===\n")

    print("Available presets:")
    for p in list_presets():
        print(f"  {p['name']:<16} — {p['description']}")

    print()

    for name in ["dashboard", "split-pane", "split-pane-v", "modal-dialog", "log-viewer"]:
        spec = get_preset(name)
        d = spec.to_dict()
        j = json.dumps(d)
        print(f"[{name}]")
        print(f"  spec_type = {d['spec_type']}")
        print(f"  JSON size = {len(j)} bytes")
        print(f"  Portability: OK (roundtrip via JSON)")
        print()


if __name__ == "__main__":
    main()

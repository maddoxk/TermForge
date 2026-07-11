"""Story: core/diff_demo — showcase structural spec diffing.

Demonstrates diff_specs(), has_changed(), and filter_changes() against
real TermForge spec objects, all with seeded/deterministic data.
"""
import json
from termforge.core.diff import (
    ChangeKind, SpecChange, diff_specs, has_changed, filter_changes,
)
from termforge.windows.types import WindowSpec, PaneSpec
from termforge.core import FlexDirection
from termforge.text.types import TextAlign


def main() -> None:
    print("=== TermForge Spec Diff Demo ===\n")

    # ------------------------------------------------------------------ 1
    print("─── 1. Flat WindowSpec field changes ───")
    before = WindowSpec(title="Dashboard", width=80, height=24, padding=0)
    after  = WindowSpec(title="Dashboard v2", width=80, height=30, padding=1)
    changes = diff_specs(before.to_dict(), after.to_dict())
    for c in changes:
        print(f"  [{c.kind.value.upper():8}] {c.path}: {c.old!r} → {c.new!r}")
    print()

    # ------------------------------------------------------------------ 2
    print("─── 2. has_changed() quick check ───")
    spec_a = WindowSpec(title="Same", width=40, height=10)
    spec_b = WindowSpec(title="Same", width=40, height=10)
    spec_c = WindowSpec(title="Different", width=40, height=10)
    print(f"  spec_a == spec_b? has_changed={has_changed(spec_a.to_dict(), spec_b.to_dict())}")
    print(f"  spec_a == spec_c? has_changed={has_changed(spec_a.to_dict(), spec_c.to_dict())}")
    print()

    # ------------------------------------------------------------------ 3
    print("─── 3. Nested PaneSpec children diff ───")
    child1_before = WindowSpec(title="Left Panel", width=40, height=20)
    child1_after  = WindowSpec(title="Left Panel — Updated", width=40, height=20)
    pane_before = PaneSpec(direction=FlexDirection.ROW, children=[child1_before])
    pane_after  = PaneSpec(direction=FlexDirection.ROW, children=[child1_after])
    nested_changes = diff_specs(pane_before.to_dict(), pane_after.to_dict())
    for c in nested_changes:
        print(f"  [{c.kind.value.upper():8}] {c.path}: {c.old!r} → {c.new!r}")
    print()

    # ------------------------------------------------------------------ 4
    print("─── 4. filter_changes() by kind ───")
    a = {"title": "Old", "width": 80}
    b = {"title": "New", "width": 80, "height": 30}
    all_changes = diff_specs(a, b)
    mods = filter_changes(all_changes, kind=ChangeKind.MODIFIED)
    added = filter_changes(all_changes, kind=ChangeKind.ADDED)
    print(f"  total changes: {len(all_changes)}")
    print(f"  MODIFIED: {[c.path for c in mods]}")
    print(f"  ADDED:    {[c.path for c in added]}")
    print()

    # ------------------------------------------------------------------ 5
    print("─── 5. Portability: SpecChange JSON round-trip ───")
    changes_for_json = diff_specs(
        WindowSpec(title="A", width=60).to_dict(),
        WindowSpec(title="B", width=80).to_dict(),
    )
    j = json.dumps([c.to_dict() for c in changes_for_json])
    restored = [SpecChange.from_dict(d) for d in json.loads(j)]
    print(f"  serialized: {len(j)} bytes")
    print(f"  restored {len(restored)} SpecChange(s)")
    for r in restored:
        print(f"    {r.path}: {r.old!r} → {r.new!r}")
    print("  Portability: OK")


if __name__ == "__main__":
    main()

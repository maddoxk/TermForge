"""TermForge spec diff — structural change detection between two RenderableSpec dicts.

Computes a list of :class:`SpecChange` records describing every field that was
added, removed, or modified when going from spec *a* to spec *b*.

Design principles (portability contract):
- Pure functions only — no Rich/Textual types, no I/O, no side effects.
- Input and output are plain JSON-compatible dicts/lists.
- :class:`SpecChange` is itself JSON-serializable via :meth:`SpecChange.to_dict`.
- Thread-safe by construction (stateless functions).

Example::

    from termforge.core.diff import diff_specs, SpecChange, ChangeKind
    from termforge.windows.types import WindowSpec

    before = WindowSpec(title="Old", width=80, height=24)
    after  = WindowSpec(title="New", width=80, height=30)

    changes = diff_specs(before.to_dict(), after.to_dict())
    # [SpecChange(path='title',  kind=MODIFIED, old='Old', new='New'),
    #  SpecChange(path='height', kind=MODIFIED, old=24,    new=30)]

    for c in changes:
        print(c)  # SpecChange(path='title', kind='modified', old='Old', new='New')

    # All changes are JSON-serializable
    import json
    json.dumps([c.to_dict() for c in changes])
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Public data model
# ---------------------------------------------------------------------------

class ChangeKind(str, Enum):
    """The nature of a change between two specs."""
    ADDED    = "added"    #: key/element present in *b* but not in *a*
    REMOVED  = "removed"  #: key/element present in *a* but not in *b*
    MODIFIED = "modified" #: key/element present in both but with different values


@dataclass
class SpecChange:
    """A single field-level change between two ``RenderableSpec`` dicts.

    Attributes:
        path: Dot-separated path to the changed value, e.g.
            ``"children.0.border_style"`` or ``"y_axis.min_val"``.
        kind: Whether the value was :attr:`~ChangeKind.ADDED`,
            :attr:`~ChangeKind.REMOVED`, or :attr:`~ChangeKind.MODIFIED`.
        old: The previous value (``None`` for :attr:`~ChangeKind.ADDED`).
        new: The new value (``None`` for :attr:`~ChangeKind.REMOVED`).
    """

    path: str
    kind: ChangeKind
    old: Any
    new: Any

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict with keys ``path``, ``kind``, ``old``, ``new``.
        """
        return {
            "path": self.path,
            "kind": self.kind.value,
            "old": self.old,
            "new": self.new,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SpecChange":
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict with keys ``path``, ``kind``, ``old``, ``new``.

        Returns:
            A new :class:`SpecChange` instance.
        """
        return cls(
            path=d["path"],
            kind=ChangeKind(d["kind"]),
            old=d.get("old"),
            new=d.get("new"),
        )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"SpecChange(path={self.path!r}, kind={self.kind.value!r}, "
            f"old={self.old!r}, new={self.new!r})"
        )


# ---------------------------------------------------------------------------
# Core diff algorithm
# ---------------------------------------------------------------------------

def diff_specs(
    a: dict[str, Any],
    b: dict[str, Any],
    path: str = "",
    *,
    ignore_keys: frozenset[str] | None = None,
) -> list[SpecChange]:
    """Recursively diff two ``RenderableSpec`` dicts.

    Both *a* and *b* must be plain JSON-compatible dicts (e.g. produced by
    ``spec.to_dict()``).  The function walks the full tree, comparing every
    leaf value and recursing into nested dicts and list elements.

    Args:
        a: The "before" spec dict.
        b: The "after" spec dict.
        path: Dot-separated key path prefix used when recursing.  Callers
            should leave this at its default ``""`` unless they intentionally
            want to scope the diff to a subtree.
        ignore_keys: Optional set of top-level-only key names to skip when
            comparing both dicts at the *current* level.  Useful to exclude
            ``spec_type`` from change detection when comparing heterogeneous
            collections.

    Returns:
        A list of :class:`SpecChange` objects, one per changed value.  The
        list is empty when *a* and *b* are structurally identical.

    Example::

        >>> from termforge.core.diff import diff_specs
        >>> diff_specs({"x": 1, "y": 2}, {"x": 1, "y": 3})
        [SpecChange(path='y', kind='modified', old=2, new=3)]

        >>> diff_specs({"a": {"b": 1}}, {"a": {"b": 2}})
        [SpecChange(path='a.b', kind='modified', old=1, new=2)]
    """
    _ignore = ignore_keys or frozenset()
    changes: list[SpecChange] = []

    all_keys = set(a) | set(b)
    for key in sorted(all_keys):
        if key in _ignore:
            continue

        child_path = f"{path}.{key}" if path else key
        in_a = key in a
        in_b = key in b

        if in_a and not in_b:
            changes.append(SpecChange(
                path=child_path,
                kind=ChangeKind.REMOVED,
                old=a[key],
                new=None,
            ))
        elif in_b and not in_a:
            changes.append(SpecChange(
                path=child_path,
                kind=ChangeKind.ADDED,
                old=None,
                new=b[key],
            ))
        else:
            # Both present — compare
            va, vb = a[key], b[key]
            changes.extend(_compare_values(va, vb, child_path))

    return changes


def _compare_values(
    va: Any,
    vb: Any,
    path: str,
) -> list[SpecChange]:
    """Compare two leaf or nested values at *path*."""
    if type(va) != type(vb):
        # Type mismatch — treat as modification without recursion
        return [SpecChange(path=path, kind=ChangeKind.MODIFIED, old=va, new=vb)]

    if isinstance(va, dict) and isinstance(vb, dict):
        return diff_specs(va, vb, path)

    if isinstance(va, list) and isinstance(vb, list):
        return _diff_lists(va, vb, path)

    if va != vb:
        return [SpecChange(path=path, kind=ChangeKind.MODIFIED, old=va, new=vb)]

    return []


def _diff_lists(
    la: list[Any],
    lb: list[Any],
    path: str,
) -> list[SpecChange]:
    """Diff two lists positionally (index-aligned, not LCS-based).

    Items beyond the shorter list are reported as ADDED or REMOVED.
    This is intentionally simple: TermForge specs rarely reorder children;
    if needed, callers can pre-align lists themselves before diffing.
    """
    changes: list[SpecChange] = []
    max_len = max(len(la), len(lb))
    for i in range(max_len):
        item_path = f"{path}.{i}"
        in_a = i < len(la)
        in_b = i < len(lb)
        if in_a and not in_b:
            changes.append(SpecChange(
                path=item_path,
                kind=ChangeKind.REMOVED,
                old=la[i],
                new=None,
            ))
        elif in_b and not in_a:
            changes.append(SpecChange(
                path=item_path,
                kind=ChangeKind.ADDED,
                old=None,
                new=lb[i],
            ))
        else:
            changes.extend(_compare_values(la[i], lb[i], item_path))
    return changes


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------

def has_changed(
    a: dict[str, Any],
    b: dict[str, Any],
    *,
    ignore_keys: frozenset[str] | None = None,
) -> bool:
    """Return ``True`` if *a* and *b* differ in any field.

    Equivalent to ``bool(diff_specs(a, b, ignore_keys=ignore_keys))`` but
    short-circuits on the first change found.

    Args:
        a: The "before" spec dict.
        b: The "after" spec dict.
        ignore_keys: Keys to skip during comparison.

    Returns:
        ``True`` if any structural difference exists.

    Example::

        >>> has_changed({"x": 1}, {"x": 1})
        False
        >>> has_changed({"x": 1}, {"x": 2})
        True
    """
    return bool(diff_specs(a, b, ignore_keys=ignore_keys))


def filter_changes(
    changes: list[SpecChange],
    *,
    kind: ChangeKind | None = None,
    path_prefix: str | None = None,
) -> list[SpecChange]:
    """Filter a change list by kind and/or path prefix.

    Args:
        changes: List of :class:`SpecChange` objects from :func:`diff_specs`.
        kind: If set, only return changes of this :class:`ChangeKind`.
        path_prefix: If set, only return changes whose ``path`` starts with
            this prefix (e.g. ``"children"`` to see only child changes).

    Returns:
        Filtered list of :class:`SpecChange` objects.

    Example::

        >>> changes = diff_specs(before, after)
        >>> mods = filter_changes(changes, kind=ChangeKind.MODIFIED)
        >>> child_changes = filter_changes(changes, path_prefix="children")
    """
    result = changes
    if kind is not None:
        result = [c for c in result if c.kind == kind]
    if path_prefix is not None:
        result = [c for c in result if c.path.startswith(path_prefix)]
    return result

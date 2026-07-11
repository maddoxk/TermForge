"""TermForge declarative forms — FormSpec and validation engine.

Provides declarative models and validation logic for forms containing text,
checkbox, and textarea inputs.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FieldType(str, Enum):
    """The input type of a form field."""
    TEXT     = "text"
    CHECKBOX = "checkbox"
    TEXTAREA = "textarea"


@dataclass
class FormFieldSpec:
    """A single field specification in a form.

    Attributes:
        name: Internal string key for the field's data value.
        label: User-facing display label for the field.
        field_type: The input component type (TEXT, CHECKBOX, or TEXTAREA).
        placeholder: Optional helper text displayed when empty.
        default_value: Initial value (e.g. False for CHECKBOX, or empty string).
        validation_rules: Dictionary of constraint rules (e.g. required, min_length).
    """
    name: str
    label: str
    field_type: FieldType = FieldType.TEXT
    placeholder: str | None = None
    default_value: Any = None
    validation_rules: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing field properties.
        """
        return {
            "name": self.name,
            "label": self.label,
            "field_type": self.field_type.value,
            "placeholder": self.placeholder,
            "default_value": self.default_value,
            "validation_rules": dict(self.validation_rules),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> FormFieldSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing field properties.

        Returns:
            A new :class:`FormFieldSpec` instance.
        """
        return cls(
            name=d["name"],
            label=d["label"],
            field_type=FieldType(d.get("field_type", "text")),
            placeholder=d.get("placeholder"),
            default_value=d.get("default_value"),
            validation_rules=d.get("validation_rules", {}),
        )


@dataclass
class FormSpec:
    """A complete form specification containing multiple fields and validation.

    Attributes:
        title: Optional form title.
        fields: List of FormFieldSpec instances defining the form fields.
    """
    title: str | None = None
    fields: list[FormFieldSpec] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing form properties.
        """
        return {
            "title": self.title,
            "fields": [f.to_dict() for f in self.fields],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> FormSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing form properties.

        Returns:
            A new :class:`FormSpec` instance.
        """
        return cls(
            title=d.get("title"),
            fields=[FormFieldSpec.from_dict(f) for f in d.get("fields", [])],
        )

    def validate(self, data: dict[str, Any]) -> tuple[bool, dict[str, str]]:
        """Validate form fields against supplied data.

        Applies validation rules such as:
        - ``required``: Checked for existence and non-empty/non-None status.
        - ``min_length``: Checks minimum character length of string values.
        - ``max_length``: Checks maximum character length of string values.
        - ``regex``: Validates string matches a regular expression pattern.
        - ``numeric``: Checks if value can be converted to/is a float/int.
        - ``choices``: Validates value is one of the allowed options.

        Args:
            data: Dictionary of field names and their current input values.

        Returns:
            A ``(is_valid, errors)`` tuple, where ``errors`` maps field names
            to validation error messages.
        """
        errors: dict[str, str] = {}

        for f in self.fields:
            val = data.get(f.name)
            rules = f.validation_rules

            # 1. required check
            is_required = rules.get("required", False)
            if is_required:
                if val is None or (isinstance(val, str) and not val.strip()):
                    errors[f.name] = f"{f.label} is required."
                    continue

            # Skip remaining validation if field is empty and not required
            if val is None or (isinstance(val, str) and not val.strip()):
                continue

            # 2. choices check
            choices = rules.get("choices")
            if choices is not None:
                if val not in choices:
                    errors[f.name] = f"{f.label} must be one of: {', '.join(map(str, choices))}."
                    continue

            # 3. numeric check
            is_numeric = rules.get("numeric", False)
            if is_numeric:
                try:
                    float(val)
                except (ValueError, TypeError):
                    errors[f.name] = f"{f.label} must be numeric."
                    continue

            # String validations (min_length, max_length, regex)
            if isinstance(val, str):
                # 4. min_length check
                min_len = rules.get("min_length")
                if min_len is not None and len(val) < int(min_len):
                    errors[f.name] = f"{f.label} must be at least {min_len} characters."
                    continue

                # 5. max_length check
                max_len = rules.get("max_length")
                if max_len is not None and len(val) > int(max_len):
                    errors[f.name] = f"{f.label} must be at most {max_len} characters."
                    continue

                # 6. regex check
                pattern = rules.get("regex")
                if pattern is not None:
                    try:
                        if not re.search(pattern, val):
                            errors[f.name] = f"{f.label} format is invalid."
                            continue
                    except re.error:
                        # Faulty regex config -> fallback pass
                        pass

        return len(errors) == 0, errors

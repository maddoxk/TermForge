"""Story: config/form_demo — showcase declarative FormSpec and validation.

Demonstrates form field definitions, applying constraints, executing
validation checks, and JSON roundtrip portability.
"""
from __future__ import annotations
import json
from termforge.config.form import FieldType, FormFieldSpec, FormSpec


def main() -> None:
    print("=== TermForge Declarative Forms & Validation Demo ===\n")

    # 1. Define form specification
    form = FormSpec(
        title="Account Setup",
        fields=[
            FormFieldSpec(
                name="username",
                label="Username",
                field_type=FieldType.TEXT,
                placeholder="e.g. johndoe",
                validation_rules={"required": True, "min_length": 4, "regex": "^[a-z0-9_]+$"}
            ),
            FormFieldSpec(
                name="age",
                label="Age",
                field_type=FieldType.TEXT,
                placeholder="e.g. 21",
                validation_rules={"required": True, "numeric": True}
            ),
            FormFieldSpec(
                name="role",
                label="Role",
                field_type=FieldType.TEXT,
                default_value="developer",
                validation_rules={"required": False, "choices": ["admin", "developer", "guest"]}
            ),
            FormFieldSpec(
                name="newsletter",
                label="Subscribe to newsletter",
                field_type=FieldType.CHECKBOX,
                default_value=True
            )
        ]
    )

    print("--- 1. Form Specification ---")
    print(f"  Title: {form.title}")
    for f in form.fields:
        print(f"  - [{f.field_type.value:8}] {f.name:12} | Label: {f.label:24} | Rules: {f.validation_rules}")
    print()

    # 2. Test valid input
    print("--- 2. Valid Input Test ---")
    valid_data = {
        "username": "dox_user",
        "age": "28",
        "role": "developer",
        "newsletter": True
    }
    is_ok, errs = form.validate(valid_data)
    print(f"  Data: {valid_data}")
    print(f"  Valid? {is_ok}")
    print(f"  Errors: {errs}")
    print()

    # 3. Test invalid input (failing username regex/min_length, age non-numeric, role choice)
    print("--- 3. Invalid Input Test ---")
    invalid_data = {
        "username": "JD",       # too short, has capitals (regex fails)
        "age": "twenty",        # non-numeric
        "role": "manager",      # not in choices
        "newsletter": False
    }
    is_ok, errs = form.validate(invalid_data)
    print(f"  Data: {invalid_data}")
    print(f"  Valid? {is_ok}")
    print("  Validation Errors:")
    for field_name, msg in errs.items():
        print(f"    - {field_name}: {msg}")
    print()

    # 4. Verify Portability
    print("--- 4. Portability / JSON check ---")
    j = json.dumps(form.to_dict())
    print(f"  JSON length: {len(j)} bytes")
    restored = FormSpec.from_dict(json.loads(j))
    print(f"  Restored Title: {restored.title}")
    print(f"  Restored field count: {len(restored.fields)}")
    print("  Portability: OK")


if __name__ == "__main__":
    main()

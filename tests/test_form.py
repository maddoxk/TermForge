"""Tests for Issue #154: Declarative Forms & Validation."""
import json
import pytest
from termforge.config.form import FieldType, FormFieldSpec, FormSpec


def test_form_field_spec_to_dict():
    f = FormFieldSpec(
        name="age",
        label="Your Age",
        field_type=FieldType.TEXT,
        placeholder="e.g. 25",
        default_value=18,
        validation_rules={"required": True, "numeric": True}
    )
    d = f.to_dict()
    assert d == {
        "name": "age",
        "label": "Your Age",
        "field_type": "text",
        "placeholder": "e.g. 25",
        "default_value": 18,
        "validation_rules": {"required": True, "numeric": True}
    }


def test_form_field_spec_from_dict():
    d = {
        "name": "accept",
        "label": "Terms",
        "field_type": "checkbox",
        "placeholder": None,
        "default_value": False,
        "validation_rules": {"required": True}
    }
    f = FormFieldSpec.from_dict(d)
    assert f.name == "accept"
    assert f.field_type == FieldType.CHECKBOX
    assert f.validation_rules == {"required": True}


def test_form_spec_roundtrip():
    form = FormSpec(
        title="Settings",
        fields=[
            FormFieldSpec("username", "User"),
            FormFieldSpec("password", "Pass")
        ]
    )
    d = form.to_dict()
    j = json.dumps(d)
    restored = FormSpec.from_dict(json.loads(j))
    assert restored.title == "Settings"
    assert len(restored.fields) == 2
    assert restored.fields[0].name == "username"
    assert restored.fields[1].name == "password"


def test_validation_required():
    form = FormSpec(fields=[FormFieldSpec("name", "Name", validation_rules={"required": True})])
    
    # Valid
    ok, errs = form.validate({"name": "dox"})
    assert ok
    assert not errs

    # Invalid (missing)
    ok, errs = form.validate({})
    assert not ok
    assert "name" in errs
    assert errs["name"] == "Name is required."

    # Invalid (empty string)
    ok, errs = form.validate({"name": "   "})
    assert not ok
    assert "name" in errs


def test_validation_choices():
    form = FormSpec(fields=[
        FormFieldSpec("color", "Color", validation_rules={"choices": ["red", "blue"]})
    ])

    # Valid
    ok, errs = form.validate({"color": "red"})
    assert ok

    # Invalid
    ok, errs = form.validate({"color": "green"})
    assert not ok
    assert "color" in errs
    assert errs["color"] == "Color must be one of: red, blue."


def test_validation_numeric():
    form = FormSpec(fields=[
        FormFieldSpec("qty", "Quantity", validation_rules={"numeric": True})
    ])

    # Valid (int)
    assert form.validate({"qty": 10})[0]
    # Valid (float)
    assert form.validate({"qty": "4.5"})[0]

    # Invalid
    ok, errs = form.validate({"qty": "ten"})
    assert not ok
    assert "qty" in errs
    assert errs["qty"] == "Quantity must be numeric."


def test_validation_string_constraints():
    form = FormSpec(fields=[
        FormFieldSpec("code", "Code", validation_rules={
            "min_length": 3,
            "max_length": 5,
            "regex": "^[A-Z]+$"
        })
    ])

    # Valid
    assert form.validate({"code": "ABC"})[0]
    assert form.validate({"code": "XYZAB"})[0]

    # Invalid min_length
    ok, errs = form.validate({"code": "AB"})
    assert not ok
    assert "code" in errs
    assert "at least 3 characters" in errs["code"]

    # Invalid max_length
    ok, errs = form.validate({"code": "ABCDEF"})
    assert not ok
    assert "code" in errs
    assert "at most 5 characters" in errs["code"]

    # Invalid regex
    ok, errs = form.validate({"code": "abc"})
    assert not ok
    assert "code" in errs
    assert "format is invalid" in errs["code"]


def test_validation_optional_skip():
    # If not required and missing/empty, validation checks (like numeric, min_length) should be skipped
    form = FormSpec(fields=[
        FormFieldSpec("age", "Age", validation_rules={"numeric": True, "required": False})
    ])
    assert form.validate({})[0]
    assert form.validate({"age": ""})[0]
    assert form.validate({"age": "  "})[0]

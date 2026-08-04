from __future__ import annotations

import re
from dataclasses import dataclass, field
from keyword import iskeyword
from typing import Any


@dataclass(slots=True)
class ClassDef:
    name: str
    fields: list[tuple[str, str]] = field(default_factory=list)
    children: list["ClassDef"] = field(default_factory=list)


def to_pascal(name: str) -> str:
    parts = re.findall(r"[A-Za-z0-9]+", name)
    if not parts:
        return "Generated"

    out = "".join(part[:1].upper() + part[1:] for part in parts)
    if out[0].isdigit():
        out = f"Field{out}"

    return out or "Generated"


def to_identifier(name: str) -> str:
    cleaned = re.sub(r"\W+", "_", name).strip("_")
    if not cleaned:
        cleaned = "field"

    if cleaned[0].isdigit():
        cleaned = f"field_{cleaned}"

    if iskeyword(cleaned):
        cleaned += "_"

    return cleaned


def analyze_module(module_name: str, data: Any) -> ClassDef:
    if isinstance(data, dict):
        return _analyze_dict(to_pascal(module_name), data)

    return _analyze_dict(to_pascal(module_name), {"value": data})


def _analyze_dict(class_name: str, data: dict[str, Any]) -> ClassDef:
    fields: list[tuple[str, str]] = []
    children: list[ClassDef] = []

    for raw_key, value in data.items():
        key = to_identifier(str(raw_key))
        annotation, nested = _infer_value_type(value, class_name, key)
        fields.append((key, annotation))
        children.extend(nested)

    return ClassDef(name=class_name, fields=fields, children=children)


def _infer_value_type(
    value: Any,
    parent_class: str,
    field_name: str,
) -> tuple[str, list[ClassDef]]:
    if value is None:
        return "Any", []

    if isinstance(value, bool):
        return "bool", []

    if isinstance(value, int):
        return "int", []

    if isinstance(value, float):
        return "float", []

    if isinstance(value, str):
        return "str", []

    if isinstance(value, dict):
        child_name = f"{parent_class}{to_pascal(field_name)}"
        child_def = _analyze_dict(child_name, value)
        return child_def.name, [child_def]

    if isinstance(value, list):
        return _infer_list_type(value, parent_class, field_name)

    return "Any", []


def _infer_list_type(
    values: list[Any],
    parent_class: str,
    field_name: str,
) -> tuple[str, list[ClassDef]]:
    if not values:
        return "list[Any]", []

    filtered = [v for v in values if v is not None]
    if not filtered:
        return "list[Any]", []

    first = filtered[0]

    if all(isinstance(v, dict) for v in filtered):
        child_name = f"{parent_class}{to_pascal(field_name)}Item"
        child_def = _analyze_dict(child_name, first)
        return f"list[{child_def.name}]", [child_def]

    if all(type(v) is type(first) for v in filtered):
        scalar_type, _ = _infer_value_type(first, parent_class, field_name)
        return f"list[{scalar_type}]", []

    return "list[Any]", []


def flatten_classes(root: ClassDef) -> list[ClassDef]:
    out: list[ClassDef] = []

    for child in root.children:
        out.extend(flatten_classes(child))

    out.append(root)
    return out


def render_stub(root: ClassDef) -> str:
    lines: list[str] = [
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
    ]

    for cls in flatten_classes(root):
        lines.append(f"class {cls.name}:")
        if not cls.fields:
            lines.append("    pass")
        else:
            for field_name, annotation in cls.fields:
                lines.append(f"    {field_name}: {annotation}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"

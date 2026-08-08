"""Deterministic NL → DOQL block planner (no LLM)."""

from __future__ import annotations

import re

from nlp2doql.models import BlockPlan, DoqlPlan

_ENTITY_HINTS = (
    ("contact", "Contact"),
    ("kontakt", "Contact"),
    ("company", "Company"),
    ("firma", "Company"),
    ("deal", "Deal"),
    ("transakc", "Deal"),
    ("todo", "Todo"),
    ("task", "Todo"),
    ("zadani", "Todo"),
    ("user", "User"),
    ("użytkown", "User"),
    ("product", "Product"),
    ("produkt", "Product"),
    ("order", "Order"),
    ("zamówien", "Order"),
)
_CRM_HINTS = ("crm", "sales", "sprzeda", "pipeline", "lead")
_TODO_HINTS = ("todo", "task", "zadani", "checklist", "pwa")
_API_HINTS = ("api", "rest", "backend", "fastapi")
_WEB_HINTS = ("web", "spa", "frontend", "react", "ui", "interfejs")
_CLI_HINTS = ("cli", "shell", "terminal", "command")
_WORKFLOW_HINTS = ("install", "test", "build", "deploy", "quality", "ci")


def _contains_any(text: str, hints: tuple[str, ...]) -> bool:
    return any(h in text for h in hints)


def _extract_app_name(prompt: str) -> str:
    quoted = re.search(r'"([^"]+)"|\'([^\']+)\'', prompt)
    if quoted:
        return quoted.group(1) or quoted.group(2) or "Generated App"
    if _contains_any(prompt, _CRM_HINTS):
        return "CRM App"
    if _contains_any(prompt, _TODO_HINTS):
        return "Todo App"
    return "Generated App"


def _entity_block(name: str, *, fields: list[tuple[str, str]] | None = None) -> BlockPlan:
    props: dict[str, str] = {
        "id": "uuid! auto",
        "created": "datetime auto",
        "updated": "datetime auto",
    }
    for field_name, field_type in fields or []:
        props[field_name] = field_type
    return BlockPlan(
        selector=f'entity[name="{name}"]',
        properties=props,
        comment=f"entity {name}",
    )


def _default_entities(prompt: str) -> list[BlockPlan]:
    lowered = prompt.lower()
    blocks: list[BlockPlan] = []
    seen: set[str] = set()

    for hint, name in _ENTITY_HINTS:
        if hint in lowered and name not in seen:
            seen.add(name)
            if name == "Contact":
                blocks.append(
                    _entity_block(
                        name,
                        fields=[
                            ("first_name", "string!"),
                            ("last_name", "string!"),
                            ("email", "string unique"),
                        ],
                    ),
                )
            elif name == "Company":
                blocks.append(_entity_block(name, fields=[("name", "string! unique")]))
            elif name == "Deal":
                blocks.append(
                    _entity_block(
                        name,
                        fields=[
                            ("title", "string!"),
                            ("value", "decimal"),
                            ("stage", "enum[lead, won, lost] default=lead"),
                        ],
                    ),
                )
            elif name == "Todo":
                blocks.append(
                    _entity_block(
                        name,
                        fields=[
                            ("title", "string!"),
                            ("done", "bool default=false"),
                        ],
                    ),
                )
            else:
                blocks.append(_entity_block(name, fields=[("name", "string!")]))

    if _contains_any(lowered, _CRM_HINTS) and "Contact" not in seen:
        blocks.append(
            _entity_block(
                "Contact",
                fields=[
                    ("first_name", "string!"),
                    ("last_name", "string!"),
                    ("email", "string unique"),
                ],
            ),
        )
    if _contains_any(lowered, _TODO_HINTS) and "Todo" not in seen:
        blocks.append(
            _entity_block(
                "Todo",
                fields=[
                    ("title", "string!"),
                    ("done", "bool default=false"),
                ],
            ),
        )
    if not blocks:
        blocks.append(_entity_block("Item", fields=[("name", "string!"), ("value", "string")]))
    return blocks


def _interface_blocks(prompt: str) -> list[BlockPlan]:
    lowered = prompt.lower()
    blocks: list[BlockPlan] = []
    if _contains_any(lowered, _API_HINTS) or _contains_any(lowered, _CRM_HINTS):
        blocks.append(
            BlockPlan(
                selector='interface[type="api"]',
                properties={"type": "rest", "framework": "fastapi"},
                comment="REST API interface",
            ),
        )
    if _contains_any(lowered, _WEB_HINTS) or _contains_any(lowered, _TODO_HINTS):
        blocks.append(
            BlockPlan(
                selector='interface[type="web"]',
                properties={"type": "spa", "framework": "react"},
                comment="Web SPA interface",
            ),
        )
    if _contains_any(lowered, _CLI_HINTS):
        blocks.append(
            BlockPlan(
                selector='interface[type="cli"]',
                properties={"framework": "click"},
                comment="CLI interface",
            ),
        )
    if not blocks:
        blocks.append(
            BlockPlan(
                selector='interface[type="api"]',
                properties={"type": "rest", "framework": "fastapi"},
            ),
        )
    return blocks


def _workflow_blocks(prompt: str) -> list[BlockPlan]:
    lowered = prompt.lower()
    blocks: list[BlockPlan] = []
    if _contains_any(lowered, _WORKFLOW_HINTS) or "workflow" in lowered:
        blocks.append(
            BlockPlan(
                selector='workflow[name="install"]',
                properties={
                    "trigger": "manual",
                    "step-1": "run cmd=pip install -e .[dev]",
                },
            ),
        )
        blocks.append(
            BlockPlan(
                selector='workflow[name="test"]',
                properties={"trigger": "manual", "step-1": "run cmd=pytest -q"},
            ),
        )
    return blocks


def plan_with_rules(prompt: str) -> DoqlPlan:
    """Map NL prompt to DOQL blocks using keyword rules."""
    text = prompt.strip()
    lowered = text.lower()
    app_name = _extract_app_name(text)

    blocks: list[BlockPlan] = [
        BlockPlan(
            selector="app",
            properties={"name": f'"{app_name}"', "version": '"0.1.0"'},
            comment="application metadata",
        ),
    ]
    blocks.extend(_default_entities(lowered))
    blocks.extend(_interface_blocks(lowered))
    blocks.extend(_workflow_blocks(lowered))
    blocks.append(
        BlockPlan(
            selector="deploy",
            properties={"target": "docker"},
            comment="deployment target",
        ),
    )

    title = text[:80] if len(text) <= 80 else text[:77] + "..."
    return DoqlPlan(
        title=title,
        blocks=blocks,
        planner="rules",
        confidence=0.72 if len(blocks) > 3 else 0.55,
        rationale="keyword rules for entities, interfaces, workflows",
    )

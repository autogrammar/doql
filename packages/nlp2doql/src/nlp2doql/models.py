"""Data models for NL → DOQL planning."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BlockPlan:
    """Single DOQL CSS-like block to render."""

    selector: str
    properties: dict[str, str] = field(default_factory=dict)
    comment: str = ""

    def render(self) -> str:
        lines: list[str] = []
        if self.comment:
            lines.append(f"// {self.comment}")
        lines.append(f"{self.selector} {{")
        for key, value in self.properties.items():
            lines.append(f"  {key}: {value};")
        lines.append("}")
        return "\n".join(lines)


@dataclass
class DoqlPlan:
    """Ordered DOQL blocks with planning metadata."""

    title: str
    blocks: list[BlockPlan] = field(default_factory=list)
    planner: str = "rules"
    confidence: float = 0.0
    rationale: str = ""
    contract_version: str = "1.0.0"

    def to_doql_less(self) -> str:
        header = f"// SCENARIO: {self.title}\n// PLANNER: {self.planner}\n"
        if self.rationale:
            header += f"// RATIONALE: {self.rationale}\n"
        body = "\n\n".join(block.render() for block in self.blocks)
        return f"{header}\n{body}\n"


@dataclass
class GenerateResult:
    ok: bool
    doql: str
    plan: DoqlPlan
    validation: dict[str, Any] | None = None
    output_path: str | None = None
    error: str | None = None

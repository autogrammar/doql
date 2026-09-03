"""nlp2doql — Natural language → DOQL (.doql.less) specifications."""

from nlp2doql.apply import ApplyResult, apply_nl, edit_nl
from nlp2doql.models import BlockPlan, DoqlPlan, GenerateResult
from nlp2doql.pipeline import generate_spec

__version__ = "1.0.44"
__all__ = [
    "ApplyResult",
    "BlockPlan",
    "DoqlPlan",
    "GenerateResult",
    "apply_nl",
    "edit_nl",
    "generate_spec",
    "__version__",
]

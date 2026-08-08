"""CSS block to DoqlSpec mappers.

Maps parsed CSS blocks to the DoqlSpec model structure.
Each mapper handles a specific selector type (entity, interface, etc.)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import DoqlSpec
    from ..css_utils import CssBlock, ParsedSelector

from .entity import (
    _map_entity,
    _parse_type_flags,
    _add_entity_field,
    _parse_type_modifiers,
    _map_data_source,
)
from .config import (
    _map_config_block,
    _map_template,
    _map_document,
    _map_report,
    _map_dependencies,
)
from .interface import (
    _find_or_create_interface,
    _handle_interface_chain,
    _apply_interface_properties,
    _apply_nested_interface_children,
    _map_interface,
    _add_interface_page,
)
from .workflow import (
    _parse_step_text,
    _append_inline_steps,
    _append_child_steps,
    _map_workflow,
    _map_role,
)
from .infra import (
    _map_deploy,
    _map_database,
    _map_environment,
    _map_infrastructure,
    _map_ingress,
    _map_ci,
)
from .integration import _map_integration
from .digital_twin import _map_digital_twin
from .site import _map_site

__all__ = [
    "_add_entity_field",
    "_add_interface_page",
    "_append_child_steps",
    "_append_inline_steps",
    "_apply_interface_properties",
    "_apply_nested_interface_children",
    "_find_or_create_interface",
    "_handle_interface_chain",
    "_map_ci",
    "_map_config_block",
    "_map_data_source",
    "_map_database",
    "_map_deploy",
    "_map_dependencies",
    "_map_digital_twin",
    "_map_document",
    "_map_entity",
    "_map_environment",
    "_map_infrastructure",
    "_map_ingress",
    "_map_integration",
    "_map_interface",
    "_map_project",
    "_map_report",
    "_map_role",
    "_map_site",
    "_map_template",
    "_map_workflow",
    "_parse_step_text",
    "_parse_type_flags",
    "_parse_type_modifiers",
]


def _map_project(spec: "DoqlSpec", sel: "ParsedSelector", block: "CssBlock") -> None:
    """Map nested CSS project block to Subproject.

    Children blocks (app, interface, workflow, deploy, etc.) are parsed
    into a fresh DoqlSpec attached to the Subproject.
    """
    from ..models import Subproject, DoqlSpec
    from ..css_utils import _parse_selector

    sub_spec = DoqlSpec()
    # Dispatch children to the same mappers used by _apply_css_block
    child_route = {
        'entity': _map_entity,
        'data': _map_data_source,
        'template': _map_template,
        'document': _map_document,
        'report': _map_report,
        'integration': _map_integration,
        'workflow': _map_workflow,
        'dependencies': _map_dependencies,
        'role': _map_role,
        'deploy': _map_deploy,
        'database': _map_database,
        'environment': _map_environment,
        'infrastructure': _map_infrastructure,
        'ingress': _map_ingress,
        'ci': _map_ci,
        'interface': _map_interface,
    }

    for child in block.children:
        child_sel = _parse_selector(child.selector)
        t = child_sel.type
        if t == 'app':
            sub_spec.app_name = child.declarations.get('name', sub_spec.app_name)
            sub_spec.version = child.declarations.get('version', sub_spec.version)
            sub_spec.description = child.declarations.get('description')
            sub_spec.license = child.declarations.get('license')
        elif t in child_route:
            child_route[t](sub_spec, child_sel, child)
        elif t == 'project':
            # Nested project (depth > 1) — skip to avoid infinite recursion
            continue

    name = sel.attributes.get('name', '')
    path = sel.attributes.get('path', '')
    spec.subprojects.append(Subproject(name=name, spec=sub_spec, path=path))

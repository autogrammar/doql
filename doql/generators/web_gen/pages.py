"""Page components generation (Dashboard, Entity CRUD pages)."""
from __future__ import annotations

import json
import re
import textwrap
from typing import TYPE_CHECKING

from .common import _kebab

if TYPE_CHECKING:
    from ...parsers import DoqlSpec, Entity, EntityField


_TS_IDENTIFIER = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")


def _property_key(name: str) -> str:
    return name if _TS_IDENTIFIER.fullmatch(name) else json.dumps(name)


def _property_access(owner: str, name: str) -> str:
    if _TS_IDENTIFIER.fullmatch(name):
        return f"{owner}.{name}"
    return f"{owner}[{json.dumps(name)}]"


def _object_update_key(name: str) -> str:
    return name if _TS_IDENTIFIER.fullmatch(name) else f"[{json.dumps(name)}]"


def _gen_dashboard(spec: DoqlSpec) -> str:
    """Generate Dashboard.tsx with entity count cards."""
    cards = []
    for ent in spec.entities:
        slug = _kebab(ent.name) + "s"
        cards.append(textwrap.dedent(f"""\
              <Link to="/{slug}" className="block p-6 bg-white rounded-xl border hover:shadow-md transition-shadow">
                <h3 className="text-sm text-gray-500">{ent.name}s</h3>
                <p className="text-2xl font-bold mt-1">{{counts['{slug}'] ?? '…'}}</p>
              </Link>"""))
    cards_block = "\n".join(cards)

    fetch_lines = []
    for ent in spec.entities:
        slug = _kebab(ent.name) + "s"
        fetch_lines.append(f"      api.list('{slug}').then((d: any[]) => setCounts(c => ({{...c, '{slug}': d.length}})));")
    fetch_block = "\n".join(fetch_lines)

    return textwrap.dedent(f"""\
        import React from 'react';
        import {{ Link }} from 'react-router-dom';
        import {{ api }} from '../api';

        export default function Dashboard() {{
          const [counts, setCounts] = React.useState<Record<string, number>>({{}}); 

          React.useEffect(() => {{
        {fetch_block}
          }}, []);

          return (
            <div>
              <h1 className="text-2xl font-bold mb-6">{spec.app_name}</h1>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards_block}
              </div>
            </div>
          );
        }}
    """)


def _field_input(f: EntityField) -> str:
    """Generate form input for an entity field."""
    if f.auto or f.computed:
        return ""
    input_type = "text"
    if f.type in ("int", "float"):
        input_type = "number"
    if f.type == "date":
        input_type = "date"
    if f.type == "datetime":
        input_type = "datetime-local"
    field_access = _property_access("form", f.name)
    update_key = _object_update_key(f.name)
    if f.type == "bool":
        return (
            f'          <label className="flex items-center gap-2">'
            f'<input type="checkbox" name="{f.name}" checked={{!!{field_access}}} '
            f'onChange={{e => setForm({{...form, {update_key}: e.target.checked}})}} />'
            f' {f.name}</label>'
        )
    return (
        f'          <input name="{f.name}" placeholder="{f.name}" type="{input_type}" '
        f'value={{{field_access} || ""}} '
        f'onChange={{e => setForm({{...form, {update_key}: e.target.value}})}} '
        f'className="border rounded px-3 py-2 text-sm" />'
    )


def _build_interface_body(visible_fields: list[EntityField]) -> str:
    """Return TypeScript interface field list, ensuring `id` is always present."""
    fields = []
    if not any(f.name == "id" for f in visible_fields):
        fields.append("id: any")
    fields.extend(f"{_property_key(f.name)}: any" for f in visible_fields)
    return "; ".join(fields)


def _gen_entity_page(ent: Entity) -> str:
    """Generate CRUD page for an entity."""
    slug = _kebab(ent.name) + "s"
    visible_fields = [f for f in ent.fields if not f.computed]
    form_fields = [f for f in ent.fields if not f.auto and not f.computed]
    headers = " ".join(f'<th className="text-left p-2 text-xs text-gray-500 uppercase">{f.name}</th>' for f in visible_fields[:8])
    cells = " ".join(
        f'<td className="p-2 text-sm">{{String({_property_access("item", f.name)} ?? "")}}</td>'
        for f in visible_fields[:8]
    )
    form_init = ", ".join(f"{_property_key(f.name)}: ''" for f in form_fields)
    inputs = "\n".join(filter(None, (_field_input(f) for f in form_fields)))
    interface_body = _build_interface_body(visible_fields)

    return textwrap.dedent(f"""\
        import React from 'react';
        import {{ api }} from '../api';

        interface {ent.name} {{
          {interface_body};
        }}

        export default function {ent.name}Page() {{
          const [items, setItems] = React.useState<{ent.name}[]>([]);
          const [showForm, setShowForm] = React.useState(false);
          const [form, setForm] = React.useState<any>({{ {form_init} }});

          const load = () => api.list<{ent.name}>('{slug}').then(setItems).catch(console.error);
          React.useEffect(() => {{ load(); }}, []);

          const handleSubmit = async (e: React.FormEvent) => {{
            e.preventDefault();
            await api.create('{slug}', form);
            setForm({{ {form_init} }});
            setShowForm(false);
            load();
          }};

          const handleDelete = async (id: string) => {{
            if (!confirm('Delete?')) return;
            await api.remove('{slug}', id);
            load();
          }};

          return (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h1 className="text-2xl font-bold">{ent.name}s</h1>
                <button onClick={{() => setShowForm(!showForm)}} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">
                  {{showForm ? 'Cancel' : '+ New'}}
                </button>
              </div>

              {{showForm && (
                <form onSubmit={{handleSubmit}} className="mb-6 p-4 bg-white rounded-xl border space-y-3">
        {inputs}
                  <button type="submit" className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm">Save</button>
                </form>
              )}}

              <div className="bg-white rounded-xl border overflow-x-auto">
                <table className="w-full">
                  <thead className="border-b"><tr>{headers}<th></th></tr></thead>
                  <tbody>
                    {{items.map((item) => (
                      <tr key={{item.id}} className="border-b last:border-0 hover:bg-gray-50">
                        {cells}
                        <td className="p-2">
                          <button onClick={{() => handleDelete(item.id)}} className="text-red-500 text-xs hover:underline">Delete</button>
                        </td>
                      </tr>
                    ))}}
                    {{items.length === 0 && <tr><td colSpan={{99}} className="p-8 text-center text-gray-400">No items yet</td></tr>}}
                  </tbody>
                </table>
              </div>
            </div>
          );
        }}
    """)

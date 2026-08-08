import React from 'react';
import { api } from '../api';

interface Device {
  id: any; serial: any; model: any; manufacturer: any; device_type: any; station: any; purchase_date: any; warranty_until: any; photo: any; barcode: any; status: any; last_inspection: any; total_uses: any; formula: any; "when-device_type": any; result: any; when: any; indexes: any;
}

export default function DevicePage() {
  const [items, setItems] = React.useState<Device[]>([]);
  const [showForm, setShowForm] = React.useState(false);
  const [form, setForm] = React.useState<any>({ serial: '', model: '', manufacturer: '', device_type: '', station: '', purchase_date: '', warranty_until: '', photo: '', barcode: '', status: '', last_inspection: '', total_uses: '', formula: '', "when-device_type": '', result: '', when: '', indexes: '' });

  const load = () => api.list<Device>('devices').then(setItems).catch(console.error);
  React.useEffect(() => { load(); }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.create('devices', form);
    setForm({ serial: '', model: '', manufacturer: '', device_type: '', station: '', purchase_date: '', warranty_until: '', photo: '', barcode: '', status: '', last_inspection: '', total_uses: '', formula: '', "when-device_type": '', result: '', when: '', indexes: '' });
    setShowForm(false);
    load();
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Delete?')) return;
    await api.remove('devices', id);
    load();
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">Devices</h1>
        <button onClick={() => setShowForm(!showForm)} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">
          {showForm ? 'Cancel' : '+ New'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="mb-6 p-4 bg-white rounded-xl border space-y-3">
          <input name="serial" placeholder="serial" type="text" value={form.serial || ""} onChange={e => setForm({...form, serial: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="model" placeholder="model" type="text" value={form.model || ""} onChange={e => setForm({...form, model: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="manufacturer" placeholder="manufacturer" type="text" value={form.manufacturer || ""} onChange={e => setForm({...form, manufacturer: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="device_type" placeholder="device_type" type="text" value={form.device_type || ""} onChange={e => setForm({...form, device_type: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="station" placeholder="station" type="text" value={form.station || ""} onChange={e => setForm({...form, station: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="purchase_date" placeholder="purchase_date" type="date" value={form.purchase_date || ""} onChange={e => setForm({...form, purchase_date: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="warranty_until" placeholder="warranty_until" type="date" value={form.warranty_until || ""} onChange={e => setForm({...form, warranty_until: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="photo" placeholder="photo" type="text" value={form.photo || ""} onChange={e => setForm({...form, photo: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="barcode" placeholder="barcode" type="text" value={form.barcode || ""} onChange={e => setForm({...form, barcode: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="status" placeholder="status" type="text" value={form.status || ""} onChange={e => setForm({...form, status: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="last_inspection" placeholder="last_inspection" type="date" value={form.last_inspection || ""} onChange={e => setForm({...form, last_inspection: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="total_uses" placeholder="total_uses" type="number" value={form.total_uses || ""} onChange={e => setForm({...form, total_uses: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="formula" placeholder="formula" type="text" value={form.formula || ""} onChange={e => setForm({...form, formula: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="when-device_type" placeholder="when-device_type" type="text" value={form["when-device_type"] || ""} onChange={e => setForm({...form, ["when-device_type"]: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="result" placeholder="result" type="text" value={form.result || ""} onChange={e => setForm({...form, result: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="when" placeholder="when" type="text" value={form.when || ""} onChange={e => setForm({...form, when: e.target.value})} className="border rounded px-3 py-2 text-sm" />
  <input name="indexes" placeholder="indexes" type="text" value={form.indexes || ""} onChange={e => setForm({...form, indexes: e.target.value})} className="border rounded px-3 py-2 text-sm" />
          <button type="submit" className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm">Save</button>
        </form>
      )}

      <div className="bg-white rounded-xl border overflow-x-auto">
        <table className="w-full">
          <thead className="border-b"><tr><th className="text-left p-2 text-xs text-gray-500 uppercase">id</th> <th className="text-left p-2 text-xs text-gray-500 uppercase">serial</th> <th className="text-left p-2 text-xs text-gray-500 uppercase">model</th> <th className="text-left p-2 text-xs text-gray-500 uppercase">manufacturer</th> <th className="text-left p-2 text-xs text-gray-500 uppercase">device_type</th> <th className="text-left p-2 text-xs text-gray-500 uppercase">station</th> <th className="text-left p-2 text-xs text-gray-500 uppercase">purchase_date</th> <th className="text-left p-2 text-xs text-gray-500 uppercase">warranty_until</th><th></th></tr></thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} className="border-b last:border-0 hover:bg-gray-50">
                <td className="p-2 text-sm">{String(item.id ?? "")}</td> <td className="p-2 text-sm">{String(item.serial ?? "")}</td> <td className="p-2 text-sm">{String(item.model ?? "")}</td> <td className="p-2 text-sm">{String(item.manufacturer ?? "")}</td> <td className="p-2 text-sm">{String(item.device_type ?? "")}</td> <td className="p-2 text-sm">{String(item.station ?? "")}</td> <td className="p-2 text-sm">{String(item.purchase_date ?? "")}</td> <td className="p-2 text-sm">{String(item.warranty_until ?? "")}</td>
                <td className="p-2">
                  <button onClick={() => handleDelete(item.id)} className="text-red-500 text-xs hover:underline">Delete</button>
                </td>
              </tr>
            ))}
            {items.length === 0 && <tr><td colSpan={99} className="p-8 text-center text-gray-400">No items yet</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}

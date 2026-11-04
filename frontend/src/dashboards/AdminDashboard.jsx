import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  Users,
  Database,
  Cpu,
  Scale,
  ScanEye,
  Plus,
  Trash2,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Search,
  Activity
} from 'lucide-react';
import { adminService, fertilizerService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [fertilizers, setFertilizers] = useState([]);
  const [activeTab, setActiveTab] = useState('overview'); // overview, users, fertilizers
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  // New fertilizer form state
  const [newFert, setNewFert] = useState({
    name: '',
    brand: '',
    category: 'Nitrogenous',
    pack_size_kg: 50,
    price: 300,
    rating: 4.5,
    nutrient_composition: '',
    description: '',
    is_subsidized: false,
  });
  const [addingFert, setAddingFert] = useState(false);

  const fetchAdminData = async () => {
    setLoading(true);
    setError('');
    try {
      const [statsData, usersData, fertsData] = await Promise.all([
        adminService.getStats(),
        adminService.getUsers(),
        fertilizerService.getAll(),
      ]);
      setStats(statsData);
      setUsers(usersData);
      setFertilizers(fertsData);
    } catch (err) {
      setError(err.message || 'Failed to load administrative control data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
  }, []);

  const handleAddFertilizer = async (e) => {
    e.preventDefault();
    setAddingFert(true);
    setError('');
    setSuccessMsg('');
    try {
      await adminService.addFertilizer(newFert);
      setSuccessMsg(`Successfully added ${newFert.name} to the verified product catalog.`);
      // Refresh list
      const updated = await fertilizerService.getAll();
      setFertilizers(updated);
      setNewFert({
        name: '',
        brand: '',
        category: 'Nitrogenous',
        pack_size_kg: 50,
        price: 300,
        rating: 4.5,
        nutrient_composition: '',
        description: '',
        is_subsidized: false,
      });
    } catch (err) {
      setError('Could not add product: ' + err.message);
    } finally {
      setAddingFert(false);
    }
  };

  const handleDeleteFertilizer = async (id, name) => {
    if (!window.confirm(`Are you sure you want to remove "${name}" from the catalog?`)) {
      return;
    }
    try {
      await adminService.deleteFertilizer(id);
      setFertilizers(fertilizers.filter((f) => f.id !== id));
      setSuccessMsg(`Removed ${name} from catalog.`);
    } catch (err) {
      setError('Could not remove product: ' + err.message);
    }
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 text-emerald-400 text-xs font-bold uppercase tracking-wider border border-slate-700">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Administrative Console</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            System Operations & Governance
          </h1>
          <p className="text-xs text-slate-400">
            Manage registered farmers, agricultural experts, catalog verification, and model infrastructure.
          </p>
        </div>

        <button
          onClick={fetchAdminData}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Metrics</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-200 gap-6 text-sm font-semibold text-slate-500">
        <button
          onClick={() => setActiveTab('overview')}
          className={`pb-3 border-b-2 transition ${
            activeTab === 'overview'
              ? 'border-emerald-600 text-emerald-700'
              : 'border-transparent hover:text-slate-900'
          }`}
        >
          System Overview
        </button>
        <button
          onClick={() => setActiveTab('users')}
          className={`pb-3 border-b-2 transition ${
            activeTab === 'users'
              ? 'border-emerald-600 text-emerald-700'
              : 'border-transparent hover:text-slate-900'
          }`}
        >
          User Accounts ({users.length})
        </button>
        <button
          onClick={() => setActiveTab('fertilizers')}
          className={`pb-3 border-b-2 transition ${
            activeTab === 'fertilizers'
              ? 'border-emerald-600 text-emerald-700'
              : 'border-transparent hover:text-slate-900'
          }`}
        >
          Fertilizer Catalog Management ({fertilizers.length})
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-xs text-red-700 flex items-start gap-2">
          <AlertCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {successMsg && (
        <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-start gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
          <span>{successMsg}</span>
        </div>
      )}

      {loading ? (
        <LoadingSpinner message="Aggregating cluster metrics..." size="lg" />
      ) : activeTab === 'overview' && stats ? (
        <div className="space-y-6">
          {/* Key Metric Counters */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-1">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-xs font-medium">Registered Farmers</span>
                <Users className="w-4 h-4 text-emerald-600" />
              </div>
              <div className="text-2xl font-black text-slate-900 font-mono">
                {stats.total_farmers}
              </div>
              <div className="text-[11px] text-slate-500">Across active states</div>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-1">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-xs font-medium">Extension Experts</span>
                <Users className="w-4 h-4 text-blue-600" />
              </div>
              <div className="text-2xl font-black text-slate-900 font-mono">
                {stats.total_experts}
              </div>
              <div className="text-[11px] text-slate-500">KVK certified agronomists</div>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-1">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-xs font-medium">Disease Leaf Scans</span>
                <ScanEye className="w-4 h-4 text-purple-600" />
              </div>
              <div className="text-2xl font-black text-slate-900 font-mono">
                {stats.total_disease_scans}
              </div>
              <div className="text-[11px] text-slate-500">Total pipeline uploads</div>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-1">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-xs font-medium">Pending Expert Reviews</span>
                <Activity className="w-4 h-4 text-amber-600" />
              </div>
              <div className="text-2xl font-black text-amber-600 font-mono">
                {stats.pending_expert_reviews}
              </div>
              <div className="text-[11px] text-slate-500">Awaiting clinical diagnosis</div>
            </div>
          </div>

          {/* Infrastructure Health Status */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-4">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Database className="w-4 h-4 text-emerald-600" />
                <span>Database Connectivity (MongoDB Atlas)</span>
              </h3>
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                <div>
                  <div className="text-xs font-bold text-slate-800">
                    {stats.database_connected ? 'MongoDB Cluster Online' : 'Local Memory Store Active'}
                  </div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    {stats.database_connected
                      ? 'Connected to Atlas with auto-indexing on users, disease_cases, fertilizers.'
                      : 'Running in development fallback mode. Configure MONGODB_URI in backend/.env for persistent Atlas.'}
                  </div>
                </div>
                <span
                  className={`w-3 h-3 rounded-full ${
                    stats.database_connected ? 'bg-emerald-500' : 'bg-amber-500'
                  }`}
                />
              </div>
            </div>

            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-4">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Cpu className="w-4 h-4 text-emerald-600" />
                <span>AI / Machine Learning Pipelines</span>
              </h3>
              <div className="space-y-2 text-xs">
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                  <span>CNN Disease Detection Model:</span>
                  <span
                    className={`font-bold px-2 py-0.5 rounded-md ${
                      stats.ai_models_status?.cnn_disease_detection
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-amber-100 text-amber-800'
                    }`}
                  >
                    {stats.ai_models_status?.cnn_disease_detection
                      ? 'Weights Loaded'
                      : 'Modular Interface Active (Training Pending)'}
                  </span>
                </div>

                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                  <span>Crop Recommendation Engine:</span>
                  <span
                    className={`font-bold px-2 py-0.5 rounded-md ${
                      stats.ai_models_status?.crop_recommendation_ml
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-emerald-100 text-emerald-800'
                    }`}
                  >
                    Agronomic Extension Rules Active
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : activeTab === 'users' ? (
        <div className="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="p-6 border-b border-slate-100 flex items-center justify-between">
            <h3 className="font-bold text-slate-900 text-base">Registered Users Directory</h3>
            <span className="text-xs text-slate-500">{users.length} accounts total</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 border-b border-slate-100">
                <tr>
                  <th className="p-4">Name</th>
                  <th className="p-4">Email</th>
                  <th className="p-4">Phone</th>
                  <th className="p-4">Role</th>
                  <th className="p-4">Location</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map((u) => (
                  <tr key={u.id || u.email} className="hover:bg-slate-50/50">
                    <td className="p-4 font-bold text-slate-900">{u.full_name}</td>
                    <td className="p-4 text-slate-600">{u.email}</td>
                    <td className="p-4 text-slate-600">{u.phone_number}</td>
                    <td className="p-4">
                      <span
                        className={`px-2 py-0.5 rounded-md font-semibold capitalize ${
                          u.role === 'admin'
                            ? 'bg-purple-100 text-purple-800'
                            : u.role === 'expert'
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-emerald-100 text-emerald-800'
                        }`}
                      >
                        {u.role}
                      </span>
                    </td>
                    <td className="p-4 text-slate-600">
                      {u.village_district}, {u.state}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : activeTab === 'fertilizers' ? (
        <div className="space-y-8">
          {/* Add Fertilizer Form */}
          <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-xs space-y-4">
            <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
              <Plus className="w-5 h-5 text-emerald-600" />
              <span>Add Verified Fertilizer Product to Database</span>
            </h3>

            <form onSubmit={handleAddFertilizer} className="space-y-4 text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Product Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Zinc Sulfate 21%"
                    value={newFert.name}
                    onChange={(e) => setNewFert({ ...newFert, name: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Brand / Manufacturer</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. IFFCO, Tata Chemicals"
                    value={newFert.brand}
                    onChange={(e) => setNewFert({ ...newFert, brand: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Category</label>
                  <select
                    value={newFert.category}
                    onChange={(e) => setNewFert({ ...newFert, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white font-medium"
                  >
                    <option value="Nitrogenous">Nitrogenous</option>
                    <option value="Phosphatic">Phosphatic</option>
                    <option value="Potassic">Potassic</option>
                    <option value="Complex">Complex</option>
                    <option value="Organic">Organic</option>
                    <option value="Bio-Fertilizer">Bio-Fertilizer</option>
                    <option value="Micronutrient">Micronutrient</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Pack Size (kg)</label>
                  <input
                    type="number"
                    step="0.1"
                    required
                    value={newFert.pack_size_kg}
                    onChange={(e) => setNewFert({ ...newFert, pack_size_kg: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Total Pack Price (₹)</label>
                  <input
                    type="number"
                    step="0.5"
                    required
                    value={newFert.price}
                    onChange={(e) => setNewFert({ ...newFert, price: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Initial Rating (1-5)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="1"
                    max="5"
                    value={newFert.rating}
                    onChange={(e) => setNewFert({ ...newFert, rating: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>

                <div className="flex items-center pt-5">
                  <label className="inline-flex items-center gap-2 cursor-pointer font-semibold text-slate-700">
                    <input
                      type="checkbox"
                      checked={newFert.is_subsidized}
                      onChange={(e) => setNewFert({ ...newFert, is_subsidized: e.target.checked })}
                      className="w-4 h-4 text-emerald-600 rounded-sm"
                    />
                    <span>Govt. Subsidized</span>
                  </label>
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Product Description / Notes</label>
                <input
                  type="text"
                  placeholder="Agronomic purpose and instructions..."
                  value={newFert.description}
                  onChange={(e) => setNewFert({ ...newFert, description: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <button
                type="submit"
                disabled={addingFert}
                className="px-6 py-2.5 rounded-xl bg-emerald-600 text-white font-bold hover:bg-emerald-700 transition disabled:opacity-50"
              >
                {addingFert ? 'Saving Product...' : 'Add Product to Catalog'}
              </button>
            </form>
          </div>

          {/* Current Catalog Table */}
          <div className="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex items-center justify-between">
              <h3 className="font-bold text-slate-900 text-base">Current Product Catalog</h3>
              <span className="text-xs text-slate-500">{fertilizers.length} products listed</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-500 border-b border-slate-100">
                  <tr>
                    <th className="p-4">Brand & Name</th>
                    <th className="p-4">Category</th>
                    <th className="p-4">Pack Size</th>
                    <th className="p-4">Price</th>
                    <th className="p-4">Unit Rate</th>
                    <th className="p-4">Rating</th>
                    <th className="p-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {fertilizers.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-50/50">
                      <td className="p-4">
                        <div className="font-bold text-slate-900">{p.name}</div>
                        <div className="text-slate-400 text-[11px]">{p.brand}</div>
                      </td>
                      <td className="p-4 text-slate-600">{p.category}</td>
                      <td className="p-4 text-slate-600">{p.pack_size_kg} kg</td>
                      <td className="p-4 font-bold text-slate-900">₹{p.price}</td>
                      <td className="p-4 font-bold text-emerald-700">₹{p.price_per_kg} / kg</td>
                      <td className="p-4 text-amber-600 font-bold">{p.rating || 'N/A'} ★</td>
                      <td className="p-4 text-right">
                        <button
                          onClick={() => handleDeleteFertilizer(p.id, p.name)}
                          className="p-1.5 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg transition"
                          title="Delete product"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}


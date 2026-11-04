import React, { useState, useEffect } from 'react';
import {
  Scale,
  Search,
  Sliders,
  Star,
  CheckCircle2,
  Info,
  Layers,
  ArrowRight,
  TrendingDown,
  Tag,
  Award
} from 'lucide-react';
import { fertilizerService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function FertilizerComparisonPage() {
  const [products, setProducts] = useState([]);
  const [category, setCategory] = useState('all');
  const [search, setSearch] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [alpha, setAlpha] = useState(0.5); // Weight for price vs rating
  const [comparisonResult, setComparisonResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [comparing, setComparing] = useState(false);
  const [error, setError] = useState('');

  const categories = [
    { key: 'all', label: 'All Fertilizers' },
    { key: 'Nitrogenous', label: 'Nitrogenous (Urea)' },
    { key: 'Phosphatic', label: 'Phosphatic (DAP, SSP)' },
    { key: 'Potassic', label: 'Potassic (MOP)' },
    { key: 'Complex', label: 'Complex (NPK)' },
    { key: 'Organic', label: 'Organic / Compost' },
    { key: 'Bio-Fertilizer', label: 'Bio-Fertilizers' },
    { key: 'Micronutrient', label: 'Micronutrients (Zinc, etc.)' }
  ];

  const fetchProducts = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await fertilizerService.getAll({
        category: category !== 'all' ? category : undefined,
        search: search.trim() || undefined,
      });
      setProducts(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch fertilizer catalog.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, [category]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchProducts();
  };

  const toggleSelect = (id) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter((item) => item !== id));
    } else {
      if (selectedIds.length >= 6) {
        alert('You can compare up to 6 fertilizer products at once.');
        return;
      }
      setSelectedIds([...selectedIds, id]);
    }
  };

  const handleCompare = async () => {
    if (selectedIds.length < 2) {
      setError('Please select at least 2 products to perform mathematical comparison.');
      return;
    }

    setComparing(true);
    setError('');
    try {
      const res = await fertilizerService.compare({
        product_ids: selectedIds,
        alpha: parseFloat(alpha),
      });
      setComparisonResult(res);
    } catch (err) {
      setError(err.message || 'Comparison calculation failed.');
    } finally {
      setComparing(false);
    }
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          <Scale className="w-4 h-4 text-emerald-600" />
          <span>Economic Decision Support</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Fertilizer Price & Quality Comparison
        </h1>
        <p className="text-sm text-slate-600 max-w-2xl leading-relaxed">
          Evaluate fertilizer products with mathematical objectivity. Our normalized scoring algorithm balances actual cost-per-kilogram against verified farmer satisfaction ratings.
        </p>
      </div>

      {/* Comparison Drawer / Toolbar if products selected */}
      {selectedIds.length > 0 && (
        <div className="sticky top-20 z-20 bg-slate-900 text-white p-5 rounded-3xl shadow-xl flex flex-col md:flex-row items-center justify-between gap-4 border border-slate-800">
          <div className="flex items-center gap-3">
            <span className="w-8 h-8 rounded-xl bg-emerald-500 text-slate-950 font-bold flex items-center justify-center text-sm">
              {selectedIds.length}
            </span>
            <div>
              <div className="text-sm font-bold text-white">Fertilizers Selected for Comparison</div>
              <div className="text-xs text-slate-400">
                Adjust preference weighting (Price vs Quality) below
              </div>
            </div>
          </div>

          {/* Alpha Weight Slider */}
          <div className="flex items-center gap-3 bg-slate-800 px-4 py-2 rounded-2xl border border-slate-700 text-xs">
            <span className="text-slate-300 font-medium">Price Weight:</span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={alpha}
              onChange={(e) => setAlpha(parseFloat(e.target.value))}
              className="accent-emerald-500 cursor-pointer w-28"
            />
            <span className="font-mono font-bold text-emerald-400 w-10 text-right">
              {Math.round(alpha * 100)}%
            </span>
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            <button
              onClick={() => setSelectedIds([])}
              className="px-4 py-2 rounded-xl text-xs text-slate-400 hover:text-white transition"
            >
              Clear
            </button>
            <button
              onClick={handleCompare}
              disabled={selectedIds.length < 2 || comparing}
              className="flex-1 md:flex-none inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl bg-emerald-600 text-white font-bold text-xs hover:bg-emerald-700 transition disabled:opacity-50"
            >
              {comparing ? 'Calculating Scores...' : 'Calculate Optimal Rank'}
            </button>
          </div>
        </div>
      )}

      {/* Comparison Result Section if calculated */}
      {comparisonResult && (
        <div className="bg-white rounded-3xl p-6 sm:p-8 border-2 border-emerald-500 shadow-md space-y-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
            <div>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider mb-1">
                <Award className="w-3.5 h-3.5 text-emerald-600" />
                <span>Ranked Results</span>
              </div>
              <h2 className="text-2xl font-bold text-slate-900">
                Mathematical Comparison Ranking
              </h2>
            </div>
            <div className="text-xs text-slate-500 font-mono bg-slate-50 p-2.5 rounded-xl border border-slate-200">
              Formula: {comparisonResult.formula_used} (α = {comparisonResult.alpha_used})
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {comparisonResult.ranked_products?.map((item) => (
              <div
                key={item.product.id}
                className={`rounded-2xl p-6 border transition flex flex-col justify-between ${
                  item.rank === 1
                    ? 'bg-gradient-to-b from-emerald-50/70 to-white border-emerald-400 shadow-md ring-2 ring-emerald-500/20'
                    : 'bg-white border-slate-200'
                }`}
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span
                      className={`w-7 h-7 rounded-lg text-xs font-black flex items-center justify-center ${
                        item.rank === 1
                          ? 'bg-emerald-600 text-white shadow-xs'
                          : 'bg-slate-200 text-slate-700'
                      }`}
                    >
                      #{item.rank}
                    </span>
                    <span className="text-2xl font-black text-emerald-600 font-mono">
                      {item.overall_score}%
                    </span>
                  </div>

                  <div>
                    <div className="text-xs font-semibold text-slate-500">{item.product.brand}</div>
                    <h3 className="text-base font-bold text-slate-900 mt-0.5">
                      {item.product.name}
                    </h3>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs pt-2 border-t border-slate-100">
                    <div>
                      <span className="text-slate-400">Unit Price:</span>
                      <p className="font-bold text-slate-900">₹{item.product.price_per_kg} / kg</p>
                    </div>
                    <div>
                      <span className="text-slate-400">Rating:</span>
                      <p className="font-bold text-amber-600 flex items-center gap-1">
                        <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
                        <span>{item.product.rating || 'Unrated'}</span>
                      </p>
                    </div>
                  </div>

                  <p className="text-xs text-slate-600 bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                    {item.recommendation_note}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500">
                  Total Pack: ₹{item.product.price} ({item.product.pack_size_kg} kg)
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              placeholder="Search by fertilizer name, composition, or brand (e.g. Urea, IFFCO)..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-2.5 rounded-xl bg-slate-900 text-white font-semibold text-xs hover:bg-slate-800 transition"
          >
            Search
          </button>
        </form>

        {/* Category Pill Filters */}
        <div className="flex flex-wrap gap-2 pt-1">
          {categories.map((c) => (
            <button
              key={c.key}
              onClick={() => setCategory(c.key)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition ${
                category === c.key
                  ? 'bg-emerald-600 text-white border-emerald-600 shadow-xs'
                  : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>
      </div>

      {/* Products Grid */}
      {loading ? (
        <LoadingSpinner message="Fetching verified fertilizer catalog..." size="lg" />
      ) : products.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((p) => {
            const isSelected = selectedIds.includes(p.id);
            return (
              <div
                key={p.id}
                onClick={() => toggleSelect(p.id)}
                className={`cursor-pointer rounded-3xl p-6 border transition flex flex-col justify-between ${
                  isSelected
                    ? 'bg-emerald-50/60 border-emerald-500 shadow-sm ring-2 ring-emerald-500/20'
                    : 'bg-white border-slate-200 hover:border-emerald-300 hover:shadow-sm'
                }`}
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                      {p.brand}
                    </span>
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => {}} // handled by card click
                      className="w-4 h-4 text-emerald-600 rounded-sm focus:ring-emerald-500"
                    />
                  </div>

                  <h3 className="text-lg font-bold text-slate-900 leading-snug">{p.name}</h3>

                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-slate-100 text-slate-700 border border-slate-200">
                      {p.category}
                    </span>
                    {p.is_subsidized && (
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-100 text-emerald-800">
                        Govt. Subsidized
                      </span>
                    )}
                  </div>

                  <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">
                    {p.description}
                  </p>
                </div>

                <div className="pt-4 border-t border-slate-100 mt-4 space-y-2">
                  <div className="flex items-baseline justify-between">
                    <div>
                      <span className="text-2xl font-black text-slate-900">₹{p.price}</span>
                      <span className="text-xs text-slate-500 ml-1">/ {p.pack_size_kg} kg bag</span>
                    </div>
                    <div className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-100">
                      ₹{p.price_per_kg} / kg
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <div className="flex items-center gap-1">
                      <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
                      <span className="font-semibold text-slate-800">{p.rating || 'N/A'}</span>
                      <span>({p.rating_count} reviews)</span>
                    </div>
                    <span className="text-[11px] text-emerald-700 font-medium">
                      {isSelected ? '✓ Selected' : '+ Select to compare'}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-white rounded-3xl p-12 text-center text-slate-500 border border-slate-200">
          No fertilizer products matched your query.
        </div>
      )}
    </div>
  );
}


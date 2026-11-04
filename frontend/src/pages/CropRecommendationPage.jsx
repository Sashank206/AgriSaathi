import React, { useState } from 'react';
import {
  Trees,
  MapPin,
  Compass,
  Droplets,
  Calendar,
  CloudSun,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  Info,
  Layers,
  ArrowRight
} from 'lucide-react';
import { cropService, weatherService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function CropRecommendationPage() {
  const [state, setState] = useState('Punjab');
  const [district, setDistrict] = useState('Ludhiana');
  const [village, setVillage] = useState('');
  const [gpsCoords, setGpsCoords] = useState(null);
  const [soilType, setSoilType] = useState('Alluvial Soil');
  const [waterSource, setWaterSource] = useState('Borewell');
  const [season, setSeason] = useState('Rabi (Winter)');
  const [loading, setLoading] = useState(false);
  const [locationDetecting, setLocationDetecting] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const indianStates = [
    'Punjab',
    'Haryana',
    'Uttar Pradesh',
    'Maharashtra',
    'Madhya Pradesh',
    'Gujarat',
    'Rajasthan',
    'Karnataka',
    'Andhra Pradesh',
    'Telangana',
    'Tamil Nadu',
    'West Bengal',
    'Bihar',
    'Kerala'
  ];

  const soilOptions = [
    'Alluvial Soil',
    'Black Soil (Vertisols/Regur)',
    'Red & Yellow Soil',
    'Sandy Loam',
    'Clayey Loam',
    'Laterite Soil',
    'Arid / Desert Soil',
    'Unknown / Let System Detect'
  ];

  const waterSources = [
    'Borewell',
    'Canal irrigation',
    'Rain-fed',
    'Other irrigation source',
    'Unknown'
  ];

  const seasons = [
    'Rabi (Winter)',
    'Kharif (Monsoon)',
    'Zaid (Summer)'
  ];

  const handleDetectLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.');
      return;
    }

    setLocationDetecting(true);
    setError('');

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setGpsCoords({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
        });
        setLocationDetecting(false);
      },
      (err) => {
        setLocationDetecting(false);
        setError('Could not obtain GPS coordinates: ' + err.message + '. You may select your State and District manually.');
      },
      { timeout: 10000 }
    );
  };

  const handleRecommend = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const payload = {
        state,
        district,
        village,
        latitude: gpsCoords?.latitude || null,
        longitude: gpsCoords?.longitude || null,
        soil_type: soilType === 'Unknown / Let System Detect' ? null : soilType,
        water_source: waterSource,
        season,
      };

      const res = await cropService.recommend(payload);
      setResult(res);
    } catch (err) {
      setError(err.message || 'Crop recommendation request failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          <Trees className="w-4 h-4 text-emerald-600" />
          <span>Agro-Climatic Intelligence</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Location-Based Smart Crop Recommendation
        </h1>
        <p className="text-sm text-slate-600 max-w-2xl leading-relaxed">
          Recommends crop sowing candidates using your geographical location, seasonal weather patterns, regional soil series, and practical farm water sources — without requiring complex lab NPK chemical test values.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 flex items-start gap-3 text-xs text-red-700">
          <AlertCircle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
          <div className="flex-1 font-medium">{error}</div>
        </div>
      )}

      {/* Main Form & Results Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Form Column (lg:col-span-5) */}
        <div className="lg:col-span-5 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <MapPin className="w-5 h-5 text-emerald-600" />
              <span>Farm Parameters</span>
            </h2>
            <button
              type="button"
              onClick={handleDetectLocation}
              disabled={locationDetecting}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-semibold hover:bg-emerald-100 transition"
            >
              <Compass className={`w-3.5 h-3.5 ${locationDetecting ? 'animate-spin' : ''}`} />
              <span>{locationDetecting ? 'Detecting...' : 'Detect GPS'}</span>
            </button>
          </div>

          {gpsCoords && (
            <div className="p-3 rounded-xl bg-emerald-50/80 border border-emerald-200 text-xs text-emerald-900 flex items-center justify-between">
              <span>GPS: {gpsCoords.latitude.toFixed(4)}°N, {gpsCoords.longitude.toFixed(4)}°E</span>
              <span className="font-semibold text-emerald-700">Detected</span>
            </div>
          )}

          <form onSubmit={handleRecommend} className="space-y-4">
            {/* State & District */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">State</label>
                <select
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
                >
                  {indianStates.map((st) => (
                    <option key={st} value={st}>
                      {st}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">District</label>
                <input
                  type="text"
                  required
                  value={district}
                  onChange={(e) => setDistrict(e.target.value)}
                  placeholder="e.g. Ludhiana"
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>
            </div>

            {/* Village */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Village (Optional)</label>
              <input
                type="text"
                value={village}
                onChange={(e) => setVillage(e.target.value)}
                placeholder="Village name (if available)"
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            {/* Soil Type */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Soil Type (Supporting input or regional database)
              </label>
              <select
                value={soilType}
                onChange={(e) => setSoilType(e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
              >
                {soilOptions.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>

            {/* Water Source (Part G Requirement: practical choices, not chemical tests) */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Practical Irrigation / Water Availability
              </label>
              <select
                value={waterSource}
                onChange={(e) => setWaterSource(e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
              >
                {waterSources.map((w) => (
                  <option key={w} value={w}>
                    {w}
                  </option>
                ))}
              </select>
            </div>

            {/* Season */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Agricultural Season</label>
              <select
                value={season}
                onChange={(e) => setSeason(e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
              >
                {seasons.map((sn) => (
                  <option key={sn} value={sn}>
                    {sn}
                  </option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-emerald-600 text-white font-bold text-sm hover:bg-emerald-700 transition shadow-sm disabled:opacity-50"
            >
              {loading ? (
                <span>Evaluating Environmental Conditions...</span>
              ) : (
                <>
                  <Trees className="w-4 h-4" />
                  <span>Generate Crop Recommendations</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Results Column (lg:col-span-7) */}
        <div className="lg:col-span-7 space-y-6">
          {!result && !loading && (
            <div className="bg-white rounded-3xl p-8 sm:p-12 border border-slate-200 shadow-sm text-center space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto">
                <Trees className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-bold text-slate-800">Ready to Evaluate Suitability</h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto leading-relaxed">
                Confirm your farm parameters on the left and generate recommendations. Environmental factors like temperature and water sources will be evaluated automatically.
              </p>
            </div>
          )}

          {loading && (
            <div className="bg-white rounded-3xl p-12 border border-slate-200 shadow-sm text-center space-y-4">
              <LoadingSpinner message="Checking ICAR agro-climatic boundaries and weather normals..." size="lg" />
            </div>
          )}

          {result && !loading && (
            <div className="space-y-6">
              {/* Context provenance card */}
              <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-3">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100 text-xs font-bold text-slate-700">
                  <span className="flex items-center gap-1.5">
                    <Layers className="w-4 h-4 text-emerald-600" />
                    <span>Environmental Context</span>
                  </span>
                  <span className="text-emerald-700 font-mono">
                    {result.location?.district}, {result.location?.state}
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="text-slate-400 font-medium">Regional Soil</div>
                    <div className="font-bold text-slate-800 mt-0.5">
                      {result.soil_info?.soil_type || 'Regional Average'}
                    </div>
                    <div className="text-[10px] text-slate-400 italic">
                      Source: {result.soil_info?.source}
                    </div>
                  </div>

                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="text-slate-400 font-medium">Water Availability</div>
                    <div className="font-bold text-slate-800 mt-0.5">{result.water_source}</div>
                    <div className="text-[10px] text-slate-400">Farmer specified</div>
                  </div>

                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="text-slate-400 font-medium">Current Season</div>
                    <div className="font-bold text-slate-800 mt-0.5">
                      {result.weather_info?.season_detected || season}
                    </div>
                    <div className="text-[10px] text-slate-400">
                      Temp: {result.weather_info?.temperature}°C
                    </div>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-emerald-50/70 border border-emerald-100 text-[11px] text-emerald-900 leading-relaxed">
                  <strong>Notice:</strong> {result.message}
                </div>
              </div>

              {/* Recommended Crops List */}
              <div className="space-y-4">
                <h3 className="text-base font-bold text-slate-900 flex items-center justify-between">
                  <span>Recommended Crops for Your Location</span>
                  <span className="text-xs font-normal text-slate-500">
                    Ranked by agro-climatic score
                  </span>
                </h3>

                <div className="space-y-4">
                  {result.recommendations?.map((rec, index) => (
                    <div
                      key={index}
                      className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4 hover:border-emerald-300 transition"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <div className="text-xs font-bold text-emerald-700 uppercase tracking-wider">
                            Recommendation #{index + 1}
                          </div>
                          <h4 className="text-xl font-bold text-slate-900 mt-0.5">{rec.crop_name}</h4>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-black text-emerald-600 font-mono">
                            {rec.suitability_score}%
                          </div>
                          <div className="text-[10px] font-semibold text-slate-500">Suitability Index</div>
                        </div>
                      </div>

                      {/* Suitability reason */}
                      <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
                        <strong>Reason:</strong> {rec.reason}
                      </p>

                      {/* Guidance & water details */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                        <div className="space-y-1">
                          <span className="text-slate-400 font-medium">Water Requirement:</span>
                          <p className="text-slate-800 font-medium">{rec.water_requirement}</p>
                        </div>
                        <div className="space-y-1">
                          <span className="text-slate-400 font-medium">Optimal Season:</span>
                          <p className="text-slate-800 font-medium">{rec.suitable_season}</p>
                        </div>
                      </div>

                      <div className="pt-3 border-t border-slate-100 text-xs text-emerald-900">
                        <strong>Cultivation Guidance:</strong> {rec.basic_guidance}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ScanEye,
  Trees,
  Scale,
  CloudSun,
  AlertTriangle,
  ArrowRight,
  MapPin,
  Clock,
  Sparkles,
  ChevronRight,
  ShieldCheck,
  CheckCircle2,
  Calendar
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { weatherService, diseaseService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function FarmerDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [weatherData, setWeatherData] = useState(null);
  const [recentCases, setRecentCases] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    const fetchDashboardData = async () => {
      try {
        const [wRes, casesRes] = await Promise.allSettled([
          weatherService.getCurrent({ city: user?.village_district || 'Punjab' }),
          diseaseService.getMyCases(),
        ]);

        if (isMounted) {
          if (wRes.status === 'fulfilled') setWeatherData(wRes.value);
          if (casesRes.status === 'fulfilled') setRecentCases(casesRes.value.slice(0, 3));
        }
      } catch (err) {
        console.error('Error fetching dashboard feed:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchDashboardData();
    return () => {
      isMounted = false;
    };
  }, [user]);

  return (
    <div className="space-y-8 pb-12">
      {/* 1. Welcome & Location Banner */}
      <div className="bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-800 rounded-3xl p-6 sm:p-8 text-white shadow-sm relative overflow-hidden">
        <div className="relative z-10 space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-900/60 text-emerald-200 text-xs font-semibold border border-emerald-600/50">
            <Sparkles className="w-3.5 h-3.5 text-emerald-300" />
            <span>Kisan Advisory Center</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">
            Namaste, {user?.full_name || 'Farmer Friend'}!
          </h1>

          <div className="flex flex-wrap items-center gap-4 text-xs text-emerald-100 pt-1">
            <div className="flex items-center gap-1.5 bg-emerald-900/40 px-3 py-1 rounded-lg border border-emerald-600/40">
              <MapPin className="w-3.5 h-3.5 text-emerald-300" />
              <span>
                {user?.village_district ? `${user.village_district}, ${user.state}` : 'Farm Location Set'}
              </span>
            </div>

            <div className="flex items-center gap-1.5 bg-emerald-900/40 px-3 py-1 rounded-lg border border-emerald-600/40">
              <Calendar className="w-3.5 h-3.5 text-emerald-300" />
              <span>{new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' })}</span>
            </div>
          </div>
        </div>

        {/* Decorative background shape */}
        <div className="absolute right-0 bottom-0 translate-x-8 translate-y-8 w-64 h-64 bg-emerald-600/20 rounded-full blur-2xl pointer-events-none"></div>
      </div>

      {/* 2. Most Prominent Action: DETECT PLANT DISEASE (Part E Requirement) */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border-2 border-emerald-500 shadow-sm relative overflow-hidden">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="space-y-3 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
              <span className="w-2 h-2 rounded-full bg-emerald-600 animate-ping"></span>
              <span>Primary Diagnostic Action</span>
            </div>

            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Detect Plant Disease & Receive Treatment
            </h2>

            <p className="text-sm text-slate-600 leading-relaxed">
              Found diseased, spotted, or yellowing leaves on your crops? Snap or upload a photo to immediately run our multi-crop leaf diagnostic pipeline and access organic or certified chemical prescriptions.
            </p>

            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 pt-1">
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Instant leaf validation
              </span>
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Agronomic knowledge-base
              </span>
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Agricultural expert review
              </span>
            </div>
          </div>

          <div className="shrink-0 w-full lg:w-auto">
            <button
              onClick={() => navigate('/disease-detection')}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-3 px-8 py-4 rounded-2xl bg-emerald-600 text-white font-bold text-base hover:bg-emerald-700 shadow-md transition group"
            >
              <ScanEye className="w-6 h-6 text-emerald-100 group-hover:scale-110 transition-transform" />
              <span>Detect Plant Disease</span>
              <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
            </button>
          </div>
        </div>
      </div>

      {/* 3. Weather Summary & Agricultural Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Weather card */}
        <div className="lg:col-span-5 bg-white rounded-3xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <div className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
                  <CloudSun className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-slate-900 text-base">Weather Summary</h3>
              </div>
              <Link
                to="/weather-monitoring"
                className="text-xs font-semibold text-emerald-600 hover:text-emerald-700"
              >
                Full Forecast →
              </Link>
            </div>

            {loading ? (
              <LoadingSpinner message="Checking local weather..." size="sm" />
            ) : weatherData?.current ? (
              <div className="space-y-4">
                <div className="flex items-baseline justify-between">
                  <div>
                    <span className="text-4xl font-extrabold text-slate-900">
                      {weatherData.current.temperature_celsius}°C
                    </span>
                    <span className="text-xs text-slate-500 ml-2">
                      Feels like {weatherData.current.feels_like_celsius}°C
                    </span>
                  </div>
                  <div className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-100">
                    {weatherData.current.weather_condition}
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2 pt-2 text-center text-xs">
                  <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="text-slate-400">Humidity</div>
                    <div className="font-bold text-slate-800 text-sm mt-0.5">
                      {weatherData.current.humidity_percent}%
                    </div>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="text-slate-400">Rainfall</div>
                    <div className="font-bold text-slate-800 text-sm mt-0.5">
                      {weatherData.current.rainfall_mm} mm
                    </div>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="text-slate-400">Wind</div>
                    <div className="font-bold text-slate-800 text-sm mt-0.5">
                      {weatherData.current.wind_speed_kmh} km/h
                    </div>
                  </div>
                </div>

                <div className="text-[11px] text-slate-500 italic">
                  {weatherData.current.data_source_note}
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-500">Weather data unavailable.</p>
            )}
          </div>
        </div>

        {/* Agricultural Alerts */}
        <div className="lg:col-span-7 bg-white rounded-3xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <div className="w-9 h-9 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center">
                  <AlertTriangle className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-slate-900 text-base">Agricultural Alerts & Advisories</h3>
              </div>
              <span className="text-[11px] font-semibold text-slate-500">Rule-Based Engine</span>
            </div>

            <div className="space-y-3">
              {weatherData?.alerts && weatherData.alerts.length > 0 ? (
                weatherData.alerts.slice(0, 2).map((alt) => (
                  <div
                    key={alt.id}
                    className={`p-4 rounded-2xl border text-xs space-y-1.5 ${
                      alt.severity === 'Critical' || alt.severity === 'Warning'
                        ? 'bg-amber-50/70 border-amber-200 text-amber-950'
                        : 'bg-emerald-50/60 border-emerald-100 text-emerald-950'
                    }`}
                  >
                    <div className="flex items-center justify-between font-bold">
                      <span className="text-sm">{alt.title}</span>
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded-full ${
                          alt.severity === 'Critical'
                            ? 'bg-red-600 text-white'
                            : alt.severity === 'Warning'
                            ? 'bg-amber-500 text-white'
                            : 'bg-emerald-600 text-white'
                        }`}
                      >
                        {alt.severity}
                      </span>
                    </div>
                    <p className="text-xs opacity-90">{alt.description}</p>
                    <div className="font-semibold pt-1 border-t border-amber-200/60 text-emerald-900">
                      💡 Suggestion: {alt.agricultural_suggestion}
                    </div>
                  </div>
                ))
              ) : (
                <div className="p-4 rounded-2xl bg-slate-50 text-xs text-slate-600 text-center">
                  No extreme weather threats recorded. Normal field conditions.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 4. Secondary Action Modules: Crop Recommendation & Fertilizer Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Crop Recommendation Card */}
        <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between group hover:border-emerald-300 transition">
          <div className="space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
              <Trees className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-700">
                Location & Climate Based
              </span>
              <h3 className="text-xl font-bold text-slate-900 mt-1">Smart Crop Recommendation</h3>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Find optimal crops suited to your district's regional soil order, current agricultural season, and irrigation water source (Borewell, Canal, or Rain-fed) without needing manual NPK chemical tests.
            </p>
          </div>
          <div className="pt-6 border-t border-slate-100 mt-6">
            <Link
              to="/crop-recommendation"
              className="inline-flex items-center gap-2 text-sm font-bold text-emerald-700 group-hover:text-emerald-800"
            >
              <span>Explore Crop Options</span>
              <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </Link>
          </div>
        </div>

        {/* Fertilizer Comparison Card */}
        <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between group hover:border-emerald-300 transition">
          <div className="space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
              <Scale className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-700">
                Formula Ranked
              </span>
              <h3 className="text-xl font-bold text-slate-900 mt-1">Fertilizer Comparison Hub</h3>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Compare commercial fertilizers side-by-side. Our mathematical formula normalizes pack pricing per kg against verified farmer satisfaction ratings so you don't overpay for nutrients.
            </p>
          </div>
          <div className="pt-6 border-t border-slate-100 mt-6">
            <Link
              to="/fertilizer-comparison"
              className="inline-flex items-center gap-2 text-sm font-bold text-emerald-700 group-hover:text-emerald-800"
            >
              <span>Compare Products</span>
              <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </Link>
          </div>
        </div>
      </div>

      {/* 5. Recent Activity Section */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-emerald-600" />
            <h3 className="font-bold text-slate-900 text-base">Your Recent Scans & Activity</h3>
          </div>
          <Link
            to="/disease-detection"
            className="text-xs font-semibold text-emerald-600 hover:text-emerald-700"
          >
            New Scan +
          </Link>
        </div>

        {recentCases.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {recentCases.map((c) => (
              <div
                key={c.id}
                className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900">{c.crop_type || 'Crop Leaf'}</span>
                  <span
                    className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                      c.status === 'reviewed'
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-amber-100 text-amber-800'
                    }`}
                  >
                    {c.status === 'reviewed' ? 'Expert Verified' : 'Under Review'}
                  </span>
                </div>
                <div className="text-slate-500 truncate">
                  {c.predicted_disease || 'AI Assessment Pending'}
                </div>
                <div className="text-[10px] text-slate-400">
                  {new Date(c.created_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="py-6 text-center text-xs text-slate-500">
            No plant disease scans recorded yet.{' '}
            <Link to="/disease-detection" className="text-emerald-600 font-semibold underline">
              Upload your first leaf sample
            </Link>{' '}
            to start monitoring your crop health.
          </div>
        )}
      </div>
    </div>
  );
}


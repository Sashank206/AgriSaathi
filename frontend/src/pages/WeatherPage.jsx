import React, { useState, useEffect } from 'react';
import {
  CloudSun,
  MapPin,
  Compass,
  Wind,
  Droplets,
  CloudRain,
  AlertTriangle,
  Calendar,
  CheckCircle2,
  Info,
  ShieldAlert,
  Sparkles,
  Thermometer
} from 'lucide-react';
import { weatherService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from '../components/LoadingSpinner';

export default function WeatherPage() {
  const { user } = useAuth();
  const [cityInput, setCityInput] = useState(user?.village_district || 'Ludhiana');
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchWeather = async (cityName = cityInput, lat = null, lon = null) => {
    setLoading(true);
    setError('');
    try {
      const data = await weatherService.getCurrent({
        city: cityName || undefined,
        lat: lat || undefined,
        lon: lon || undefined,
      });
      setWeatherData(data);
    } catch (err) {
      setError(err.message || 'Could not retrieve meteorological data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWeather(user?.village_district || 'Ludhiana');
  }, [user]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (cityInput.trim()) {
      fetchWeather(cityInput.trim());
    }
  };

  const handleDetectGPS = () => {
    if (!navigator.geolocation) {
      setError('Browser geolocation is not supported.');
      return;
    }
    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        fetchWeather(null, pos.coords.latitude, pos.coords.longitude);
      },
      (err) => {
        setError('GPS lookup failed: ' + err.message);
        setLoading(false);
      }
    );
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          <CloudSun className="w-4 h-4 text-emerald-600" />
          <span>Agro-Meteorology Hub</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Weather Monitoring & Smart Agricultural Alerts
        </h1>
        <p className="text-sm text-slate-600 max-w-2xl leading-relaxed">
          Real-time agro-weather tracking with tailored alerts for excess precipitation, lodging wind velocities, and frost hazards paired with proactive crop-protection steps.
        </p>
      </div>

      {/* Search / Location Bar */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm">
        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <MapPin className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              placeholder="Enter District or City name (e.g. Ludhiana, Nashik, Varanasi)..."
              value={cityInput}
              onChange={(e) => setCityInput(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-2.5 rounded-xl bg-slate-900 text-white font-semibold text-xs hover:bg-slate-800 transition"
          >
            Check Weather
          </button>
          <button
            type="button"
            onClick={handleDetectGPS}
            className="px-4 py-2.5 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-semibold hover:bg-emerald-100 transition flex items-center justify-center gap-1.5"
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Use My GPS</span>
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-xs text-red-700 flex items-start gap-2">
          <AlertTriangle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {loading ? (
        <LoadingSpinner message="Retrieving meteorological observation records..." size="lg" />
      ) : weatherData ? (
        <div className="space-y-8">
          {/* Current Weather Card */}
          <div className="bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-800 text-white rounded-3xl p-6 sm:p-10 shadow-sm relative overflow-hidden">
            <div className="relative z-10 space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="text-xs uppercase font-bold tracking-widest text-emerald-200">
                    Observation Location
                  </div>
                  <h2 className="text-3xl font-extrabold tracking-tight">
                    {weatherData.current.location_name}, {weatherData.current.country}
                  </h2>
                </div>
                <div className="px-3.5 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-500/40 text-xs font-semibold text-emerald-200">
                  {weatherData.current.weather_condition}
                </div>
              </div>

              {/* Main Weather Metrics */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-2xl bg-emerald-900/40 border border-emerald-600/40">
                  <div className="flex items-center gap-2 text-xs text-emerald-200">
                    <Thermometer className="w-4 h-4" />
                    <span>Temperature</span>
                  </div>
                  <div className="text-3xl font-black mt-1 font-mono">
                    {weatherData.current.temperature_celsius}°C
                  </div>
                  <div className="text-[11px] text-emerald-300/80 mt-0.5">
                    Feels like {weatherData.current.feels_like_celsius}°C
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-emerald-900/40 border border-emerald-600/40">
                  <div className="flex items-center gap-2 text-xs text-emerald-200">
                    <Droplets className="w-4 h-4" />
                    <span>Relative Humidity</span>
                  </div>
                  <div className="text-3xl font-black mt-1 font-mono">
                    {weatherData.current.humidity_percent}%
                  </div>
                  <div className="text-[11px] text-emerald-300/80 mt-0.5">Moisture level</div>
                </div>

                <div className="p-4 rounded-2xl bg-emerald-900/40 border border-emerald-600/40">
                  <div className="flex items-center gap-2 text-xs text-emerald-200">
                    <CloudRain className="w-4 h-4" />
                    <span>Precipitation</span>
                  </div>
                  <div className="text-3xl font-black mt-1 font-mono">
                    {weatherData.current.rainfall_mm} mm
                  </div>
                  <div className="text-[11px] text-emerald-300/80 mt-0.5">Past hour accumulation</div>
                </div>

                <div className="p-4 rounded-2xl bg-emerald-900/40 border border-emerald-600/40">
                  <div className="flex items-center gap-2 text-xs text-emerald-200">
                    <Wind className="w-4 h-4" />
                    <span>Wind Velocity</span>
                  </div>
                  <div className="text-3xl font-black mt-1 font-mono">
                    {weatherData.current.wind_speed_kmh} km/h
                  </div>
                  <div className="text-[11px] text-emerald-300/80 mt-0.5">Surface anemometer</div>
                </div>
              </div>

              {/* Data provenance notice */}
              <div className="text-xs text-emerald-200/90 pt-2 border-t border-emerald-600/40">
                {weatherData.current.data_source_note}
              </div>
            </div>
          </div>

          {/* Rule-Based Agricultural Alerts Section */}
          <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2.5">
                <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center">
                  <AlertTriangle className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 text-base">Agricultural Risk Alerts</h3>
                  <p className="text-xs text-slate-500">Evaluated against crop physiological vulnerability thresholds</p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {weatherData.alerts?.map((alt) => (
                <div
                  key={alt.id}
                  className={`p-5 rounded-2xl border text-xs space-y-2.5 ${
                    alt.severity === 'Critical'
                      ? 'bg-red-50/70 border-red-200 text-red-950'
                      : alt.severity === 'Warning'
                      ? 'bg-amber-50/70 border-amber-200 text-amber-950'
                      : 'bg-emerald-50/60 border-emerald-200 text-emerald-950'
                  }`}
                >
                  <div className="flex items-center justify-between font-bold">
                    <span className="text-sm">{alt.title}</span>
                    <span
                      className={`text-[10px] px-2.5 py-0.5 rounded-full font-bold uppercase ${
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
                  <p className="leading-relaxed opacity-90">{alt.description}</p>
                  <div className="pt-2 border-t border-slate-200/60 font-semibold text-emerald-900">
                    🌾 Mitigation Step: {alt.agricultural_suggestion}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 5-Day Agro-Forecast */}
          {weatherData.forecast && weatherData.forecast.length > 0 && (
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-emerald-600" />
                <span>5-Day Agricultural Outlook</span>
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
                {weatherData.forecast.map((day, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-2xl bg-slate-50 border border-slate-100 text-center space-y-2"
                  >
                    <div className="text-xs font-bold text-slate-800">{day.day_name}</div>
                    <div className="text-[11px] text-slate-400">{day.date}</div>
                    <div className="text-xs font-semibold text-emerald-700 bg-white py-1 px-2 rounded-lg border border-slate-100">
                      {day.condition}
                    </div>
                    <div className="text-sm font-bold text-slate-900 font-mono">
                      {day.temp_max}° <span className="text-slate-400 font-normal">/ {day.temp_min}°</span>
                    </div>
                    <div className="text-[10px] text-slate-500">
                      🌧 {day.pop_percent}% Rain Chance
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* General Farming Advisories */}
          {weatherData.farming_advisory && weatherData.farming_advisory.length > 0 && (
            <div className="bg-slate-50 rounded-3xl p-6 border border-slate-200 text-xs space-y-2">
              <div className="font-bold text-slate-800">Krishi Advisory Guidelines:</div>
              <ul className="list-disc list-inside space-y-1 text-slate-600">
                {weatherData.farming_advisory.map((adv, i) => (
                  <li key={i}>{adv}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
}


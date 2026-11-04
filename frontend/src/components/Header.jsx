import React, { useState, useEffect } from 'react';
import { Menu, MapPin, CloudSun, Bell, Shield, User, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { weatherService } from '../services/api';

export default function Header({ setIsSidebarOpen }) {
  const { user, logout } = useAuth();
  const [weatherSnap, setWeatherSnap] = useState(null);

  useEffect(() => {
    let isMounted = true;
    const fetchWeatherSnapshot = async () => {
      try {
        const data = await weatherService.getCurrent({ city: user?.village_district || 'Delhi' });
        if (isMounted && data?.current) {
          setWeatherSnap(data.current);
        }
      } catch {
        // Soft fail for weather pill
      }
    };
    fetchWeatherSnapshot();
    return () => {
      isMounted = false;
    };
  }, [user]);

  return (
    <header className="h-16 bg-white border-b border-gray-200 sticky top-0 z-30 flex items-center justify-between px-4 sm:px-6 lg:px-8">
      {/* Mobile toggle & location */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => setIsSidebarOpen((prev) => !prev)}
          className="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 focus:outline-none"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Location badge */}
        <div className="flex items-center gap-2 text-xs text-gray-700 bg-gray-50 border border-gray-200/80 px-3 py-1.5 rounded-full">
          <MapPin className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
          <span className="font-medium truncate max-w-[150px] sm:max-w-[220px]">
            {user?.village_district ? `${user.village_district}, ${user.state}` : 'National Agro Network'}
          </span>
        </div>

        {/* Weather snapshot pill */}
        {weatherSnap && (
          <div className="hidden sm:flex items-center gap-1.5 text-xs text-emerald-800 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-full">
            <CloudSun className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
            <span className="font-semibold">{weatherSnap.temperature_celsius}°C</span>
            <span className="text-emerald-600 hidden lg:inline">({weatherSnap.weather_condition})</span>
          </div>
        )}
      </div>

      {/* Right controls */}
      <div className="flex items-center gap-3">
        {/* Role tag */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold bg-gray-100 text-gray-700 border border-gray-200">
          <Shield className="w-3.5 h-3.5 text-emerald-600" />
          <span className="capitalize">{user?.role || 'Farmer'}</span>
        </div>

        {/* User initials icon */}
        <div className="w-9 h-9 rounded-full bg-emerald-600 text-white font-semibold flex items-center justify-center text-sm shadow-sm">
          {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
        </div>
      </div>
    </header>
  );
}


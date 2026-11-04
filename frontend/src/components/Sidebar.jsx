import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  ScanEye,
  Trees,
  Scale,
  CloudSun,
  ShieldCheck,
  Microscope,
  LogOut,
  ChevronRight,
  Sprout,
  HelpCircle
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Sidebar({ isOpen, setIsOpen }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const farmerNavItems = [
    {
      name: 'Overview',
      path: '/farmer',
      icon: LayoutDashboard,
      badge: null,
    },
    {
      name: 'Detect Plant Disease',
      path: '/disease-detection',
      icon: ScanEye,
      badge: 'Primary AI',
      highlight: true,
    },
    {
      name: 'Crop Recommendation',
      path: '/crop-recommendation',
      icon: Trees,
      badge: 'Location AI',
    },
    {
      name: 'Fertilizer Comparison',
      path: '/fertilizer-comparison',
      icon: Scale,
      badge: null,
    },
    {
      name: 'Weather & Smart Alerts',
      path: '/weather-monitoring',
      icon: CloudSun,
      badge: 'Live',
    },
  ];

  const adminNavItems = [
    {
      name: 'Admin Dashboard',
      path: '/admin',
      icon: ShieldCheck,
      badge: 'Admin',
    },
    {
      name: 'Plant Disease Scanner',
      path: '/disease-detection',
      icon: ScanEye,
      badge: null,
    },
    {
      name: 'Crop Recommendation',
      path: '/crop-recommendation',
      icon: Trees,
      badge: null,
    },
    {
      name: 'Fertilizer Catalog',
      path: '/fertilizer-comparison',
      icon: Scale,
      badge: null,
    },
    {
      name: 'Weather Alerts Hub',
      path: '/weather-monitoring',
      icon: CloudSun,
      badge: null,
    },
  ];

  const expertNavItems = [
    {
      name: 'Expert Diagnosis Hub',
      path: '/expert',
      icon: Microscope,
      badge: 'Queue',
    },
    {
      name: 'Plant Disease Tool',
      path: '/disease-detection',
      icon: ScanEye,
      badge: null,
    },
    {
      name: 'Crop Recommendations',
      path: '/crop-recommendation',
      icon: Trees,
      badge: null,
    },
    {
      name: 'Fertilizer Analysis',
      path: '/fertilizer-comparison',
      icon: Scale,
      badge: null,
    },
    {
      name: 'Weather Monitoring',
      path: '/weather-monitoring',
      icon: CloudSun,
      badge: null,
    },
  ];

  let navItems = farmerNavItems;
  if (user?.role === 'admin') navItems = adminNavItems;
  if (user?.role === 'expert') navItems = expertNavItems;

  return (
    <aside
      className={`fixed inset-y-0 left-0 z-40 w-64 bg-slate-900 text-slate-200 border-r border-slate-800 flex flex-col justify-between transition-transform duration-200 ease-in-out md:translate-x-0 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      <div>
        {/* Brand header */}
        <div className="h-16 flex items-center px-6 border-b border-slate-800 bg-slate-950/40">
          <NavLink to="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-emerald-600 flex items-center justify-center text-white shadow-sm">
              <Sprout className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-white text-lg tracking-tight">
                Agri<span className="text-emerald-400">Saathi</span>
              </span>
              <span className="block text-[9px] font-semibold uppercase tracking-widest text-emerald-500">
                {user?.role?.toUpperCase() || 'PORTAL'}
              </span>
            </div>
          </NavLink>
        </div>

        {/* Role badge */}
        <div className="px-5 py-4 border-b border-slate-800/80 bg-slate-900/60">
          <div className="text-xs text-slate-400">Signed in as</div>
          <div className="font-medium text-slate-100 truncate text-sm">
            {user?.full_name || 'Farmer User'}
          </div>
          <div className="flex items-center gap-1.5 mt-1 text-xs text-emerald-400 font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>{user?.village_district ? `${user.village_district}, ${user.state}` : 'Kisan Portal'}</span>
          </div>
        </div>

        {/* Navigation list */}
        <div className="px-3 py-4 space-y-1">
          <div className="px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2">
            Main Navigation
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-emerald-600 text-white shadow-sm'
                      : item.highlight
                      ? 'bg-emerald-950/60 text-emerald-300 border border-emerald-800/70 hover:bg-emerald-900/40'
                      : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
                  }`
                }
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-5 h-5 ${item.highlight ? 'text-emerald-400' : ''}`} />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                      item.highlight
                        ? 'bg-emerald-400 text-slate-950 font-bold'
                        : 'bg-slate-800 text-slate-300 border border-slate-700'
                    }`}
                  >
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </div>
      </div>

      {/* Bottom user action & logout */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/30 space-y-2">
        <NavLink
          to="/how-it-works"
          className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition"
        >
          <HelpCircle className="w-4 h-4 text-slate-400" />
          <span>Documentation & Advisory</span>
        </NavLink>
        <button
          onClick={handleLogout}
          className="w-full flex items-center justify-between px-3.5 py-2 rounded-xl text-sm font-medium text-red-400 hover:bg-red-950/40 hover:text-red-300 border border-red-900/30 transition"
        >
          <div className="flex items-center gap-2.5">
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </div>
          <ChevronRight className="w-4 h-4 text-red-500/70" />
        </button>
      </div>
    </aside>
  );
}


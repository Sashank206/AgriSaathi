import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Sprout, Lock, Mail, ArrowRight, AlertCircle, Sparkles, UserCheck, ShieldCheck, Microscope } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { login, register } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const redirectByRole = (user) => {
    if (user.role === 'admin') navigate('/admin');
    else if (user.role === 'expert') navigate('/expert');
    else navigate('/farmer');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const user = await login(email, password);
      redirectByRole(user);
    } catch (err) {
      setError(err.message || 'Login failed. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  const setDemoAccount = async (demoEmail, demoPassword, roleName, fullName, village, state) => {
    setEmail(demoEmail);
    setPassword(demoPassword);
    setError('');
    setLoading(true);
    try {
      // Try login first
      const user = await login(demoEmail, demoPassword);
      redirectByRole(user);
    } catch (loginErr) {
      const msg = loginErr.message || '';
      if (
        msg.toLowerCase().includes('network error') ||
        msg.toLowerCase().includes('failed to fetch') ||
        msg.toLowerCase().includes('econnrefused')
      ) {
        setError(
          'Cannot reach AgriSaathi backend on http://localhost:8000. Please ensure the backend server is running: cd backend; .\\venv\\Scripts\\uvicorn app.main:app --reload --port 8000'
        );
        return;
      }

      // If credentials were not found, register demo user
      try {
        const newUser = await register({
          full_name: fullName,
          email: demoEmail,
          password: demoPassword,
          phone_number: '9876543210',
          role: roleName,
          village_district: village,
          state: state,
        });
        redirectByRole(newUser);
      } catch (regErr) {
        setError('Could not initialize demo login: ' + regErr.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 sm:p-10 rounded-3xl border border-slate-200 shadow-sm">
        {/* Header */}
        <div className="text-center space-y-2">
          <Link to="/" className="inline-flex items-center gap-2 mb-2">
            <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center text-white">
              <Sprout className="w-6 h-6" />
            </div>
            <span className="text-xl font-bold tracking-tight text-slate-900">
              Agri<span className="text-emerald-600">Saathi</span>
            </span>
          </Link>
          <h2 className="text-2xl font-bold text-slate-900">Sign in to your account</h2>
          <p className="text-xs text-slate-500">
            Access your agricultural advisory dashboard and case histories
          </p>
        </div>

        {/* Quick Demo Credentials Bar for Easy Review */}
        <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200/80 space-y-2">
          <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-800">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>1-Click Evaluator Roles:</span>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <button
              type="button"
              onClick={() =>
                setDemoAccount(
                  'farmer@agrisaathi.org',
                  'farmer123',
                  'farmer',
                  'Ramesh Patel (Farmer)',
                  'Ludhiana',
                  'Punjab'
                )
              }
              className="py-1.5 px-2 rounded-lg bg-white hover:bg-emerald-100/70 border border-emerald-200 text-[11px] font-semibold text-emerald-800 flex items-center justify-center gap-1 transition"
            >
              <UserCheck className="w-3 h-3 text-emerald-600" />
              <span>Farmer</span>
            </button>
            <button
              type="button"
              onClick={() =>
                setDemoAccount(
                  'expert@agrisaathi.org',
                  'expert123',
                  'expert',
                  'Dr. Anita Sharma (Plant Pathologist)',
                  'Krishi Vigyan Kendra',
                  'Maharashtra'
                )
              }
              className="py-1.5 px-2 rounded-lg bg-white hover:bg-emerald-100/70 border border-emerald-200 text-[11px] font-semibold text-emerald-800 flex items-center justify-center gap-1 transition"
            >
              <Microscope className="w-3 h-3 text-emerald-600" />
              <span>Expert</span>
            </button>
            <button
              type="button"
              onClick={() =>
                setDemoAccount(
                  'admin@agrisaathi.org',
                  'admin123',
                  'admin',
                  'System Administrator',
                  'Central Agritech Hub',
                  'Delhi'
                )
              }
              className="py-1.5 px-2 rounded-lg bg-white hover:bg-emerald-100/70 border border-emerald-200 text-[11px] font-semibold text-emerald-800 flex items-center justify-center gap-1 transition"
            >
              <ShieldCheck className="w-3 h-3 text-emerald-600" />
              <span>Admin</span>
            </button>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 flex items-start gap-2.5 text-xs text-red-700">
            <AlertCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="farmer@example.com"
                className="w-full pl-10 pr-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-emerald-600 text-white font-semibold text-sm hover:bg-emerald-700 transition shadow-sm disabled:opacity-60"
          >
            {loading ? (
              <span>Authenticating...</span>
            ) : (
              <>
                <span>Sign In to Dashboard</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Register link */}
        <div className="text-center text-xs text-slate-600">
          New to AgriSaathi?{' '}
          <Link to="/register" className="font-semibold text-emerald-600 hover:text-emerald-700">
            Create a farmer account
          </Link>
        </div>
      </div>
    </div>
  );
}


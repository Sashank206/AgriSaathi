import React from 'react';
import { Sprout, Target, Shield, Users, Award, Code2, Database, Brain } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          About AgriSaathi
        </div>
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
          Bridging Agronomic Science and Everyday Farming
        </h1>
        <p className="text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
          AgriSaathi was born out of a simple observation: modern agricultural technology often demands high-level laboratory data that everyday farmers do not possess, while failing to provide immediate diagnosis when crop diseases emerge.
        </p>
      </div>

      {/* Mission / Vision Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white p-7 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
            <Target className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">Our Core Mission</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Provide farmers with instant, trustworthy disease diagnostics and location-driven advisories without imposing unrealistic inputs or false promises.
          </p>
        </div>

        <div className="bg-white p-7 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
            <Shield className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">Truth in Agritech</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            We operate on strict algorithmic integrity. If an AI model is not yet trained for a rare disease, the platform truthfully says so and connects to certified extension experts.
          </p>
        </div>

        <div className="bg-white p-7 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
            <Users className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">Collaborative Ecosystem</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Connecting ground-level farmers, Krishi Vigyan Kendra scientists, and agricultural administrators on a shared digital infrastructure.
          </p>
        </div>
      </div>

      {/* Tech Stack Breakdown */}
      <div className="bg-slate-900 text-white p-8 sm:p-12 rounded-3xl space-y-8">
        <div className="space-y-2">
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            Engineered For Scale
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
            The AgriSaathi Technology Foundation
          </h2>
          <p className="text-sm text-slate-400 max-w-xl">
            A production-ready decoupled architecture built with modern frameworks.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="p-5 rounded-2xl bg-slate-800/80 border border-slate-700 space-y-2">
            <Brain className="w-6 h-6 text-emerald-400" />
            <h4 className="font-bold text-sm text-white">AI / ML Pipelines</h4>
            <p className="text-xs text-slate-400">
              TensorFlow/Keras CNNs for leaf pathology + Scikit-Learn / XGBoost for location crop suitability.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-800/80 border border-slate-700 space-y-2">
            <Code2 className="w-6 h-6 text-emerald-400" />
            <h4 className="font-bold text-sm text-white">FastAPI Engine</h4>
            <p className="text-xs text-slate-400">
              High-throughput async Python REST API with JWT security and role-based route protection.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-800/80 border border-slate-700 space-y-2">
            <Database className="w-6 h-6 text-emerald-400" />
            <h4 className="font-bold text-sm text-white">MongoDB Data Store</h4>
            <p className="text-xs text-slate-400">
              Schematized collections for cases, agronomic knowledge, fertilizer catalog, and expert reviews.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-800/80 border border-slate-700 space-y-2">
            <Sprout className="w-6 h-6 text-emerald-400" />
            <h4 className="font-bold text-sm text-white">React + Vite UI</h4>
            <p className="text-xs text-slate-400">
              Responsive Tailwind CSS interface designed for rapid field operation across all devices.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}


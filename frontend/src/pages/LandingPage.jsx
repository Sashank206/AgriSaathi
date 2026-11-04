import React from 'react';
import { Link } from 'react-router-dom';
import {
  ScanEye,
  Trees,
  Scale,
  CloudSun,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Cpu,
  Sparkles,
  Award,
  ChevronRight,
  Droplets,
  Microscope,
  Leaf
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="space-y-24 pb-20">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 sm:pt-20 bg-gradient-to-b from-emerald-50/70 via-white to-slate-50 border-b border-emerald-100/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center pb-20">
            {/* Left Column: Heading & CTAs */}
            <div className="lg:col-span-7 space-y-6 text-left">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold tracking-wide border border-emerald-200">
                <Sparkles className="w-4 h-4 text-emerald-600" />
                <span>Next-Generation Agricultural AI Intelligence</span>
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.15]">
                Smart Farming Decisions, <br className="hidden sm:inline" />
                <span className="text-emerald-600">Empowered by AI.</span>
              </h1>

              <p className="text-lg text-slate-600 max-w-2xl leading-relaxed">
                AgriSaathi integrates deep-learning plant disease diagnosis, location-driven crop recommendations, transparent fertilizer ranking, and precision weather alerts into one dependable platform for Indian farmers.
              </p>

              {/* CTAs */}
              <div className="flex flex-wrap gap-4 pt-2">
                <Link
                  to="/register"
                  className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-emerald-600 text-white font-semibold text-base hover:bg-emerald-700 shadow-sm transition"
                >
                  <span>Get Started Free</span>
                  <ArrowRight className="w-5 h-5" />
                </Link>

                <a
                  href="#features"
                  className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white text-slate-700 font-semibold text-base border border-slate-300 hover:bg-slate-50 transition"
                >
                  <span>Explore Features</span>
                </a>
              </div>

              {/* Trust highlights */}
              <div className="grid grid-cols-3 gap-4 pt-6 border-t border-slate-200/80 text-xs text-slate-600">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>CNN Leaf Diagnostics</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>No Manual NPK Guesswork</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Expert Verification</span>
                </div>
              </div>
            </div>

            {/* Right Column: Visual Product Graphic */}
            <div className="lg:col-span-5 relative">
              <div className="relative mx-auto max-w-md bg-white rounded-3xl p-6 shadow-xl border border-emerald-100">
                {/* Decorative header */}
                <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-5">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
                      <ScanEye className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-slate-800">Primary AI Module</div>
                      <div className="text-[10px] text-slate-500">Plant Disease Identification</div>
                    </div>
                  </div>
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                    Live Interface
                  </span>
                </div>

                {/* Leaf scan simulation card */}
                <div className="relative aspect-4/3 rounded-2xl bg-emerald-950/90 overflow-hidden flex flex-col items-center justify-center p-6 text-center text-white">
                  <div className="absolute inset-0 bg-[radial-gradient(#10b981_1px,transparent_1px)] [background-size:16px_16px] opacity-20"></div>
                  <div className="w-16 h-16 rounded-2xl bg-emerald-600/30 border border-emerald-500/40 flex items-center justify-center text-emerald-300 mb-3 animate-pulse">
                    <Leaf className="w-8 h-8" />
                  </div>
                  <div className="text-sm font-semibold tracking-wide">Target: Tomato Leaf Sample</div>
                  <div className="text-xs text-emerald-300/80 mt-1">Multi-Crop CNN Diagnostic Engine</div>
                  <div className="mt-4 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-[11px] font-mono border border-emerald-500/30">
                    Confidence Assessment & Treatment Guide
                  </div>
                </div>

                {/* Floating summary pills */}
                <div className="mt-4 grid grid-cols-2 gap-3 text-left">
                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="text-[11px] text-slate-500">Treatment Plan</div>
                    <div className="text-xs font-semibold text-slate-800">Organic & Chemical</div>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="text-[11px] text-slate-500">Expert Review</div>
                    <div className="text-xs font-semibold text-emerald-700">Available On-Demand</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Four Core Features Section */}
      <section id="features" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-3 mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
            Integrated Agricultural Suite
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight">
            Four Core Tools Designed for the Realities of Farming
          </h2>
          <p className="text-slate-600 max-w-2xl mx-auto text-base">
            No fragmented apps or theoretical claims. Each module delivers practical, agronomic utility directly to your field.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Card 1: Plant Disease Detection (Primary AI - Highlighted) */}
          <div className="relative rounded-2xl bg-gradient-to-b from-emerald-50/80 to-white p-7 border-2 border-emerald-500 shadow-md flex flex-col justify-between group hover:shadow-lg transition">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="w-12 h-12 rounded-xl bg-emerald-600 flex items-center justify-center text-white shadow-sm">
                  <ScanEye className="w-6 h-6" />
                </div>
                <span className="px-2.5 py-1 rounded-full text-[10px] font-extrabold uppercase bg-emerald-600 text-white">
                  Primary AI
                </span>
              </div>
              <h3 className="text-xl font-bold text-slate-900">
                AI Plant Disease Detection
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Upload or capture leaf images for instant diagnosis of foliar infections. Receive symptom breakdowns, organic bio-treatments, and certified chemical remedies.
              </p>
            </div>
            <div className="pt-6 border-t border-emerald-100/80 mt-6">
              <Link
                to="/disease-detection"
                className="inline-flex items-center gap-1.5 text-sm font-semibold text-emerald-700 group-hover:text-emerald-800"
              >
                <span>Launch Disease Scanner</span>
                <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </div>
          </div>

          {/* Card 2: Location-Based Crop Recommendation */}
          <div className="rounded-2xl bg-white p-7 border border-slate-200 shadow-sm flex flex-col justify-between group hover:border-emerald-300 hover:shadow-md transition">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
                  <Trees className="w-6 h-6" />
                </div>
                <span className="px-2.5 py-1 rounded-full text-[10px] font-semibold bg-slate-100 text-slate-700">
                  Environmental
                </span>
              </div>
              <h3 className="text-xl font-bold text-slate-900">
                Smart Crop Recommendation
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Location-based crop suitability driven by GPS, regional soil orders, practical water sources (borewell, canal, rainfed), and seasonal climate — without requiring manual NPK inputs.
              </p>
            </div>
            <div className="pt-6 border-t border-slate-100 mt-6">
              <Link
                to="/crop-recommendation"
                className="inline-flex items-center gap-1.5 text-sm font-semibold text-emerald-700 group-hover:text-emerald-800"
              >
                <span>Recommend Crops</span>
                <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </div>
          </div>

          {/* Card 3: Fertilizer Comparison */}
          <div className="rounded-2xl bg-white p-7 border border-slate-200 shadow-sm flex flex-col justify-between group hover:border-emerald-300 hover:shadow-md transition">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
                  <Scale className="w-6 h-6" />
                </div>
                <span className="px-2.5 py-1 rounded-full text-[10px] font-semibold bg-slate-100 text-slate-700">
                  Formula Ranked
                </span>
              </div>
              <h3 className="text-xl font-bold text-slate-900">
                Fertilizer Price & Quality
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Objective product scoring combining cost-per-kilogram with farmer satisfaction ratings using mathematical multi-factor normalization. Stop overpaying for marketing gimmicks.
              </p>
            </div>
            <div className="pt-6 border-t border-slate-100 mt-6">
              <Link
                to="/fertilizer-comparison"
                className="inline-flex items-center gap-1.5 text-sm font-semibold text-emerald-700 group-hover:text-emerald-800"
              >
                <span>Compare Fertilizers</span>
                <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </div>
          </div>

          {/* Card 4: Weather Monitoring */}
          <div className="rounded-2xl bg-white p-7 border border-slate-200 shadow-sm flex flex-col justify-between group hover:border-emerald-300 hover:shadow-md transition">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
                  <CloudSun className="w-6 h-6" />
                </div>
                <span className="px-2.5 py-1 rounded-full text-[10px] font-semibold bg-slate-100 text-slate-700">
                  Agro-Alerts
                </span>
              </div>
              <h3 className="text-xl font-bold text-slate-900">
                Weather & Agricultural Alerts
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Rule-based agricultural weather advisories for extreme heat, heavy downpours, lodging wind risks, and frost hazards paired with targeted farm mitigation suggestions.
              </p>
            </div>
            <div className="pt-6 border-t border-slate-100 mt-6">
              <Link
                to="/weather-monitoring"
                className="inline-flex items-center gap-1.5 text-sm font-semibold text-emerald-700 group-hover:text-emerald-800"
              >
                <span>View Weather Hub</span>
                <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-slate-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-3 mb-16">
            <div className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-emerald-950 text-emerald-400 text-xs font-bold uppercase tracking-wider border border-emerald-800">
              User Journey
            </div>
            <h2 className="text-3xl sm:text-4xl font-bold tracking-tight">
              How AgriSaathi Works for You
            </h2>
            <p className="text-slate-400 max-w-xl mx-auto text-sm">
              Simple 3-step advisory workflow engineered to run seamlessly even on basic rural mobile networks.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-slate-800/80 rounded-2xl p-8 border border-slate-700/60 relative">
              <div className="w-10 h-10 rounded-xl bg-emerald-500 text-slate-950 font-black text-lg flex items-center justify-center mb-6">
                1
              </div>
              <h3 className="text-lg font-bold text-white mb-2">
                Snap Leaf or Select Location
              </h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Take a quick photo of an unhealthy plant leaf or choose your state, district, and irrigation water source with one click.
              </p>
            </div>

            <div className="bg-slate-800/80 rounded-2xl p-8 border border-slate-700/60 relative">
              <div className="w-10 h-10 rounded-xl bg-emerald-500 text-slate-950 font-black text-lg flex items-center justify-center mb-6">
                2
              </div>
              <h3 className="text-lg font-bold text-white mb-2">
                Automated Agronomic Analysis
              </h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                The platform validates image integrity, assesses agro-climatic boundaries, and evaluates real environmental parameters.
              </p>
            </div>

            <div className="bg-slate-800/80 rounded-2xl p-8 border border-slate-700/60 relative">
              <div className="w-10 h-10 rounded-xl bg-emerald-500 text-slate-950 font-black text-lg flex items-center justify-center mb-6">
                3
              </div>
              <h3 className="text-lg font-bold text-white mb-2">
                Actionable Advice & Verification
              </h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Obtain concrete chemical and organic treatments, ranked fertilizer choices, or request manual review from a certified Agricultural Expert.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Advantages Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-emerald-50 rounded-3xl p-8 sm:p-12 border border-emerald-100">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-7 space-y-4">
              <div className="text-xs font-bold uppercase tracking-wider text-emerald-800">
                Why AgriSaathi?
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
                Built on Integrity and Agronomic Reality
              </h2>
              <div className="space-y-3 pt-2">
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">Truthful AI Architecture</h4>
                    <p className="text-xs text-slate-600">
                      We never invent false predictions. If model weights are unconfigured, you receive an honest status and an expert review option.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">Zero Unrealistic Requirements</h4>
                    <p className="text-xs text-slate-600">
                      Unlike systems demanding complex lab NPK chemical test numbers, our crop engine works with practical location, water source, and regional soil facts.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">Triple-Role Collaboration</h4>
                    <p className="text-xs text-slate-600">
                      Connects Farmers, Agricultural University Experts, and Extension Administrators on a unified, role-governed platform.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="lg:col-span-5 flex justify-center">
              <div className="p-8 rounded-2xl bg-white shadow-sm border border-emerald-100 text-center space-y-4 w-full max-w-sm">
                <div className="w-12 h-12 rounded-xl bg-emerald-600 text-white flex items-center justify-center mx-auto">
                  <Microscope className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-slate-900">Ready to examine your field?</h3>
                <p className="text-xs text-slate-600">
                  Create your free farmer account in 30 seconds and run your first leaf inspection.
                </p>
                <Link
                  to="/register"
                  className="block w-full py-3 rounded-xl bg-emerald-600 text-white font-semibold text-sm hover:bg-emerald-700 transition"
                >
                  Create Free Farmer Account
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}


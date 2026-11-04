import React from 'react';
import { Link } from 'react-router-dom';
import {
  ScanEye,
  Trees,
  Scale,
  CloudSun,
  ShieldCheck,
  CheckCircle2,
  ChevronRight,
  Droplets,
  Microscope,
  Info
} from 'lucide-react';

export default function FeaturesPage() {
  const features = [
    {
      id: 'disease',
      icon: ScanEye,
      title: 'AI Plant Disease Detection',
      tag: 'Primary AI Feature',
      highlight: true,
      description:
        'Upload or capture high-resolution leaf images directly from your mobile camera or desktop. The modular CNN interface checks for foliar pathogen symptoms across staple Indian crops including Tomato, Rice, Potato, Wheat, and Cotton.',
      benefits: [
        'Pre-validation for image blur, format, resolution, and corrupted uploads',
        'Transparent confidence scoring without synthetic predictions',
        'Dual-action agronomic recommendations: biological bio-agents and certified chemical controls',
        'Direct one-click routing to Krishi Vigyan Kendra agricultural scientists for unresolved scans'
      ],
      link: '/disease-detection',
      actionText: 'Open Disease Diagnostic Tool'
    },
    {
      id: 'crop',
      icon: Trees,
      title: 'Location-Based Crop Recommendation',
      tag: 'Agro-Climatic Intelligence',
      highlight: false,
      description:
        'A practical crop selection system that does NOT require chemical laboratory NPK values. Recommends optimal sowing candidates based on your geographical district, state, regional soil orders, practical water availability, and current agricultural season.',
      benefits: [
        'Browser GPS coordinates auto-detect your agro-climatic region',
        'ICAR soil reference database mapping (Alluvial, Black Vertisol, Red, Sandy Loam)',
        'Water availability choices: Borewell, Canal irrigation, Rain-fed, or Other',
        'Detailed crop profiles with water requirements and critical sowing window advisories'
      ],
      link: '/crop-recommendation',
      actionText: 'Explore Crop Recommender'
    },
    {
      id: 'fertilizer',
      icon: Scale,
      title: 'Fertilizer Price & Quality Comparison',
      tag: 'Economic Decision Support',
      highlight: false,
      description:
        'An unbiased mathematical comparison engine evaluating commercial fertilizers across unit pricing (₹/kg) and verified farmer rating metrics using our multi-criteria formula.',
      benefits: [
        'Mathematical scoring: S_i = α(1 - u_i/u_max) + (1 - α)(r_i/r_max)',
        'Customizable alpha (α) slider balancing budget vs peer satisfaction',
        'Distinction between government subsidized fertilizers (Urea, DAP, MOP) and specialty bio-fertilizers',
        'Transparent ranking summary with unit-cost breakdown'
      ],
      link: '/fertilizer-comparison',
      actionText: 'Compare Fertilizer Products'
    },
    {
      id: 'weather',
      icon: CloudSun,
      title: 'Weather Monitoring & Smart Agricultural Alerts',
      tag: 'Risk Mitigation',
      highlight: false,
      description:
        'Live weather tracking backed by OpenWeatherMap API and agro-meteorological rule engines. Evaluates temperature, humidity, wind velocity, and precipitation to generate timely agricultural hazard alerts.',
      benefits: [
        'Automatic alerts for heavy rainfall / waterlogging threats',
        'High gust wind advisories to prevent lodging in tall cereal crops',
        'Frost and extreme heat stress warnings with immediate mitigation measures',
        'Fungal proliferation notices during sustained high leaf-wetness periods'
      ],
      link: '/weather-monitoring',
      actionText: 'Check Agricultural Weather'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
      <div className="text-center space-y-4">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          Capabilities Overview
        </div>
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
          Comprehensive Agronomic Features
        </h1>
        <p className="text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Explore the four core pillars of the AgriSaathi platform engineered to support farmers through the entire crop lifecycle.
        </p>
      </div>

      <div className="space-y-10">
        {features.map((feat) => {
          const Icon = feat.icon;
          return (
            <div
              key={feat.id}
              className={`rounded-3xl p-8 sm:p-10 border transition-all ${
                feat.highlight
                  ? 'bg-gradient-to-r from-emerald-50/60 via-white to-emerald-50/20 border-emerald-400 shadow-md'
                  : 'bg-white border-slate-200 shadow-sm'
              }`}
            >
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                <div className="lg:col-span-8 space-y-4">
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                        feat.highlight ? 'bg-emerald-600 text-white' : 'bg-emerald-100 text-emerald-700'
                      }`}
                    >
                      <Icon className="w-6 h-6" />
                    </div>
                    <div>
                      <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">
                        {feat.tag}
                      </span>
                      <h2 className="text-2xl font-bold text-slate-900">{feat.title}</h2>
                    </div>
                  </div>

                  <p className="text-sm text-slate-600 leading-relaxed">{feat.description}</p>

                  <div className="space-y-2 pt-2">
                    {feat.benefits.map((b, i) => (
                      <div key={i} className="flex items-start gap-2 text-xs text-slate-700">
                        <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                        <span>{b}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="lg:col-span-4 flex flex-col items-start lg:items-end justify-center">
                  <Link
                    to={feat.link}
                    className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-emerald-600 text-white font-semibold text-sm hover:bg-emerald-700 transition shadow-sm w-full sm:w-auto justify-center"
                  >
                    <span>{feat.actionText}</span>
                    <ChevronRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}


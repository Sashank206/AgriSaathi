import React from 'react';
import { Camera, MapPin, Calculator, BellRing, Check, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function HowItWorksPage() {
  const steps = [
    {
      step: '01',
      title: 'Plant Disease Scanning Workflow',
      icon: Camera,
      description:
        'When you notice unusual spots, chlorosis, or wilting on your crop leaves, take a clear photo under natural daylight.',
      substeps: [
        'Place the affected leaf flat and focus on lesion boundaries.',
        'Upload or capture via smartphone or desktop browser.',
        'AgriSaathi validates dimensions, format, and image clarity.',
        'The deep-learning CNN evaluates symptoms against verified disease categories.'
      ]
    },
    {
      step: '02',
      title: 'Smart Location-Based Crop Selection',
      icon: MapPin,
      description:
        'Plan upcoming planting seasons with reliable agro-climatic alignment rather than guesswork or expensive chemical tests.',
      substeps: [
        'Allow browser GPS or select your Indian state and district.',
        'System matches predominant regional soil series from ICAR records.',
        'Indicate your realistic water availability (Borewell, Canal, or Rainfed).',
        'Review top suitable crops ranked by seasonal adaptation and water requirements.'
      ]
    },
    {
      step: '03',
      title: 'Fertilizer Quality & Price Calculation',
      icon: Calculator,
      description:
        'Make data-backed nutrient purchase decisions by comparing multiple commercial brands.',
      substeps: [
        'Search our verified product catalog across major agricultural fertilizers.',
        'Select two or more products to compare side-by-side.',
        'Adjust the weighting between unit cost (₹/kg) and peer farmer satisfaction ratings.',
        'Inspect the normalized score to select the most economical, high-performing fertilizer.'
      ]
    },
    {
      step: '04',
      title: 'Live Agro-Weather Alerts',
      icon: BellRing,
      description:
        'Stay ahead of extreme meteorological events that can harm flowering, tillering, or harvest.',
      substeps: [
        'Automatic checks for heavy precipitation and potential root-zone waterlogging.',
        'Wind speed monitoring to safeguard against lodging in tall cereal crops.',
        'Frost and heat stress warnings with immediate protective cultural practices.'
      ]
    }
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
      <div className="text-center space-y-4">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          Step-by-Step Guide
        </div>
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
          How AgriSaathi Works in the Field
        </h1>
        <p className="text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Designed from the ground up for simplicity, clarity, and reliability. Follow our operational workflow to get the most out of each module.
        </p>
      </div>

      <div className="space-y-8">
        {steps.map((s, idx) => {
          const Icon = s.icon;
          return (
            <div
              key={idx}
              className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm flex flex-col md:flex-row gap-8 items-start"
            >
              <div className="shrink-0 flex md:flex-col items-center gap-4">
                <span className="text-3xl font-black text-emerald-600 font-mono">{s.step}</span>
                <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
                  <Icon className="w-6 h-6" />
                </div>
              </div>

              <div className="space-y-4 flex-1">
                <h3 className="text-xl font-bold text-slate-900">{s.title}</h3>
                <p className="text-sm text-slate-600 leading-relaxed">{s.description}</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                  {s.substeps.map((sub, i) => (
                    <div
                      key={i}
                      className="flex items-start gap-2.5 p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs text-slate-700"
                    >
                      <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                      <span>{sub}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* CTA card */}
      <div className="bg-emerald-600 rounded-3xl p-8 sm:p-10 text-white text-center space-y-4 shadow-sm">
        <h3 className="text-2xl font-bold">Ready to put AgriSaathi to work on your farm?</h3>
        <p className="text-emerald-100 text-sm max-w-md mx-auto">
          Start diagnosing plant foliage, planning seasonal crops, and monitoring live alerts today.
        </p>
        <Link
          to="/register"
          className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white text-emerald-800 font-bold text-sm hover:bg-emerald-50 transition shadow-sm"
        >
          <span>Create Free Account</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}


import React from 'react';
import { Link } from 'react-router-dom';
import { Sprout, ShieldAlert, Award, Phone, Mail, MapPin } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 pt-16 pb-12 border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-gray-800">
          {/* Brand Info */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-9 h-9 rounded-xl bg-emerald-500 flex items-center justify-center text-white">
                <Sprout className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold tracking-tight text-white">
                Agri<span className="text-emerald-400">Saathi</span>
              </span>
            </div>
            <p className="text-sm text-gray-400 leading-relaxed">
              Empowering farmers across India with AI-driven plant disease diagnostics, location-tailored crop recommendations, transparent fertilizer market comparisons, and precision agricultural alerts.
            </p>
            <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1.5 rounded-lg w-fit">
              <Award className="w-4 h-4" />
              <span>Developed for Sustainable Agritech</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white mb-4">
              Core Modules
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/disease-detection" className="hover:text-emerald-400 transition">
                  AI Plant Disease Detection
                </Link>
              </li>
              <li>
                <Link to="/crop-recommendation" className="hover:text-emerald-400 transition">
                  Smart Crop Recommendation
                </Link>
              </li>
              <li>
                <Link to="/fertilizer-comparison" className="hover:text-emerald-400 transition">
                  Fertilizer Price & Quality
                </Link>
              </li>
              <li>
                <Link to="/weather-monitoring" className="hover:text-emerald-400 transition">
                  Weather & Agricultural Alerts
                </Link>
              </li>
            </ul>
          </div>

          {/* Institutional / Resources */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white mb-4">
              Platform & Extension
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/about" className="hover:text-emerald-400 transition">
                  About the Project
                </Link>
              </li>
              <li>
                <Link to="/how-it-works" className="hover:text-emerald-400 transition">
                  How AgriSaathi Works
                </Link>
              </li>
              <li>
                <Link to="/contact" className="hover:text-emerald-400 transition">
                  Expert Review Helpdesk
                </Link>
              </li>
              <li>
                <a
                  href="https://icar.org.in"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-emerald-400 transition flex items-center gap-1.5"
                >
                  ICAR Advisory Guidelines
                </a>
              </li>
            </ul>
          </div>

          {/* Contact & Support */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white mb-4">
              Farmer Support
            </h4>
            <div className="space-y-3 text-sm text-gray-400">
              <div className="flex items-start gap-2.5">
                <MapPin className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>Agricultural Extension Center, District Krishi Vigyan Kendra</span>
              </div>
              <div className="flex items-center gap-2.5">
                <Phone className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Kisan Call Center: 1800-180-1551</span>
              </div>
              <div className="flex items-center gap-2.5">
                <Mail className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>support@agrisaathi.org</span>
              </div>
            </div>
          </div>
        </div>

        {/* Disclaimer & Copyright */}
        <div className="pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-gray-500">
          <p>
            © {new Date().getFullYear()} AgriSaathi. All rights reserved. Built as a trustworthy agricultural advisory platform.
          </p>
          <div className="flex items-center gap-1 text-gray-500">
            <ShieldAlert className="w-3.5 h-3.5 text-amber-500" />
            <span>AI diagnostic advice is intended to support, not replace, certified agronomic field assessments.</span>
          </div>
        </div>
      </div>
    </footer>
  );
}


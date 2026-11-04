import React, { useState } from 'react';
import { Phone, Mail, MapPin, Send, CheckCircle2, ShieldCheck } from 'lucide-react';

export default function ContactPage() {
  const [submitted, setSubmitted] = useState(false);
  const [form, setForm] = useState({ name: '', email: '', phone: '', message: '', topic: 'disease' });

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
      <div className="text-center space-y-4">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          Extension Helpdesk
        </div>
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
          Connect with Agronomic Support
        </h1>
        <p className="text-base text-slate-600 max-w-xl mx-auto leading-relaxed">
          Need assistance with a challenging disease case or platform queries? Our Krishi Vigyan Kendra support team is here to assist.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-10">
        {/* Contact info column */}
        <div className="md:col-span-5 space-y-6">
          <div className="bg-slate-900 text-white p-8 rounded-3xl space-y-6">
            <h3 className="text-lg font-bold text-white">Direct Advisory Helplines</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Available Monday through Saturday, 9:00 AM to 6:00 PM for all registered farmers and agricultural stakeholders.
            </p>

            <div className="space-y-4 text-xs text-slate-300">
              <div className="flex items-start gap-3">
                <Phone className="w-5 h-5 text-emerald-400 shrink-0" />
                <div>
                  <div className="font-semibold text-white">Toll-Free Kisan Call Center</div>
                  <div>1800-180-1551 (Govt. of India)</div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Mail className="w-5 h-5 text-emerald-400 shrink-0" />
                <div>
                  <div className="font-semibold text-white">AgriSaathi Technical Desk</div>
                  <div>support@agrisaathi.org</div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-emerald-400 shrink-0" />
                <div>
                  <div className="font-semibold text-white">Extension Liaison Office</div>
                  <div>Krishi Vigyan Kendra, Central Research Complex, India</div>
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-800 flex items-center gap-2 text-xs text-emerald-400">
              <ShieldCheck className="w-4 h-4" />
              <span>Certified Agronomists On Duty</span>
            </div>
          </div>
        </div>

        {/* Message form */}
        <div className="md:col-span-7 bg-white p-8 rounded-3xl border border-slate-200 shadow-sm">
          {submitted ? (
            <div className="text-center py-12 space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">Inquiry Received</h3>
              <p className="text-sm text-slate-600 max-w-sm mx-auto">
                Thank you for contacting AgriSaathi. An agricultural extension specialist will review your request and follow up.
              </p>
              <button
                onClick={() => setSubmitted(false)}
                className="px-5 py-2.5 rounded-xl bg-emerald-600 text-white font-medium text-xs hover:bg-emerald-700 transition"
              >
                Send Another Note
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <h3 className="text-lg font-bold text-slate-900">Send an Advisory Request</h3>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Inquiry Topic</label>
                <select
                  value={form.topic}
                  onChange={(e) => setForm({ ...form, topic: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="disease">Plant Pathology & Leaf Disease Help</option>
                  <option value="crop">Crop Selection & Seasonal Advisory</option>
                  <option value="fertilizer">Fertilizer Application & Brand Verification</option>
                  <option value="technical">Technical Account Support</option>
                </select>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Your Full Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Ramesh Kumar"
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Phone Number</label>
                  <input
                    type="tel"
                    required
                    placeholder="e.g. 9876543210"
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
                <input
                  type="email"
                  required
                  placeholder="ramesh@example.com"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Message or Field Query</label>
                <textarea
                  rows="4"
                  required
                  placeholder="Describe your crop condition or questions in detail..."
                  value={form.message}
                  onChange={(e) => setForm({ ...form, message: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <button
                type="submit"
                className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-emerald-600 text-white font-semibold text-sm hover:bg-emerald-700 transition shadow-sm"
              >
                <Send className="w-4 h-4" />
                <span>Submit Query to Agricultural Desk</span>
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}


import React, { useState, useEffect } from 'react';
import {
  Microscope,
  Clock,
  CheckCircle2,
  AlertCircle,
  FileText,
  Send,
  Eye,
  RefreshCw,
  Leaf
} from 'lucide-react';
import { expertService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function ExpertDashboard() {
  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const [diagnosisForm, setDiagnosisForm] = useState({
    expert_diagnosis: '',
    expert_treatment: '',
    severity_assessment: 'Moderate',
  });

  const fetchCases = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await expertService.getPendingCases();
      setCases(data);
      if (data.length > 0 && !selectedCase) {
        setSelectedCase(data[0]);
      }
    } catch (err) {
      setError(err.message || 'Could not load expert cases queue.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCases();
  }, []);

  const handleSelectCase = (c) => {
    setSelectedCase(c);
    setSuccessMsg('');
    setDiagnosisForm({
      expert_diagnosis: c.expert_diagnosis || c.predicted_disease || '',
      expert_treatment: c.expert_treatment || '',
      severity_assessment: c.severity_assessment || 'Moderate',
    });
  };

  const handleSubmitDiagnosis = async (e) => {
    e.preventDefault();
    if (!selectedCase) return;

    setSubmitting(true);
    setError('');
    setSuccessMsg('');

    try {
      await expertService.submitReview(selectedCase.id, diagnosisForm);
      setSuccessMsg('Clinical diagnosis and prescription recorded successfully!');
      // Update local case record
      setCases(
        cases.map((c) =>
          c.id === selectedCase.id
            ? {
                ...c,
                status: 'reviewed',
                expert_diagnosis: diagnosisForm.expert_diagnosis,
                expert_treatment: diagnosisForm.expert_treatment,
              }
            : c
        )
      );
      setSelectedCase({
        ...selectedCase,
        status: 'reviewed',
        expert_diagnosis: diagnosisForm.expert_diagnosis,
        expert_treatment: diagnosisForm.expert_treatment,
      });
    } catch (err) {
      setError(err.message || 'Failed to submit expert review.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 text-emerald-400 text-xs font-bold uppercase tracking-wider border border-slate-700">
            <Microscope className="w-3.5 h-3.5" />
            <span>Krishi Vigyan Kendra Pathology Desk</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Agriculture Expert Verification Hub
          </h1>
          <p className="text-xs text-slate-400">
            Review incoming leaf pathology scans from farmers, confirm pathogens, and prescribe verified treatments.
          </p>
        </div>

        <button
          onClick={fetchCases}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Queue</span>
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-xs text-red-700 flex items-start gap-2">
          <AlertCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {successMsg && (
        <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-start gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
          <span>{successMsg}</span>
        </div>
      )}

      {loading ? (
        <LoadingSpinner message="Loading incoming diagnosis queue..." size="lg" />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Cases Queue (lg:col-span-5) */}
          <div className="lg:col-span-5 bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="font-bold text-slate-900 text-base">Incoming Scans Queue</h3>
              <span className="text-xs text-slate-500">{cases.length} cases</span>
            </div>

            <div className="space-y-3 max-h-[600px] overflow-y-auto pr-1">
              {cases.map((c) => {
                const isSelected = selectedCase?.id === c.id;
                return (
                  <div
                    key={c.id}
                    onClick={() => handleSelectCase(c)}
                    className={`cursor-pointer p-4 rounded-2xl border transition space-y-2 ${
                      isSelected
                        ? 'bg-emerald-50/70 border-emerald-500 shadow-xs'
                        : 'bg-white border-slate-200 hover:border-emerald-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-xs text-slate-900">
                        {c.crop_type || 'Crop Leaf'}
                      </span>
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                          c.status === 'reviewed'
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-amber-100 text-amber-800'
                        }`}
                      >
                        {c.status === 'reviewed' ? 'Verified' : 'Pending Review'}
                      </span>
                    </div>

                    <div className="text-xs text-slate-600 truncate">
                      {c.predicted_disease ? `AI: ${c.predicted_disease}` : 'AI Detection Pending'}
                    </div>

                    <div className="flex items-center justify-between text-[10px] text-slate-400 pt-1 border-t border-slate-100">
                      <span>Case ID: #{c.id?.slice(0, 8)}</span>
                      <span>{c.created_at ? new Date(c.created_at).toLocaleDateString() : 'Today'}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right Column: Case Inspection & Diagnosis Editor (lg:col-span-7) */}
          <div className="lg:col-span-7 space-y-6">
            {selectedCase ? (
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
                <div className="flex items-center justify-between pb-4 border-b border-slate-100">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">
                      Case Inspection
                    </span>
                    <h2 className="text-xl font-bold text-slate-900 mt-0.5">
                      {selectedCase.crop_type || 'Crop Leaf'} Sample #{selectedCase.id?.slice(0, 8)}
                    </h2>
                  </div>
                  <span
                    className={`text-xs px-3 py-1 rounded-full font-bold ${
                      selectedCase.status === 'reviewed'
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-amber-100 text-amber-800'
                    }`}
                  >
                    {selectedCase.status === 'reviewed' ? 'Review Complete' : 'Pending Diagnosis'}
                  </span>
                </div>

                {/* Leaf Image / AI Status Preview */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="rounded-2xl bg-slate-950 aspect-4/3 overflow-hidden flex items-center justify-center border border-slate-200">
                    {selectedCase.image_url ? (
                      <img
                        src={selectedCase.image_url}
                        alt="Scanned leaf"
                        className="w-full h-full object-contain"
                        onError={(e) => {
                          // Fallback graphic if static image is unavailable
                          e.target.style.display = 'none';
                        }}
                      />
                    ) : (
                      <Leaf className="w-12 h-12 text-emerald-500" />
                    )}
                  </div>

                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-3 text-xs">
                    <div className="font-bold text-slate-800">Automated Pipeline Data</div>
                    <div>
                      <span className="text-slate-400">Initial AI Prediction:</span>
                      <p className="font-semibold text-slate-900">
                        {selectedCase.predicted_disease || 'Model weights unconfigured in Phase 1'}
                      </p>
                    </div>
                    <div>
                      <span className="text-slate-400">Confidence Score:</span>
                      <p className="font-semibold text-slate-900">
                        {selectedCase.confidence_score ? `${selectedCase.confidence_score}%` : 'N/A'}
                      </p>
                    </div>
                    <div>
                      <span className="text-slate-400">Farmer Notes:</span>
                      <p className="text-slate-600 italic">
                        {selectedCase.notes || 'No additional notes provided by farmer.'}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Expert Diagnosis Form */}
                <form onSubmit={handleSubmitDiagnosis} className="space-y-4 pt-2 border-t border-slate-100">
                  <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <FileText className="w-4 h-4 text-emerald-600" />
                    <span>Agronomic Diagnosis & Prescription</span>
                  </h3>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Confirmed Pathogen / Disease Name
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. Early Blight (Alternaria solani)"
                      value={diagnosisForm.expert_diagnosis}
                      onChange={(e) =>
                        setDiagnosisForm({ ...diagnosisForm, expert_diagnosis: e.target.value })
                      }
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Pathological Severity
                    </label>
                    <select
                      value={diagnosisForm.severity_assessment}
                      onChange={(e) =>
                        setDiagnosisForm({ ...diagnosisForm, severity_assessment: e.target.value })
                      }
                      className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white font-medium"
                    >
                      <option value="Mild">Mild (Initial foliar spotting)</option>
                      <option value="Moderate">Moderate (Active spread across canopy)</option>
                      <option value="Severe">Severe (Necrosis & defoliation)</option>
                      <option value="Critical">Critical (Immediate systemic risk)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Prescribed Agronomic Treatment Plan
                    </label>
                    <textarea
                      rows="4"
                      required
                      placeholder="Specify chemical spray dosages (e.g. Mancozeb 75% WP @ 2g/L), organic remedies, and cultural practices..."
                      value={diagnosisForm.expert_treatment}
                      onChange={(e) =>
                        setDiagnosisForm({ ...diagnosisForm, expert_treatment: e.target.value })
                      }
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={submitting}
                    className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-emerald-600 text-white font-bold text-xs hover:bg-emerald-700 transition shadow-sm disabled:opacity-50"
                  >
                    <Send className="w-4 h-4" />
                    <span>{submitting ? 'Recording Diagnosis...' : 'Submit Certified Diagnosis to Farmer'}</span>
                  </button>
                </form>
              </div>
            ) : (
              <div className="bg-white rounded-3xl p-12 text-center text-slate-500 border border-slate-200">
                Select a case from the queue on the left to examine symptoms and submit diagnosis.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}


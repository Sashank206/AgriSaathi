import React, { useState, useRef } from 'react';
import {
  ScanEye,
  Upload,
  Camera,
  X,
  RefreshCw,
  AlertCircle,
  CheckCircle2,
  ShieldAlert,
  Info,
  Microscope,
  Leaf,
  Layers,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { diseaseService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function DiseaseDetectionPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [cropType, setCropType] = useState('All / Auto-Detect (Global AI)');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [expertReviewRequested, setExpertReviewRequested] = useState(false);
  const [expertReviewSubmitting, setExpertReviewSubmitting] = useState(false);

  const fileInputRef = useRef(null);
  const cameraInputRef = useRef(null);

  const cropOptions = [
    'All / Auto-Detect (Global AI)',
    'Tomato',
    'Potato',
    'Apple',
    'Corn (Maize)',
    'Grape',
    'Pepper (Bell)',
    'Orange',
    'Peach',
    'Strawberry',
    'Squash',
    'Cherry',
    'Soybean',
    'Blueberry',
    'Raspberry'
  ];

  const getRiskBadge = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'critical':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-red-100 text-red-800 border border-red-200">Severity: Critical</span>;
      case 'high':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-200">Severity: High</span>;
      case 'medium':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-yellow-100 text-yellow-800 border border-yellow-200">Severity: Medium</span>;
      default:
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">Severity: Normal</span>;
    }
  };

  const handleFileChange = (file) => {
    setError('');
    setResult(null);
    setExpertReviewRequested(false);

    if (!file) return;

    // Check size limit: 10 MB
    if (file.size > 10 * 1024 * 1024) {
      setError('File size exceeds the 10 MB limit. Please select a smaller image.');
      return;
    }

    // Check format
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setError('Invalid file format. Please upload JPG, PNG, or WEBP leaf images.');
      return;
    }

    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleRemoveImage = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setUploadProgress(0);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please choose or capture a plant leaf image first.');
      return;
    }

    setError('');
    setLoading(true);
    setUploadProgress(10);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('crop_type', cropType);

    try {
      const data = await diseaseService.predictDisease(formData, (progressEvent) => {
        if (progressEvent.total) {
          const percent = Math.round((progressEvent.loaded * 90) / progressEvent.total);
          setUploadProgress(percent);
        }
      });
      setUploadProgress(100);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Disease analysis request failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleRequestExpertReview = async () => {
    if (!result?.case_id) return;
    setExpertReviewSubmitting(true);
    try {
      await diseaseService.requestExpertReview(result.case_id);
      setExpertReviewRequested(true);
    } catch (err) {
      setError('Could not submit for expert review: ' + err.message);
    } finally {
      setExpertReviewSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Page Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          <ScanEye className="w-4 h-4 text-emerald-600" />
          <span>Primary Diagnostic Module</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          AI Plant Disease Detection & Treatment
        </h1>
        <p className="text-sm text-slate-600 max-w-2xl leading-relaxed">
          Upload or photograph an affected plant leaf. Our convolutional neural network architecture validates the foliage sample and maps observed symptoms to certified treatments.
        </p>
      </div>

      {/* Error alert */}
      {error && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 flex items-start gap-3 text-xs text-red-700">
          <AlertCircle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
          <div className="flex-1 font-medium">{error}</div>
        </div>
      )}

      {/* Main Workflow Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Upload & Configuration (lg:col-span-6) */}
        <div className="lg:col-span-6 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Upload className="w-5 h-5 text-emerald-600" />
            <span>Select Leaf Sample</span>
          </h2>

          {/* Crop selector */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              Crop Variety / Plant Type
            </label>
            <select
              value={cropType}
              onChange={(e) => setCropType(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white font-medium"
            >
              {cropOptions.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
            <p className="text-[11px] text-slate-400 mt-1">
              Selecting the crop family helps refine pathological boundary checks.
            </p>
          </div>

          {/* Upload Area / Preview */}
          {!previewUrl ? (
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              className="border-2 border-dashed border-emerald-300 rounded-3xl p-8 text-center bg-emerald-50/30 hover:bg-emerald-50/60 transition flex flex-col items-center justify-center space-y-4 cursor-pointer"
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="w-16 h-16 rounded-2xl bg-white shadow-sm border border-emerald-100 flex items-center justify-center text-emerald-600">
                <Leaf className="w-8 h-8" />
              </div>
              <div className="space-y-1">
                <div className="text-sm font-bold text-slate-800">
                  Drag & drop leaf photo here, or browse files
                </div>
                <div className="text-xs text-slate-500">Supports JPG, PNG, WEBP up to 10 MB</div>
              </div>

              {/* Action buttons */}
              <div className="flex flex-wrap items-center gap-3 pt-2" onClick={(e) => e.stopPropagation()}>
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="px-4 py-2 rounded-xl bg-emerald-600 text-white font-medium text-xs hover:bg-emerald-700 shadow-xs transition flex items-center gap-1.5"
                >
                  <Upload className="w-4 h-4" />
                  <span>Browse Device</span>
                </button>

                <button
                  type="button"
                  onClick={() => cameraInputRef.current?.click()}
                  className="px-4 py-2 rounded-xl bg-white text-slate-700 font-medium text-xs border border-slate-300 hover:bg-slate-50 transition flex items-center gap-1.5"
                >
                  <Camera className="w-4 h-4 text-emerald-600" />
                  <span>Take Live Photo</span>
                </button>
              </div>

              {/* Hidden inputs */}
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                className="hidden"
                onChange={(e) => e.target.files && handleFileChange(e.target.files[0])}
              />
              <input
                ref={cameraInputRef}
                type="file"
                accept="image/*"
                capture="environment"
                className="hidden"
                onChange={(e) => e.target.files && handleFileChange(e.target.files[0])}
              />
            </div>
          ) : (
            <div className="space-y-4">
              <div className="relative rounded-2xl overflow-hidden border border-slate-200 bg-slate-900 flex items-center justify-center aspect-4/3">
                <img
                  src={previewUrl}
                  alt="Leaf preview"
                  className="w-full h-full object-contain"
                />
                <button
                  onClick={handleRemoveImage}
                  className="absolute top-3 right-3 p-2 rounded-full bg-slate-900/80 text-white hover:bg-red-600 transition shadow-sm"
                  title="Remove image"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div className="flex items-center justify-between text-xs text-slate-500">
                <span>Selected: {selectedFile?.name}</span>
                <span>{(selectedFile?.size / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
            </div>
          )}

          {/* Analyze CTA */}
          <button
            onClick={handleAnalyze}
            disabled={!selectedFile || loading}
            className="w-full inline-flex items-center justify-center gap-2 py-3.5 rounded-2xl bg-emerald-600 text-white font-bold text-sm hover:bg-emerald-700 transition shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center gap-2">
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Running Diagnostic Pipeline...</span>
              </div>
            ) : (
              <>
                <ScanEye className="w-5 h-5" />
                <span>Analyze Leaf Sample</span>
              </>
            )}
          </button>

          {/* Upload progress */}
          {loading && uploadProgress > 0 && (
            <div className="space-y-1.5 pt-1">
              <div className="flex justify-between text-[11px] font-semibold text-slate-600">
                <span>Processing leaf image...</span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
                <div
                  className="h-full bg-emerald-600 transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Diagnostic Results (lg:col-span-6) */}
        <div className="lg:col-span-6 space-y-6">
          {!result && !loading && (
            <div className="bg-white rounded-3xl p-8 sm:p-12 border border-slate-200 shadow-sm text-center space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto">
                <ScanEye className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-bold text-slate-800">No Image Analyzed Yet</h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto leading-relaxed">
                Upload or capture a leaf photo on the left and click "Analyze Leaf Sample" to see disease diagnostics and treatment guidance here.
              </p>
            </div>
          )}

          {loading && (
            <div className="bg-white rounded-3xl p-12 border border-slate-200 shadow-sm text-center space-y-4">
              <LoadingSpinner message="Validating leaf resolution and extracting pathology features..." size="lg" />
            </div>
          )}

          {result && !loading && (
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
              {/* Result Status Header */}
              <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="w-11 h-11 rounded-2xl bg-emerald-600 text-white flex items-center justify-center shadow-xs">
                    <Microscope className="w-6 h-6" />
                  </div>
                  <div>
                    <div className="text-xs font-bold uppercase tracking-wider text-slate-400">Pathology Diagnosis</div>
                    <div className="text-lg font-extrabold text-slate-900">{result.plant_name}</div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {getRiskBadge(result.risk_level)}
                  {result.model_configured ? (
                    <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                      {result.confidence_score}% Confidence
                    </span>
                  ) : (
                    <span className="px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
                      Phase 1 (40% Milestone)
                    </span>
                  )}
                </div>
              </div>

              {/* Trained Model Active Banner */}
              {result.model_configured && (
                <div className="px-3.5 py-2 rounded-xl bg-emerald-50/70 border border-emerald-100 flex items-center justify-between text-xs text-emerald-900">
                  <span className="flex items-center gap-2 font-semibold">
                    <Sparkles className="w-4 h-4 text-emerald-600" />
                    <span>Trained CNN Deep Learning Pipeline (38 Disease Classes across 14 Crop Types)</span>
                  </span>
                  <span className="font-bold text-[11px] text-emerald-700 uppercase">Live Model</span>
                </div>
              )}

              {/* Truthful Model Notice (Part F Rule) */}
              {!result.model_configured && (
                <div className="p-4 rounded-2xl bg-blue-50/70 border border-blue-200 space-y-2 text-xs text-blue-900">
                  <div className="flex items-center gap-2 font-bold text-blue-950">
                    <Info className="w-4 h-4 text-blue-600 shrink-0" />
                    <span>Image Validated • AI CNN Weights Interface Active</span>
                  </div>
                  <p className="leading-relaxed text-blue-900/90">
                    {result.message}
                  </p>
                </div>
              )}

              {/* If model has predictions or knowledge-base details */}
              {result.predicted_disease ? (
                <div className="space-y-5">
                  {/* Pathogen / Healthy Diagnosis Banner */}
                  <div className={`p-5 rounded-2xl border ${
                    result.predicted_disease.toLowerCase().includes('healthy')
                      ? 'bg-emerald-50 border-emerald-200 text-emerald-950'
                      : 'bg-red-50/50 border-red-200 text-red-950'
                  }`}>
                    <div className="flex items-center justify-between">
                      <div className="text-xs font-bold uppercase tracking-wider text-slate-600">
                        {result.predicted_disease.toLowerCase().includes('healthy') ? 'Foliage Condition' : 'Identified Pathogen'}
                      </div>
                      <div className="text-xs font-semibold text-slate-500">
                        Certainty: <span className="font-bold text-slate-900">{result.confidence_score}%</span>
                      </div>
                    </div>
                    <div className="text-xl font-extrabold text-slate-900 mt-1 flex items-center gap-2">
                      {result.predicted_disease.toLowerCase().includes('healthy') ? (
                        <CheckCircle2 className="w-6 h-6 text-emerald-600 shrink-0" />
                      ) : (
                        <ShieldAlert className="w-6 h-6 text-red-600 shrink-0" />
                      )}
                      <span>{result.predicted_disease}</span>
                    </div>
                    {result.disease_description && (
                      <p className="text-xs text-slate-600 mt-2.5 leading-relaxed">
                        {result.disease_description}
                      </p>
                    )}
                  </div>

                  {/* Diagnostic Probability Distribution Breakdown */}
                  {result.top_predictions && result.top_predictions.length > 0 && (
                    <div className="space-y-3 p-4 rounded-2xl bg-slate-50 border border-slate-200/80">
                      <div className="flex items-center justify-between text-xs font-bold text-slate-800">
                        <span className="flex items-center gap-1.5">
                          <Layers className="w-4 h-4 text-emerald-600" />
                          <span>Candidate Diagnosis Probabilities</span>
                        </span>
                        <span className="text-[11px] text-slate-400 font-normal">Confidence Scores</span>
                      </div>
                      <div className="space-y-2 pt-1">
                        {result.top_predictions.map((pred, idx) => (
                          <div key={idx} className="space-y-1">
                            <div className="flex justify-between text-xs font-medium">
                              <span className="flex items-center gap-1.5 truncate max-w-[260px] sm:max-w-xs">
                                <span className={`w-2 h-2 rounded-full shrink-0 ${
                                  pred.is_healthy ? 'bg-emerald-500' : idx === 0 ? 'bg-emerald-600' : 'bg-slate-400'
                                }`} />
                                <span className={idx === 0 ? 'font-bold text-slate-900' : 'text-slate-600'}>
                                  {pred.condition}
                                </span>
                              </span>
                              <span className={`font-mono text-xs ${idx === 0 ? 'font-bold text-emerald-700' : 'text-slate-500'}`}>
                                {pred.confidence_percentage}%
                              </span>
                            </div>
                            <div className="w-full h-2 rounded-full bg-slate-200 overflow-hidden">
                              <div
                                className={`h-full rounded-full transition-all duration-500 ${
                                  pred.is_healthy ? 'bg-emerald-500' : idx === 0 ? 'bg-emerald-600' : 'bg-slate-400'
                                }`}
                                style={{ width: `${Math.max(pred.confidence_percentage, 2)}%` }}
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Symptoms */}
                  {result.visible_symptoms && result.visible_symptoms.length > 0 && (
                    <div className="space-y-2.5">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                        <Leaf className="w-4 h-4 text-emerald-600" />
                        <span>Characteristic Foliage Symptoms</span>
                      </h4>
                      <div className="space-y-1.5">
                        {result.visible_symptoms.map((sym, idx) => (
                          <div key={idx} className="flex items-start gap-2.5 text-xs text-slate-700 bg-slate-50/60 p-2.5 rounded-xl border border-slate-100">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-1.5 shrink-0" />
                            <span>{sym}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Treatment recommendations */}
                  {result.treatment_recommendations && result.treatment_recommendations.length > 0 && (
                    <div className="space-y-2.5">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                        <span>Recommended Agronomic Treatments & Bio-controls</span>
                      </h4>
                      <div className="space-y-2">
                        {result.treatment_recommendations.map((t, idx) => (
                          <div
                            key={idx}
                            className="p-3 rounded-xl bg-emerald-50/40 border border-emerald-100 text-xs text-slate-800 flex items-start gap-2.5"
                          >
                            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                            <span className="leading-relaxed">{t}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Preventive measures */}
                  {result.preventive_measures && result.preventive_measures.length > 0 && (
                    <div className="space-y-2.5">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                        <Sparkles className="w-4 h-4 text-blue-600" />
                        <span>Preventive Cultural Practices (Field Hygiene)</span>
                      </h4>
                      <div className="space-y-1.5">
                        {result.preventive_measures.map((p, idx) => (
                          <div key={idx} className="flex items-start gap-2.5 text-xs text-slate-700 bg-blue-50/30 p-2.5 rounded-xl border border-blue-100">
                            <span className="w-1.5 h-1.5 rounded-full bg-blue-600 mt-1.5 shrink-0" />
                            <span className="leading-relaxed">{p}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : null}

              {/* Expert Review Option (Required by Part F & K) */}
              <div className="pt-4 border-t border-slate-100 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <div className="text-xs font-bold text-slate-900">Need Clinical Extension Verification?</div>
                    <div className="text-[11px] text-slate-500">
                      Submit this scan directly to the Agriculture Expert queue.
                    </div>
                  </div>
                  {expertReviewRequested ? (
                    <span className="inline-flex items-center gap-1 px-3 py-1.5 rounded-xl bg-emerald-100 text-emerald-800 text-xs font-bold">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                      <span>Case In Expert Queue</span>
                    </span>
                  ) : (
                    <button
                      onClick={handleRequestExpertReview}
                      disabled={expertReviewSubmitting}
                      className="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 transition disabled:opacity-50"
                    >
                      {expertReviewSubmitting ? 'Routing Case...' : 'Request Expert Review'}
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


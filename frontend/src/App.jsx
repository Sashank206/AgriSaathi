import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

// Layouts
import PublicLayout from './layouts/PublicLayout';
import DashboardLayout from './layouts/DashboardLayout';

// Public Pages
import LandingPage from './pages/LandingPage';
import AboutPage from './pages/AboutPage';
import FeaturesPage from './pages/FeaturesPage';
import HowItWorksPage from './pages/HowItWorksPage';
import ContactPage from './pages/ContactPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

// Feature Pages
import DiseaseDetectionPage from './pages/DiseaseDetectionPage';
import CropRecommendationPage from './pages/CropRecommendationPage';
import FertilizerComparisonPage from './pages/FertilizerComparisonPage';
import WeatherPage from './pages/WeatherPage';

// Role Dashboards
import FarmerDashboard from './dashboards/FarmerDashboard';
import AdminDashboard from './dashboards/AdminDashboard';
import ExpertDashboard from './dashboards/ExpertDashboard';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Marketing & Informational Routes */}
          <Route element={<PublicLayout />}>
            <Route path="/" element={<LandingPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/features" element={<FeaturesPage />} />
            <Route path="/how-it-works" element={<HowItWorksPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Route>

          {/* Farmer & Shared Agronomic Modules */}
          <Route
            element={<DashboardLayout allowedRoles={['farmer', 'admin', 'expert']} />}
          >
            <Route path="/farmer" element={<FarmerDashboard />} />
            <Route path="/disease-detection" element={<DiseaseDetectionPage />} />
            <Route path="/crop-recommendation" element={<CropRecommendationPage />} />
            <Route path="/fertilizer-comparison" element={<FertilizerComparisonPage />} />
            <Route path="/weather-monitoring" element={<WeatherPage />} />
          </Route>

          {/* Admin Operations */}
          <Route element={<DashboardLayout allowedRoles={['admin']} />}>
            <Route path="/admin" element={<AdminDashboard />} />
          </Route>

          {/* Agriculture Expert Review Hub */}
          <Route element={<DashboardLayout allowedRoles={['expert', 'admin']} />}>
            <Route path="/expert" element={<ExpertDashboard />} />
          </Route>

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

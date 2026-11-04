import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Attach JWT access token to every outgoing request if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('agrisaathi_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for clear error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if expired/tampered
      localStorage.removeItem('agrisaathi_token');
      localStorage.removeItem('agrisaathi_user');
    }
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected network error occurred.';
    return Promise.reject(new Error(message));
  }
);

export const authService = {
  login: async (credentials) => {
    const res = await apiClient.post('/auth/login', credentials);
    return res.data;
  },
  register: async (userData) => {
    const res = await apiClient.post('/auth/register', userData);
    return res.data;
  },
  getMe: async () => {
    const res = await apiClient.get('/auth/me');
    return res.data;
  },
};

export const diseaseService = {
  predictDisease: async (formData, onUploadProgress) => {
    const res = await apiClient.post('/disease/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress,
    });
    return res.data;
  },
  getMyCases: async () => {
    const res = await apiClient.get('/disease/cases');
    return res.data;
  },
  getKnowledgeBase: async () => {
    const res = await apiClient.get('/disease/knowledge');
    return res.data;
  },
  requestExpertReview: async (caseId) => {
    const res = await apiClient.post(`/disease/cases/${caseId}/request-review`);
    return res.data;
  },
};

export const cropService = {
  recommend: async (payload) => {
    const res = await apiClient.post('/crop/recommend', payload);
    return res.data;
  },
  getHistory: async () => {
    const res = await apiClient.get('/crop/history');
    return res.data;
  },
};

export const fertilizerService = {
  getAll: async (params) => {
    const res = await apiClient.get('/fertilizers', { params });
    return res.data;
  },
  getById: async (id) => {
    const res = await apiClient.get(`/fertilizers/${id}`);
    return res.data;
  },
  compare: async (payload) => {
    const res = await apiClient.post('/fertilizers/compare', payload);
    return res.data;
  },
};

export const weatherService = {
  getCurrent: async (params) => {
    const res = await apiClient.get('/weather/current', { params });
    return res.data;
  },
  getForecast: async (params) => {
    const res = await apiClient.get('/weather/forecast', { params });
    return res.data;
  },
};

export const adminService = {
  getStats: async () => {
    const res = await apiClient.get('/admin/stats');
    return res.data;
  },
  getUsers: async () => {
    const res = await apiClient.get('/admin/users');
    return res.data;
  },
  addFertilizer: async (data) => {
    const res = await apiClient.post('/admin/fertilizers', data);
    return res.data;
  },
  deleteFertilizer: async (id) => {
    const res = await apiClient.delete(`/admin/fertilizers/${id}`);
    return res.data;
  },
};

export const expertService = {
  getPendingCases: async () => {
    const res = await apiClient.get('/expert/pending-cases');
    return res.data;
  },
  submitReview: async (caseId, payload) => {
    const res = await apiClient.post(`/expert/cases/${caseId}/review`, payload);
    return res.data;
  },
};

export default apiClient;


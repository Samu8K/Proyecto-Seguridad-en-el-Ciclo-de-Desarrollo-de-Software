import axios from 'axios';

// Usar la URL base configurada en Vite o ruta relativa
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 segundos timeout
});

// Add request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Log de desarrollo
    if (import.meta.env.DEV) {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('[API] Unauthorized access');
    } else if (error.response?.status === 404) {
      console.warn('[API] Resource not found');
    } else if (error.code === 'ECONNREFUSED' || error.message.includes('ENOTFOUND')) {
      console.error('[API] Cannot connect to backend. Make sure backend is running.');
    }
    return Promise.reject(error);
  }
);

export default apiClient;

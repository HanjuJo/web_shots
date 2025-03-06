import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  timeout: 10000
});

// Request interceptor for API calls
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const toolService = {
  // Get all tool combinations with optional filtering/pagination
  async getAllToolCombinations(params = {}) {
    try {
      const response = await api.get('/tools/combinations', { params });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Get a specific tool combination by ID
  async getToolCombination(id) {
    try {
      const response = await api.get(`/tools/combinations/${id}`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Get user's personal tool combinations
  async getUserToolCombinations() {
    try {
      const response = await api.get('/tools/my-combinations');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Create a new tool combination
  async createToolCombination(data) {
    try {
      const response = await api.post('/tools/combinations/create', data);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Update an existing tool combination
  async updateToolCombination(id, data) {
    try {
      const response = await api.put(`/tools/combinations/edit/${id}`, data);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Delete a tool combination
  async deleteToolCombination(id) {
    try {
      await api.delete(`/tools/combinations/${id}`);
      return true;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Error handling utility
  handleError(error) {
    if (error.response) {
      // Server responded with a status code outside of 2xx range
      return {
        status: error.response.status,
        message: error.response.data.message || '서버 오류가 발생했습니다.'
      };
    } else if (error.request) {
      // Request was made but no response received
      return {
        status: 0,
        message: '서버에 연결할 수 없습니다.'
      };
    } else {
      // Error occurred while setting up the request
      return {
        status: 0,
        message: '요청을 처리할 수 없습니다.'
      };
    }
  }
};

export default toolService;

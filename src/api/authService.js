import axios from 'axios';

const API_URL = 'http://localhost:5003';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 30000, // 30 seconds timeout
  withCredentials: true,
  validateStatus: function (status) {
    return status >= 200 && status < 500;
  }
});

// Add JWT token to all requests
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

const authService = {
  async login(email, password) {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, { email, password });
      const { token, user } = response.data;
      if (token) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      }
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error.response?.data?.message || '로그인 중 오류가 발생했습니다';
    }
  },



  async register(userData) {
    try {
      const response = await apiClient.post('/auth/register', userData);
      
      if (!response.data || !response.data.success) {
        throw new Error(response.data?.message || '회원가입에 실패했습니다');
      }
      
      const { token, user } = response.data;
      if (token) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      }
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      if (error.response) {
        // Server responded with error
        throw new Error(error.response.data?.message || '서버에서 오류가 발생했습니다');
      } else if (error.request) {
        // Request made but no response
        throw new Error('서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요.');
      } else {
        // Error in request setup
        throw new Error('요청을 보내는 중 오류가 발생했습니다');
      }
    }
  },

  async refreshToken() {
    const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
  }
};

export default authService;

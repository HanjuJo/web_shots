import authService from '@/api/authService';

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    error: null,
    loading: false
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    },
    SET_USER(state, user) {
      state.user = user;
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
      } else {
        localStorage.removeItem('user');
      }
    },
    SET_ERROR(state, error) {
      state.error = error;
    },
    SET_LOADING(state, loading) {
      state.loading = loading;
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        commit('SET_LOADING', true);
        commit('SET_ERROR', null);
        const response = await authService.login(credentials.email, credentials.password);
        commit('SET_TOKEN', response.token);
        commit('SET_USER', response.user);
        return response;
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || '로그인에 실패했습니다');
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    async register({ commit }, userData) {
      try {
        commit('SET_LOADING', true);
        commit('SET_ERROR', null);
        
        // Validate input data
        if (!userData.username || !userData.email || !userData.password) {
          throw new Error('모든 필드를 입력해주세요');
        }
        
        if (userData.password.length < 6) {
          throw new Error('비밀번호는 최소 6자 이상이어야 합니다');
        }
        
        const response = await authService.register(userData);
        
        if (response.success) {
          commit('SET_TOKEN', response.token);
          commit('SET_USER', response.user);
          commit('SET_ERROR', null);
          return response;
        } else {
          throw new Error(response.message || '회원가입에 실패했습니다');
        }
      } catch (error) {
        const errorMessage = error.message || error.response?.data?.message || '회원가입 중 오류가 발생했습니다';
        commit('SET_ERROR', errorMessage);
        throw new Error(errorMessage);
      } finally {
        commit('SET_LOADING', false);
      }
    },


    logout({ commit }) {
      authService.logout();
      commit('SET_TOKEN', null);
      commit('SET_USER', null);
      commit('SET_ERROR', null);
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    currentUser: state => state.user,
    error: state => state.error,
    loading: state => state.loading
  }
}

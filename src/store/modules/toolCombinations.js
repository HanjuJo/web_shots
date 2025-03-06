import axios from 'axios';

const state = {
  combinations: [],
  currentCombination: null,
  loading: false,
  error: null,
  searchQuery: '',
  selectedCategory: '',
  categories: [
    { id: 'video', name: '비디오' },
    { id: 'text', name: '텍스트' },
    { id: 'image', name: '이미지' },
    { id: 'audio', name: '오디오' },
    { id: 'translation', name: '번역' },
    { id: 'analysis', name: '분석' }
  ]
};

const mutations = {
  SET_COMBINATIONS(state, combinations) {
    state.combinations = combinations;
  },
  SET_CURRENT_COMBINATION(state, combination) {
    state.currentCombination = combination;
  },
  SET_LOADING(state, loading) {
    state.loading = loading;
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
  SET_SEARCH_QUERY(state, query) {
    state.searchQuery = query;
  },
  SET_SELECTED_CATEGORY(state, category) {
    state.selectedCategory = category;
  },
  ADD_COMBINATION(state, combination) {
    state.combinations.push(combination);
  },
  UPDATE_COMBINATION(state, updatedCombination) {
    const index = state.combinations.findIndex(c => c.id === updatedCombination.id);
    if (index !== -1) {
      state.combinations.splice(index, 1, updatedCombination);
    }
  },
  DELETE_COMBINATION(state, id) {
    state.combinations = state.combinations.filter(c => c.id !== id);
  },
  CLEAR_ERROR(state) {
    state.error = null;
  }
};

const actions = {
  async fetchCombinations({ commit }, userId) {
    commit('SET_LOADING', true);
    try {
      const response = await axios.get(`/api/tools/combinations?user_id=${userId}`);
      commit('SET_COMBINATIONS', response.data.combinations);
    } catch (error) {
      commit('SET_ERROR', error.message);
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async fetchCombination({ commit }, { id }) {
    commit('SET_LOADING', true);
    try {
      const response = await axios.get(`/api/tools/combinations/${id}`);
      commit('SET_CURRENT_COMBINATION', response.data.combination);
    } catch (error) {
      commit('SET_ERROR', error.message);
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async createCombination({ commit }, combination) {
    commit('SET_LOADING', true);
    try {
      const response = await axios.post('/api/tools/combinations', combination);
      if (response.data.success) {
        commit('ADD_COMBINATION', { ...combination, id: response.data.id });
      }
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message);
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async updateCombination({ commit }, { id, combination }) {
    commit('SET_LOADING', true);
    try {
      const response = await axios.put(`/api/tools/combinations/${id}`, combination);
      if (response.data.success) {
        commit('UPDATE_COMBINATION', { ...combination, id });
      }
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message);
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async deleteCombination({ commit }, { id, userId }) {
    commit('SET_LOADING', true);
    try {
      const response = await axios.delete(`/api/tools/combinations/${id}?user_id=${userId}`);
      if (response.data.success) {
        commit('DELETE_COMBINATION', id);
      }
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message);
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  }
};

const getters = {
  getCombinationById: state => id => {
    return state.combinations.find(c => c.id === id);
  },
  getUserCombinations: state => userId => {
    return state.combinations.filter(c => c.user_id === userId);
  },
  getPublicCombinations: state => {
    return state.combinations.filter(c => c.is_public);
  },
  filteredCombinations: state => {
    return state.combinations.filter(combination => {
      const matchesSearch = state.searchQuery === '' ||
        combination.name.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
        combination.description.toLowerCase().includes(state.searchQuery.toLowerCase());
      
      const matchesCategory = state.selectedCategory === '' ||
        combination.content_type === state.selectedCategory;
      
      return matchesSearch && matchesCategory;
    });
  },
  categories: state => state.categories
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

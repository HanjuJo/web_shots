import { createStore } from 'vuex'
import axios from 'axios'
import auth from './modules/auth'
import tools from './modules/tools'
import toolCombinations from './modules/toolCombinations'

const store = createStore({
  modules: {
    auth,
    tools,
    toolCombinations
  },
  state: {
    trendingVideos: [],
    channelStats: null,
    loading: false,
    error: null
  },
  mutations: {
    SET_TRENDING_VIDEOS(state, videos) {
      state.trendingVideos = videos
    },
    SET_CHANNEL_STATS(state, stats) {
      state.channelStats = stats
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    },

  },
  actions: {
    async fetchTrendingVideos({ commit }) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await axios.get('/api/trends')
        console.log('Trends API response:', response)
        
        if (response.data && response.data.success) {
          commit('SET_TRENDING_VIDEOS', response.data.trends)
        } else {
          throw new Error(response.data?.error || 'Failed to fetch trending videos')
        }
      } catch (error) {
        console.error('Error in fetchTrendingVideos:', error)
        if (error.response) {
          commit('SET_ERROR', `서버 오류 (${error.response.status}): ${error.response.data?.error || error.message}`)
        } else if (error.request) {
          commit('SET_ERROR', '서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인해주세요.')
        } else {
          commit('SET_ERROR', `요청 오류: ${error.message}`)
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async analyzeChannel({ commit }, channelId) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await axios.post('/api/channel/analyze', { channelId })
        console.log('Channel API response:', response)
        
        if (response.data && response.data.success) {
          commit('SET_CHANNEL_STATS', response.data.analysis)
        } else {
          throw new Error(response.data?.error || 'Failed to analyze channel')
        }
      } catch (error) {
        console.error('Error in analyzeChannel:', error)
        if (error.response) {
          commit('SET_ERROR', `서버 오류 (${error.response.status}): ${error.response.data?.error || error.message}`)
        } else if (error.request) {
          commit('SET_ERROR', '서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인해주세요.')
        } else {
          commit('SET_ERROR', `요청 오류: ${error.message}`)
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },

        

  },
  getters: {
    isLoading: state => state.loading,
    getError: state => state.error,
    getTrendingVideos: state => state.trendingVideos,
    getChannelStats: state => state.channelStats,

  }
})

export default store

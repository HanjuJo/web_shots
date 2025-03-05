import { createStore } from 'vuex'
import axios from 'axios'
import auth from './modules/auth'

const store = createStore({
  modules: {
    auth
  },
  state: {
    trendingVideos: [],
    channelStats: null,
    loading: false,
    error: null,
    toolCombinations: [],
    userToolCombinations: []
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
    SET_TOOL_COMBINATIONS(state, combinations) {
      state.toolCombinations = combinations
    },
    SET_USER_TOOL_COMBINATIONS(state, combinations) {
      state.userToolCombinations = combinations
    },
    ADD_USER_TOOL_COMBINATION(state, combination) {
      state.userToolCombinations.push(combination)
    },
    UPDATE_USER_TOOL_COMBINATION(state, { id, updatedCombination }) {
      const index = state.userToolCombinations.findIndex(c => c.id === id)
      if (index !== -1) {
        state.userToolCombinations.splice(index, 1, updatedCombination)
      }
    },
    DELETE_USER_TOOL_COMBINATION(state, id) {
      state.userToolCombinations = state.userToolCombinations.filter(c => c.id !== id)
    }
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
    async fetchToolCombinations({ commit }) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const dummyCombinations = [
          {
            id: 1,
            name: '유튜브 콘텐츠 제작 세트',
            description: '유튜브 영상 제작을 위한 AI 도구 모음',
            contentType: '유튜브',
            creator: '관리자',
            toolIds: [3, 5, 6], 
            isPublic: true,
            usageCount: 1245,
            createdAt: '2023-09-15T12:00:00Z'
          },
          {
            id: 2,
            name: '블로그 콘텐츠 제작 세트',
            description: '블로그 콘텐츠 제작을 위한 AI 도구 모음',
            contentType: '블로그',
            creator: '관리자',
            toolIds: [1, 4], 
            isPublic: true,
            usageCount: 987,
            createdAt: '2023-10-05T09:30:00Z'
          },
          {
            id: 3,
            name: '소셜 미디어 콘텐츠 세트',
            description: '인스타그램, 페이스북 등의 소셜 미디어용 콘텐츠 제작 도구',
            contentType: '소셜 미디어',
            creator: '관리자',
            toolIds: [1, 2, 4], 
            isPublic: true,
            usageCount: 1587,
            createdAt: '2023-11-20T15:45:00Z'
          }
        ]
        
        setTimeout(() => {
          commit('SET_TOOL_COMBINATIONS', dummyCombinations)
          commit('SET_LOADING', false)
        }, 300)
      } catch (error) {
        console.error('Error in fetchToolCombinations:', error)
        commit('SET_ERROR', `도구 조합을 불러오는 중 오류가 발생했습니다: ${error.message}`)
        commit('SET_LOADING', false)
      }
    },
    async fetchUserToolCombinations({ commit }) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const dummyUserCombinations = [
          {
            id: 101,
            name: '내 유튜브 브이로그 도구 세트',
            description: '브이로그 제작에 최적화된 나만의 도구 모음',
            contentType: '유튜브',
            toolIds: [3, 6], 
            isPublic: false,
            createdAt: '2024-01-10T14:22:00Z',
            lastUsed: '2024-02-28T09:15:00Z'
          },
          {
            id: 102,
            name: '내 인스타그램 리뷰 도구 세트',
            description: '제품 리뷰용 인스타그램 콘텐츠 제작 도구',
            contentType: '소셜 미디어',
            toolIds: [1, 4], 
            isPublic: false,
            createdAt: '2024-02-05T11:30:00Z',
            lastUsed: '2024-03-01T16:45:00Z'
          }
        ]
        
        setTimeout(() => {
          commit('SET_USER_TOOL_COMBINATIONS', dummyUserCombinations)
          commit('SET_LOADING', false)
        }, 300)
      } catch (error) {
        console.error('Error in fetchUserToolCombinations:', error)
        commit('SET_ERROR', `내 도구 조합을 불러오는 중 오류가 발생했습니다: ${error.message}`)
        commit('SET_LOADING', false)
      }
    },
    async saveToolCombination({ commit }, combination) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const newCombination = {
          ...combination,
          id: Date.now(), 
          createdAt: new Date().toISOString(),
          lastUsed: new Date().toISOString()
        }
        
        setTimeout(() => {
          commit('ADD_USER_TOOL_COMBINATION', newCombination)
          commit('SET_LOADING', false)
        }, 300)
        
        return newCombination
      } catch (error) {
        console.error('Error in saveToolCombination:', error)
        commit('SET_ERROR', `도구 조합을 저장하는 중 오류가 발생했습니다: ${error.message}`)
        commit('SET_LOADING', false)
        throw error
      }
    },
    async updateToolCombination({ commit }, { id, updatedCombination }) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        setTimeout(() => {
          commit('UPDATE_USER_TOOL_COMBINATION', { 
            id, 
            updatedCombination: {
              ...updatedCombination,
              lastUsed: new Date().toISOString()
            } 
          })
          commit('SET_LOADING', false)
        }, 300)
      } catch (error) {
        console.error('Error in updateToolCombination:', error)
        commit('SET_ERROR', `도구 조합을 업데이트하는 중 오류가 발생했습니다: ${error.message}`)
        commit('SET_LOADING', false)
        throw error
      }
    },
    async deleteToolCombination({ commit }, id) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        setTimeout(() => {
          commit('DELETE_USER_TOOL_COMBINATION', id)
          commit('SET_LOADING', false)
        }, 300)
      } catch (error) {
        console.error('Error in deleteToolCombination:', error)
        commit('SET_ERROR', `도구 조합을 삭제하는 중 오류가 발생했습니다: ${error.message}`)
        commit('SET_LOADING', false)
        throw error
      }
    }
  },
  getters: {
    isLoading: state => state.loading,
    getError: state => state.error,
    getTrendingVideos: state => state.trendingVideos,
    getChannelStats: state => state.channelStats,
    getToolCombinations: state => state.toolCombinations,
    getUserToolCombinations: state => state.userToolCombinations
  }
})

export default store

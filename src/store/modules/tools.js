import toolService from '@/api/toolService';

export default {
  namespaced: true,

  state: {
    // 워크플로우 상태
    workflowHistory: [],
    selectedTool: null,
    workflowSettings: {
      autoLayout: true,
      snapToGrid: true,
      gridSize: 15,
      connectionType: 'smoothstep'
    },
    toolCombinations: [
      {
        id: 1,
        name: '유튜버 콘텐츠 제작 세트',
        description: '유튜버를 위한 영상, 썸네일, 자막 자동화 도구 조합',
        contentType: '유튜브',
        toolIds: [2, 3, 6],
        creator: '에이이허브',
        usageCount: 1200,
        isPublic: true
      },
      {
        id: 2,
        name: '블로그 콘텐츠 제작 세트',
        description: '블로그 글쓰기와 이미지 생성을 위한 도구 조합',
        contentType: '블로그',
        toolIds: [1, 2, 5],
        creator: '에이이허브',
        usageCount: 850,
        isPublic: true
      },
      {
        id: 3,
        name: '소셜 미디어 콘텐츠 세트',
        description: '인스타그램, 트위터를 위한 이미지와 영상 제작 도구 조합',
        contentType: '소셜 미디어',
        toolIds: [2, 3, 4],
        creator: '에이이허브',
        usageCount: 650,
        isPublic: true
      }
    ],
    currentToolCombination: null,
    userToolCombinations: [],
    availableTools: [
      { id: 1, name: 'Text Generator', type: 'text', category: 'generation' },
      { id: 2, name: 'Image Generator', type: 'image', category: 'generation' },
      { id: 3, name: 'Video Editor', type: 'video', category: 'editing' },
      { id: 4, name: 'Audio Enhancer', type: 'audio', category: 'enhancement' },
      { id: 5, name: 'Translation Tool', type: 'text', category: 'language' },
      { id: 6, name: 'Voice Synthesizer', type: 'audio', category: 'generation' }
    ],
    workflowTools: [],
    workflowConnections: [],
    loading: false,
    error: null
  },

  mutations: {
    // 워크플로우 히스토리 관리
    ADD_TO_HISTORY(state, action) {
      state.workflowHistory.push({
        ...action,
        timestamp: Date.now()
      })
    },
    UNDO_LAST_ACTION(state) {
      if (state.workflowHistory.length > 0) {
        const lastAction = state.workflowHistory.pop()
        switch (lastAction.type) {
          case 'add_tool':
            state.workflowTools = state.workflowTools.filter(t => t.id !== lastAction.data.id)
            break
          case 'remove_tool':
            state.workflowTools.push(lastAction.data)
            break
          case 'add_connection':
            state.workflowConnections = state.workflowConnections.filter(c => c.id !== lastAction.data.id)
            break
          case 'remove_connection':
            state.workflowConnections.push(lastAction.data)
            break
        }
      }
    },

    // 선택된 도구 관리
    SET_SELECTED_TOOL(state, tool) {
      state.selectedTool = tool
    },

    // 워크플로우 설정 관리
    UPDATE_WORKFLOW_SETTINGS(state, settings) {
      state.workflowSettings = { ...state.workflowSettings, ...settings }
    },
    SET_WORKFLOW_TOOLS(state, tools) {
      state.workflowTools = tools;
    },
    SET_WORKFLOW_CONNECTIONS(state, connections) {
      state.workflowConnections = connections;
    },
    ADD_WORKFLOW_TOOL(state, tool) {
      const newTool = {
        ...tool,
        position: { x: 100 * state.workflowTools.length, y: 100 }
      }
      state.workflowTools.push(newTool)
      // 히스토리에 추가
      this.commit('tools/ADD_TO_HISTORY', {
        type: 'add_tool',
        data: newTool
      })
      state.workflowTools.push({
        ...tool,
        position: { x: 100 * state.workflowTools.length, y: 100 }
      });
    },
    REMOVE_WORKFLOW_TOOL(state, toolId) {
      const tool = state.workflowTools.find(t => t.id === toolId)
      if (tool) {
        state.workflowTools = state.workflowTools.filter(t => t.id !== toolId)
        state.workflowConnections = state.workflowConnections.filter(
          c => c.source !== toolId && c.target !== toolId
        )
        // 히스토리에 추가
        this.commit('tools/ADD_TO_HISTORY', {
          type: 'remove_tool',
          data: tool
        })
      }
      state.workflowTools = state.workflowTools.filter(t => t.id !== toolId);
      state.workflowConnections = state.workflowConnections.filter(
        c => c.source !== toolId && c.target !== toolId
      );
    },
    ADD_WORKFLOW_CONNECTION(state, connection) {
      state.workflowConnections.push(connection)
      // 히스토리에 추가
      this.commit('tools/ADD_TO_HISTORY', {
        type: 'add_connection',
        data: connection
      })
      state.workflowConnections.push(connection);
    },
    REMOVE_WORKFLOW_CONNECTION(state, connectionId) {
      state.workflowConnections = state.workflowConnections.filter(
        c => c.id !== connectionId
      );
    },
    CLEAR_WORKFLOW(state) {
      state.workflowTools = [];
      state.workflowConnections = [];
    },
    SET_TOOL_COMBINATIONS(state, combinations) {
      state.toolCombinations = combinations;
    },
    SET_CURRENT_TOOL_COMBINATION(state, combination) {
      state.currentToolCombination = combination;
    },
    SET_USER_TOOL_COMBINATIONS(state, combinations) {
      state.userToolCombinations = combinations;
    },
    ADD_TOOL_COMBINATION(state, combination) {
      state.toolCombinations.push(combination);
    },
    UPDATE_TOOL_COMBINATION(state, updatedCombination) {
      const index = state.toolCombinations.findIndex(c => c.id === updatedCombination.id);
      if (index !== -1) {
        state.toolCombinations.splice(index, 1, updatedCombination);
      }
    },
    REMOVE_TOOL_COMBINATION(state, id) {
      state.toolCombinations = state.toolCombinations.filter(c => c.id !== id);
    },
    SET_LOADING(state, status) {
      state.loading = status;
    },
    SET_ERROR(state, error) {
      state.error = error;
    }
  },

  actions: {
    // 워크플로우 작업 실행 취소
    undoLastAction({ commit }) {
      commit('UNDO_LAST_ACTION')
    },

    // 선택된 도구 설정
    setSelectedTool({ commit }, tool) {
      commit('SET_SELECTED_TOOL', tool)
    },

    // 워크플로우 설정 업데이트
    updateWorkflowSettings({ commit }, settings) {
      commit('UPDATE_WORKFLOW_SETTINGS', settings)
    },

    // 워크플로우 저장
    async saveWorkflow({ state }, { name, description }) {
      const workflow = {
        name,
        description,
        tools: state.workflowTools,
        connections: state.workflowConnections,
        settings: state.workflowSettings
      }
      return await toolService.saveWorkflow(workflow)
    },
    updateWorkflowTools({ commit }, tools) {
      commit('SET_WORKFLOW_TOOLS', tools);
    },
    updateWorkflowConnections({ commit }, connections) {
      commit('SET_WORKFLOW_CONNECTIONS', connections);
    },
    addWorkflowTool({ commit }, tool) {
      commit('ADD_WORKFLOW_TOOL', tool);
    },
    removeWorkflowTool({ commit }, toolId) {
      commit('REMOVE_WORKFLOW_TOOL', toolId);
    },
    addWorkflowConnection({ commit }, connection) {
      commit('ADD_WORKFLOW_CONNECTION', connection);
    },
    removeWorkflowConnection({ commit }, connectionId) {
      commit('REMOVE_WORKFLOW_CONNECTION', connectionId);
    },
    clearWorkflow({ commit }) {
      commit('CLEAR_WORKFLOW');
    },
    async fetchToolCombinations({ commit, state }) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        // 실제로는 API 호출이 있어야 하지만, 현재는 상태에 있는 데이터를 바로 사용
        const combinations = state.toolCombinations
        commit('SET_TOOL_COMBINATIONS', combinations)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }

    },

    async fetchToolCombination({ commit }, id) {
      commit('SET_LOADING', true);
      try {
        const combination = await toolService.getToolCombination(id);
        commit('SET_CURRENT_TOOL_COMBINATION', combination);
      } catch (error) {
        commit('SET_ERROR', error.message);
      } finally {
        commit('SET_LOADING', false);
      }
    },

    async fetchUserToolCombinations({ commit }) {
      commit('SET_LOADING', true);
      try {
        const combinations = await toolService.getUserToolCombinations();
        commit('SET_USER_TOOL_COMBINATIONS', combinations);
      } catch (error) {
        commit('SET_ERROR', error.message);
      } finally {
        commit('SET_LOADING', false);
      }
    },

    async createToolCombination({ commit }, data) {
      commit('SET_LOADING', true);
      try {
        const combination = await toolService.createToolCombination(data);
        commit('ADD_TOOL_COMBINATION', combination);
        return combination;
      } catch (error) {
        commit('SET_ERROR', error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },

    async updateToolCombination({ commit }, { id, data }) {
      commit('SET_LOADING', true);
      try {
        const combination = await toolService.updateToolCombination(id, data);
        commit('UPDATE_TOOL_COMBINATION', combination);
        return combination;
      } catch (error) {
        commit('SET_ERROR', error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },

    async deleteToolCombination({ commit }, id) {
      commit('SET_LOADING', true);
      try {
        await toolService.deleteToolCombination(id);
        commit('REMOVE_TOOL_COMBINATION', id);
      } catch (error) {
        commit('SET_ERROR', error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    }
  },

  getters: {
    // 워크플로우 상태 관련 getters
    getWorkflowHistory: state => state.workflowHistory,
    getSelectedTool: state => state.selectedTool,
    getWorkflowSettings: state => state.workflowSettings,

    // 도구 타입별 필터링
    getToolsByType: state => type => {
      return state.availableTools.filter(tool => tool.type === type)
    },

    // 연결된 도구 조회
    getConnectedTools: state => toolId => {
      const connections = state.workflowConnections.filter(
        conn => conn.source === toolId || conn.target === toolId
      )
      return connections.map(conn => {
        const connectedId = conn.source === toolId ? conn.target : conn.source
        return state.workflowTools.find(tool => tool.id === connectedId)
      }).filter(Boolean)
    },

    // 워크플로우 유효성 검사
    isWorkflowValid: state => {
      if (state.workflowTools.length < 2) return false
      return state.workflowTools.every(tool => {
        return state.workflowConnections.some(
          conn => conn.source === tool.id || conn.target === tool.id
        )
      })
    },
    getAvailableTools: (state) => state.availableTools,
    getWorkflowTools: (state) => state.workflowTools,
    getWorkflowConnections: (state) => state.workflowConnections,
    getToolCombinationById: (state) => (id) => {
      return state.toolCombinations.find(c => c.id === id);
    },
    isLoading: (state) => state.loading,
    getError: (state) => state.error
  }
};

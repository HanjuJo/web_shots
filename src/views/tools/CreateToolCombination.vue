<template>
  <div class="create-combination-page">
    <div class="workflow-container">
      <!-- 도구 목록 패널 -->
      <div class="tools-panel">
        <h3>사용 가능한 도구</h3>
        <draggable
          :list="availableTools"
          :group="{ name: 'tools', pull: 'clone', put: false }"
          item-key="id"
          :clone="handleCloneNode"
          @start="handleDragStart"
          @end="handleDragEnd"
        >
          <template #item="{ element }">
            <div class="tool-item" :class="element.type">
              <i :class="getNodeIcon(element.type)"></i>
              <span>{{ element.name }}</span>
            </div>
          </template>
        </draggable>
      </div>

      <!-- 워크플로우 캔버스 -->
      <div class="workflow-canvas">
        <VueFlow
          v-model="elements"
          :default-viewport="{ zoom: 1 }"
          :min-zoom="0.2"
          :max-zoom="4"
          class="workflow-canvas"
          @connect="onConnect"
          @node-drag-stop="onNodeDragStop"
          @elements-remove="handleElementsRemove"
        >
          <template #node-custom="nodeProps">
            <div
              class="custom-node"
              :class="[nodeProps.type, { selected: checkNodeSelected(nodeProps.id) }]"
              v-contextmenu="(e) => handleContextMenu(e, nodeProps)"
              @click="handleNodeSelect(nodeProps)">
              <div class="custom-node-header">
                <i :class="getNodeIcon(nodeProps.type)"></i>
                <span>{{ nodeProps.label }}</span>
              </div>
              <div class="custom-node-body">
                <p>{{ nodeProps.data.description }}</p>
              </div>
            </div>
          </template>
          <Background pattern-color="#aaa" gap="8" />
          <Controls />
          <MiniMap />
        </VueFlow>
      </div>
    </div>
    <div class="page-header">
      <h1>{{ isEditing ? '도구 조합 수정' : '새 도구 조합 만들기' }}</h1>
      <p>콘텐츠 제작에 적합한 AI 도구 조합을 만들어 보세요.</p>
    </div>

    <div class="form-container">
      <form @submit.prevent="saveCombination">
        <div class="form-group">
          <label for="name">도구 조합 이름</label>
          <input 
            type="text" 
            id="name" 
            v-model="combinationForm.name" 
            placeholder="예: 브이로그 제작 도구 세트"
            required
          >
        </div>

        <div class="form-group">
          <label for="description">설명</label>
          <textarea 
            id="description" 
            v-model="combinationForm.description" 
            placeholder="이 도구 조합의 용도와 특징을 설명해주세요"
            rows="3"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label for="contentType">콘텐츠 유형</label>
          <select id="contentType" v-model="combinationForm.contentType" required>
            <option value="" disabled>콘텐츠 유형 선택</option>
            <option v-for="type in contentTypes" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>AI 도구 선택</label>
          <p class="form-hint">최소 1개 이상의 도구를 선택해주세요</p>
          
          <div class="tools-container">
            <div 
              v-for="tool in availableTools" 
              :key="tool.id" 
              :class="['tool-selection-card', { selected: isToolSelected(tool.id) }]"
              @click="toggleToolSelection(tool.id)"
            >
              <div class="tool-card-content">
                <div class="tool-info">
                  <h3>{{ tool.name }}</h3>
                  <span class="tool-category">{{ getCategoryName(tool.categoryId) }}</span>
                </div>
                <p>{{ tool.description }}</p>
                <div class="tool-meta">
                  <span class="tool-rating">
                    <i class="fas fa-star"></i>
                    {{ tool.rating }}
                  </span>
                </div>
              </div>
              <div class="tool-selection-indicator">
                <i class="fas fa-check"></i>
              </div>
            </div>
          </div>
          
          <div v-if="toolSelectionError" class="selection-error">
            {{ toolSelectionError }}
          </div>
        </div>

        <div class="form-group">
          <label for="isPublic">공개 설정</label>
          <div class="toggle-container">
            <label class="toggle">
              <input type="checkbox" v-model="combinationForm.isPublic">
              <span class="slider round"></span>
            </label>
            <span class="toggle-label">{{ combinationForm.isPublic ? '공개' : '비공개' }}</span>
          </div>
          <p class="form-hint">
            공개로 설정하면 다른 사용자들이 이 도구 조합을 볼 수 있습니다.
          </p>
        </div>

        <div class="form-buttons">
          <button type="button" class="cancel-btn" @click="cancel">취소</button>
          <button type="submit" class="save-btn" :disabled="loading">
            <i v-if="loading" class="fas fa-spinner fa-spin"></i>
            {{ isEditing ? '수정하기' : '저장하기' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import draggable from 'vuedraggable'
import { VueFlow, Background, Controls, MiniMap, useVueFlow } from '@vue-flow/core'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'
import '@vue-flow/minimap/dist/style.css'

export default {
  name: 'CreateToolCombination',
  components: {
    draggable,
    VueFlow,
    Background,
    Controls,
    MiniMap
  },

  // 사용자 정의 디렉티브
  directives: {
    // 우클릭 메뉴 디렉티브
    contextmenu: {
      mounted(el, binding) {
        el.addEventListener('contextmenu', (e) => {
          e.preventDefault()
          binding.value(e)
        })
      },
      unmounted(el, binding) {
        el.removeEventListener('contextmenu', binding.value)
      }
    }
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()

    // 컨텍스트 메뉴 상태
    const contextMenu = ref({
      show: false,
      x: 0,
      y: 0,
      target: null
    })

    // 컨텍스트 메뉴 표시
    const showContextMenu = (e, target) => {
      contextMenu.value = {
        show: true,
        x: e.clientX,
        y: e.clientY,
        target
      }
    }

    // 컨텍스트 메뉴 숨기기
    const hideContextMenu = () => {
      contextMenu.value.show = false
    }

    // 키보드 단축키 처리
    const handleKeyDown = (e) => {
      // Undo: Ctrl/Cmd + Z
      if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
        e.preventDefault()
        store.dispatch('tools/undoLastAction')
      }
      // Delete: Delete 키
      else if (e.key === 'Delete' && store.state.tools.selectedTool) {
        e.preventDefault()
        store.dispatch('tools/removeWorkflowTool', store.state.tools.selectedTool.id)
      }
      // Copy: Ctrl/Cmd + C
      else if ((e.ctrlKey || e.metaKey) && e.key === 'c' && store.state.tools.selectedTool) {
        e.preventDefault()
        // 도구 복사 로직 추가 예정
      }
      // Paste: Ctrl/Cmd + V
      else if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
        e.preventDefault()
        // 도구 붙여넣기 로직 추가 예정
      }
    }

    // 키보드 이벤트 리스너 등록
    onMounted(() => {
      window.addEventListener('keydown', handleKeyDown)
      window.addEventListener('click', hideContextMenu)
    })

    // 키보드 이벤트 리스너 제거
    onUnmounted(() => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('click', hideContextMenu)
    })
    const { onConnect, onNodeDragStop, project } = useVueFlow()

    // Vue Flow 이벤트 핸들러 연결
    onConnect(handleConnect)
    onNodeDragStop(handleNodeDragStop)

    // 컨텍스트 메뉴 이벤트 리스너
    const handleContextMenu = (e, node) => {
      showContextMenu(e, node)
    }

    // 노드 관련 함수들
    const handleNodeSelect = (nodeProps) => {
      selectNode(nodeProps)
    }

    const handleCloneNode = (node) => {
      return cloneNode(node)
    }

    const handleDragStart = (event) => {
      onDragStart(event)
    }

    const handleDragEnd = (event) => {
      onDragEnd(event)
    }

    const handleElementsRemove = (elements) => {
      onElementsRemove(elements)
    }

    // 아이콘 가져오기
    const getNodeIcon = (type) => {
      return getToolIcon(type)
    }

    // 노드 선택 상태 확인
    const checkNodeSelected = (id) => {
      return isNodeSelected(id)
    }

    // 워크플로우 상태
    const elements = ref([])
    const nodeId = ref(0)

    // 도구 아이콘 매핑
    const toolIcons = {
      text: 'fas fa-font',
      image: 'fas fa-image',
      video: 'fas fa-video',
      audio: 'fas fa-volume-up'
    }

    // 도구 아이콘 가져오기
    const getToolIcon = (type) => toolIcons[type] || 'fas fa-tools'

    // 노드 선택 관리
    const isNodeSelected = (nodeId) => {
      return store.state.tools.selectedTool?.id === nodeId
    }

    const selectNode = (node) => {
      store.dispatch('tools/setSelectedTool', node)
    }

    // 노드 복제 (드래그 앤 드롭용)
    const cloneNode = (node) => {
      nodeId.value++
      return {
        ...node,
        id: `node-${nodeId.value}`,
        position: project({ x: 100, y: 100 })
      }
    }

    // 드래그 시작
    const onDragStart = () => {
      // 드래그 시작 시 필요한 로직
    }

    // 드래그 종료
    const onDragEnd = () => {
      // 드래그 종료 시 필요한 로직
    }

    // 연결 생성
    const handleConnect = (params) => {
      const connection = {
        id: `edge-${params.source}-${params.target}`,
        source: params.source,
        target: params.target,
        type: 'smoothstep'
      }
      store.dispatch('tools/addWorkflowConnection', connection)
    }

    // 요소 제거
    const onElementsRemove = (elementsToRemove) => {
      elementsToRemove.forEach(element => {
        if (element.type === 'node') {
          store.dispatch('tools/removeWorkflowTool', element.id)
        } else {
          store.dispatch('tools/removeWorkflowConnection', element.id)
        }
      })
    }

    // 노드 위치 업데이트
    const handleNodeDragStop = () => {
      store.dispatch('tools/updateWorkflowTools', elements.value.filter(el => el.type === 'node'))
    }

    // 워크플로우 상태 감시
    watch(
      () => store.state.tools.workflowTools,
      (newTools) => {
        elements.value = [
          ...newTools.map(tool => ({
            id: tool.id,
            type: 'custom',
            data: { ...tool },
            position: tool.position,
            draggable: true,
            connectable: true
          })),
          ...store.state.tools.workflowConnections
        ]
      },
      { deep: true }
    )
    
    const isEditing = computed(() => route.query.edit === 'true')
    const editId = computed(() => route.query.id)
    
    const loading = ref(false)
    const toolSelectionError = ref('')
    const contentTypes = ['유튜브', '블로그', '소셜 미디어', '팟캐스트', '이커머스']
    
    // 임시 도구 데이터 (실제로는 스토어에서 가져와야 함)
    const availableTools = ref([
      {
        id: 1,
        name: 'AI 이미지 메이커',
        description: '고품질 AI 이미지를 빠르고 쉽게 생성하세요',
        image: '/images/tools/image-maker.jpg',
        categoryId: 1,
        rating: 4.8,
        reviewCount: 1234
      },
      {
        id: 2,
        name: 'AI 보이스',
        description: '자연스러운 AI 음성으로 나레이션을 제작하세요',
        image: '/images/tools/voice-maker.jpg',
        categoryId: 2,
        rating: 4.7,
        reviewCount: 892
      },
      {
        id: 3,
        name: 'AI 비디오 에디터',
        description: '원클릭으로 전문적인 영상을 편집하세요',
        image: '/images/tools/video-editor.jpg',
        categoryId: 3,
        rating: 4.6,
        reviewCount: 567
      },
      {
        id: 4,
        name: 'AI 글쓰기 도우미',
        description: '블로그, 광고, 소셜 미디어 등 다양한 콘텐츠를 AI로 작성하세요',
        image: '/images/tools/text-generator.jpg',
        categoryId: 4,
        rating: 4.9,
        reviewCount: 1543
      },
      {
        id: 5,
        name: 'AI 번역기',
        description: '100개 이상의 언어를 자연스럽게 번역하는 AI 도구',
        image: '/images/tools/translator.jpg',
        categoryId: 5,
        rating: 4.8,
        reviewCount: 2134
      },
      {
        id: 6,
        name: 'AI 자막 생성기',
        description: '영상에 자동으로 정확한 자막을 생성하고 번역까지 가능한 AI 도구',
        image: '/images/tools/subtitle-generator.jpg',
        categoryId: 6,
        rating: 4.7,
        reviewCount: 876
      }
    ])
    
    // 폼 데이터 초기화
    const combinationForm = ref({
      name: '',
      description: '',
      contentType: '',
      toolIds: [],
      isPublic: false
    })
    
    // 카테고리 정보
    const categories = [
      { id: 1, name: '이미지 생성' },
      { id: 2, name: '음성 합성' },
      { id: 3, name: '영상 편집' },
      { id: 4, name: '텍스트 생성' },
      { id: 5, name: '번역' },
      { id: 6, name: '자막 생성' }
    ]
    
    // 카테고리 이름 가져오기
    const getCategoryName = (categoryId) => {
      const category = categories.find(c => c.id === categoryId)
      return category ? category.name : '기타'
    }
    
    // 페이지 로드 시 실행
    onMounted(async () => {
      // 수정 모드인 경우 기존 데이터 로드
      if (isEditing.value && editId.value) {
        try {
          loading.value = true
          // 실제로는 API 호출이 필요하지만, 여기서는 스토어에서 데이터를 가져옴
          await store.dispatch('fetchUserToolCombinations')
          const combination = store.state.userToolCombinations.find(c => c.id === parseInt(editId.value))
          
          if (combination) {
            combinationForm.value = {
              name: combination.name,
              description: combination.description,
              contentType: combination.contentType,
              toolIds: [...combination.toolIds],
              isPublic: combination.isPublic || false
            }
          } else {
            router.push('/tools/my-combinations')
          }
        } catch (error) {
          console.error('Error loading combination:', error)
        } finally {
          loading.value = false
        }
      }
    })
    
    // 도구 선택 여부 확인
    const isToolSelected = (toolId) => {
      return combinationForm.value.toolIds.includes(toolId)
    }
    
    // 도구 선택 토글
    const toggleToolSelection = (toolId) => {
      if (isToolSelected(toolId)) {
        combinationForm.value.toolIds = combinationForm.value.toolIds.filter(id => id !== toolId)
      } else {
        combinationForm.value.toolIds.push(toolId)
      }
      
      // 에러 메시지 초기화
      toolSelectionError.value = ''
    }
    
    // 폼 제출 처리
    const saveCombination = async () => {
      // 도구 선택 검증
      if (combinationForm.value.toolIds.length === 0) {
        toolSelectionError.value = '최소 1개 이상의 도구를 선택해주세요'
        return
      }
      
      try {
        loading.value = true
        
        if (isEditing.value && editId.value) {
          // 기존 조합 수정
          await store.dispatch('updateToolCombination', {
            id: parseInt(editId.value),
            updatedCombination: { ...combinationForm.value }
          })
        } else {
          // 새 조합 저장
          await store.dispatch('saveToolCombination', { ...combinationForm.value })
        }
        
        // 저장 성공 후 내 조합 페이지로 이동
        router.push('/tools/my-combinations')
      } catch (error) {
        console.error('Error saving combination:', error)
      } finally {
        loading.value = false
      }
    }
    
    // 취소 버튼 처리
    const cancel = () => {
      router.back()
    }
    
    return {
      // 상태
      isEditing,
      loading,
      contentTypes,
      availableTools,
      combinationForm,
      toolSelectionError,
      elements,
      // 함수
      getCategoryName,
      isToolSelected,
      toggleToolSelection,
      saveCombination,
      cancel,
      // Vue Flow 함수
      handleContextMenu,
      handleNodeSelect,
      handleCloneNode,
      handleDragStart,
      handleDragEnd,
      handleElementsRemove,
      getNodeIcon,
      checkNodeSelected
    }
  }
}
</script>

<style scoped>
.workflow-container {
  display: flex;
  height: calc(100vh - 200px);
  margin: 20px 0;
  gap: 20px;
}

.tools-panel {
  width: 250px;
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tool-item {
  display: flex;
  align-items: center;
  padding: 10px;
  margin: 5px 0;
  background: white;
  border-radius: 4px;
  cursor: move;
  transition: all 0.2s;
}

.tool-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tool-item i {
  margin-right: 10px;
  font-size: 1.2em;
}

.workflow-canvas {
  flex-grow: 1;
  background: #fafafa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.custom-node {
  padding: 10px;
  border-radius: 5px;
  font-size: 12px;
  text-align: center;
  border: 1px solid #ddd;
  background: white;
  width: 150px;
}

.custom-node-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.custom-node-header i {
  margin-right: 8px;
}

.custom-node.text { border-color: #4CAF50; }
.custom-node.image { border-color: #2196F3; }
.custom-node.video { border-color: #F44336; }
.custom-node.audio { border-color: #9C27B0; }

.custom-node.selected {
  box-shadow: 0 0 0 2px #2196F3;
  transform: scale(1.02);
}

.context-menu {
  position: fixed;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 5px 0;
  z-index: 1000;
}

.context-menu-item {
  padding: 8px 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background 0.2s;
}

.context-menu-item:hover {
  background: #f5f5f5;
}

.context-menu-item i {
  margin-right: 8px;
  font-size: 14px;
  width: 20px;
  text-align: center;
}

.vue-flow__minimap {
  transform: scale(0.8);
}

.vue-flow__controls {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.create-combination-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.page-header p {
  font-size: 1.1rem;
  color: #666;
}

.form-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 15px rgba(0,0,0,0.08);
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #333;
}

.form-hint {
  font-size: 0.9rem;
  color: #777;
  margin-top: 0.3rem;
  margin-bottom: 0.8rem;
}

input[type="text"],
textarea,
select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  color: #333;
  transition: border-color 0.2s ease;
}

input[type="text"]:focus,
textarea:focus,
select:focus {
  border-color: #4a6cf7;
  outline: none;
}

.tools-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.tool-selection-card {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 1.2rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all 0.2s ease;
}

.tool-selection-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 10px rgba(0,0,0,0.05);
}

.tool-selection-card.selected {
  border-color: #4a6cf7;
  background-color: #f0f5ff;
}

.tool-card-content {
  flex: 1;
}

.tool-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.8rem;
}

.tool-info h3 {
  font-size: 1.1rem;
  margin: 0;
  color: #333;
}

.tool-category {
  font-size: 0.8rem;
  color: #666;
  background: #f5f5f5;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
}

.tool-selection-card p {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.tool-meta {
  font-size: 0.9rem;
  color: #666;
}

.tool-rating {
  color: #ffc107;
}

.tool-selection-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  background: #4a6cf7;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.tool-selection-card.selected .tool-selection-indicator {
  opacity: 1;
}

.selection-error {
  color: #d9534f;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.toggle-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #4a6cf7;
}

input:focus + .slider {
  box-shadow: 0 0 1px #4a6cf7;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.slider.round {
  border-radius: 24px;
}

.slider.round:before {
  border-radius: 50%;
}

.toggle-label {
  font-size: 1rem;
  color: #333;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-btn, .save-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.cancel-btn {
  background: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.cancel-btn:hover {
  background: #e9e9e9;
}

.save-btn {
  background: #4a6cf7;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.save-btn:hover {
  background: #3a5ce5;
}

.save-btn:disabled {
  background: #a0adf7;
  cursor: not-allowed;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .tools-container {
    grid-template-columns: 1fr;
  }
  
  .form-buttons {
    flex-direction: column;
  }
  
  .cancel-btn, .save-btn {
    width: 100%;
  }
}
</style>

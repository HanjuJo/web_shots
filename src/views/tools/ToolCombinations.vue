<template>
  <div class="combinations-page">
    <div class="page-header">
      <h1>AI 도구 조합</h1>
      <p>컨텐츠 제작 유형에 맞는 최적의 AI 도구 조합을 찾아보세요.</p>
    </div>

    <!-- 콘텐츠 유형 필터 -->
    <div class="content-type-filter">
      <h2>콘텐츠 유형</h2>
      <div class="filter-buttons">
        <button 
          v-for="type in contentTypes" 
          :key="type"
          :class="['filter-button', { active: selectedContentType === type }]"
          @click="selectedContentType = type === selectedContentType ? '' : type"
        >
          {{ type }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <i class="fas fa-spinner fa-spin"></i> 로딩 중...
    </div>
    <div v-if="actionMessage" :class="['action-message', actionMessage.type]">
      <i :class="actionMessage.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
      {{ actionMessage.text }}
    </div>
    <div v-else-if="error" class="error-message">
      <i class="fas fa-exclamation-circle"></i> {{ error }}
    </div>
    <div v-else>
      <!-- 추천 도구 조합 섹션 -->
      <section class="recommended-combinations" v-if="recommendedCombinations.length">
        <h2>추천 도구 조합</h2>
        <div class="combinations-grid">
          <div 
            v-for="combination in recommendedCombinations" 
            :key="combination.id" 
            class="combination-card"
            @click="goToCombinationDetail(combination.id)"
          >
            <div class="combination-header">
              <h3>{{ combination.name }}</h3>
              <span class="content-type-badge">{{ combination.contentType }}</span>
            </div>
            <p class="combination-description">{{ combination.description }}</p>
            <div class="tools-in-combination">
              <h4>포함된 도구</h4>
              <div class="tool-chips">
                <span v-for="toolId in combination.toolIds" :key="toolId" class="tool-chip">
                  <i :class="getToolIcon(toolId)"></i>
                  {{ getToolName(toolId) }}
                </span>
              </div>
            </div>
            <div class="combination-meta">
              <span class="usage-count">
                <i class="fas fa-users"></i> {{ combination.usageCount }}명 사용 중
              </span>
              <span class="creator">by {{ combination.creator }}</span>
            </div>
            <div class="combination-actions">
              <button class="use-combination-btn" @click.stop="useCombination(combination.id)">
                <i class="fas fa-play"></i> 사용하기
              </button>
              <button class="save-combination-btn" @click.stop="saveCombination(combination.id)">
                <i class="fas fa-save"></i> 저장하기
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 모든 도구 조합 섹션 -->
      <section class="all-combinations">
        <div class="section-header">
          <h2>모든 도구 조합</h2>
          <router-link to="/tools/combinations/create" class="create-combination-btn">
            <i class="fas fa-plus"></i> 새 도구 조합 만들기
          </router-link>
        </div>
        <div v-if="filteredCombinations.length === 0" class="no-combinations">
          <p>해당 조건에 맞는 도구 조합이 없습니다.</p>
        </div>
        <div v-else class="combinations-grid">
          <div 
            v-for="combination in filteredCombinations" 
            :key="combination.id" 
            class="combination-card"
            @click="goToCombinationDetail(combination.id)"
          >
            <div class="combination-header">
              <h3>{{ combination.name }}</h3>
              <span class="content-type-badge">{{ combination.contentType }}</span>
            </div>
            <p class="combination-description">{{ combination.description }}</p>
            <div class="tools-in-combination">
              <h4>포함된 도구</h4>
              <div class="tool-chips">
                <span v-for="toolId in combination.toolIds" :key="toolId" class="tool-chip">
                  <i :class="getToolIcon(toolId)"></i>
                  {{ getToolName(toolId) }}
                </span>
              </div>
            </div>
            <div class="combination-meta">
              <span class="usage-count">
                <i class="fas fa-users"></i> {{ combination.usageCount }}명 사용 중
              </span>
              <span class="creator">by {{ combination.creator }}</span>
            </div>
            <div class="combination-actions">
              <button class="use-combination-btn" @click.stop="useCombination(combination.id)">
                <i class="fas fa-play"></i> 사용하기
              </button>
              <button class="save-combination-btn" @click.stop="saveCombination(combination.id)">
                <i class="fas fa-save"></i> 저장하기
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 내 도구 조합 링크 -->
      <section class="my-combinations-link">
        <router-link to="/tools/my-combinations" class="view-my-combinations">
          <i class="fas fa-list"></i> 내 도구 조합 관리하기
        </router-link>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'ToolCombinations',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const selectedContentType = ref('')
    const contentTypes = ['유튜브', '블로그', '소셜 미디어', '팟캐스트', '이커머스']
    
    // Fetch tool combinations from store
    onMounted(() => {
      store.dispatch('fetchToolCombinations')
    })
    
    // Get state from store
    const loading = computed(() => store.state.tools.loading)
    const error = computed(() => store.state.tools.error)
    const allCombinations = computed(() => store.state.tools.toolCombinations)
    const availableTools = computed(() => store.state.tools.availableTools)
    const actionMessage = ref(null)
    
    // Filter combinations by content type
    const filteredCombinations = computed(() => {
      if (!selectedContentType.value) {
        return allCombinations.value
      }
      return allCombinations.value.filter(combo => combo.contentType === selectedContentType.value)
    })
    
    // Get top 3 recommended combinations by usage count
    const recommendedCombinations = computed(() => {
      return [...allCombinations.value]
        .sort((a, b) => b.usageCount - a.usageCount)
        .slice(0, 3)
    })
    
    // Helper function to get tool name by ID
    const getToolName = (toolId) => {
      const tool = availableTools.value.find(t => t.id === toolId)
      return tool ? tool.name : '알 수 없는 도구'
    }
    
    // Helper function to get tool icon by ID
    const getToolIcon = (toolId) => {
      const iconMap = {
        1: 'fas fa-image',
        2: 'fas fa-microphone',
        3: 'fas fa-video',
        4: 'fas fa-pencil-alt',
        5: 'fas fa-language',
        6: 'fas fa-closed-captioning'
      }
      return iconMap[toolId] || 'fas fa-tools'
    }
    
    // Navigation to combination detail
    const goToCombinationDetail = (id) => {
      router.push({ name: 'ToolCombinationDetail', params: { id } })
    }
    
    // Show action message
    const showMessage = (text, type = 'success', duration = 3000) => {
      actionMessage.value = { text, type }
      setTimeout(() => {
        actionMessage.value = null
      }, duration)
    }

    // Use combination
    const useCombination = async (id) => {
      try {
        const combination = allCombinations.value.find(c => c.id === id)
        if (combination) {
          // 워크플로우 초기화
          await store.dispatch('tools/clearWorkflow')
          
          // 도구 조합의 각 도구를 워크플로우에 추가
          for (const toolId of combination.toolIds) {
            const tool = availableTools.value.find(t => t.id === toolId)
            if (tool) {
              await store.dispatch('tools/addWorkflowTool', tool)
            }
          }
          
          showMessage('도구 조합을 불러왔습니다.')
          
          // 도구 조합 상세 페이지로 이동
          router.push({ 
            name: 'CreateToolCombination',
            query: { from: combination.id }
          })
        }
      } catch (error) {
        console.error('도구 조합 사용 중 오류:', error)
        showMessage('도구 조합을 불러오는 중 오류가 발생했습니다.', 'error')
      }
    }
    
    // Save combination to user's collection
    const saveCombination = async (id) => {
      try {
        const combination = allCombinations.value.find(c => c.id === id)
        if (combination) {
          await store.dispatch('tools/createToolCombination', {
            ...combination,
            id: undefined, // 새로운 ID 생성을 위해 제거
            isPublic: false // 개인 저장용으로 설정
          })
          showMessage('도구 조합이 저장되었습니다.')
        }
      } catch (error) {
        console.error('도구 조합 저장 중 오류:', error)
        showMessage('도구 조합 저장 중 오류가 발생했습니다.', 'error')
      }
      

    }
    
    return {
      loading,
      error,
      actionMessage,
      selectedContentType,
      contentTypes,
      filteredCombinations,
      recommendedCombinations,
      getToolName,
      getToolIcon,
      goToCombinationDetail,
      useCombination,
      saveCombination
    }
  }
}
</script>

<style scoped>
.combinations-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.page-header p {
  font-size: 1.1rem;
  color: #666;
}

.content-type-filter {
  margin-bottom: 2rem;
}

.content-type-filter h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-button {
  padding: 0.6rem 1.2rem;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 30px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-button:hover {
  background: #e9e9e9;
}

.filter-button.active {
  background: #4a6cf7;
  color: white;
  border-color: #4a6cf7;
}

.loading, .action-message {
  text-align: center;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.action-message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.action-message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.error-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #d9534f;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.8rem;
}

.create-combination-btn {
  padding: 0.7rem 1.4rem;
  background: #4a6cf7;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s ease;
}

.create-combination-btn:hover {
  background: #3a5ce5;
}

.combinations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.combination-card {
  border: 1px solid #e0e7ff;
  border-radius: 12px;
  padding: 1.8rem;
  background: white;
  box-shadow: 0 4px 12px rgba(74, 108, 247, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: linear-gradient(90deg, #4a6cf7, #6d8bff);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
}

.combination-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(74, 108, 247, 0.12);
  border-color: #c8d5ff;
}

.combination-card:hover::before {
  opacity: 1;
}

.combination-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.combination-header h3 {
  font-size: 1.3rem;
  color: #333;
  margin: 0;
}

.content-type-badge {
  background: linear-gradient(135deg, #f0f5ff 0%, #e6edff 100%);
  color: #4a6cf7;
  padding: 0.4rem 0.9rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid #e0e7ff;
  box-shadow: 0 2px 4px rgba(74, 108, 247, 0.05);
}

.combination-description {
  color: #666;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.tools-in-combination {
  margin-bottom: 1.5rem;
}

.tools-in-combination h4 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #333;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
  
  &::before {
    content: '🔧';
    font-size: 1.2rem;
    margin-bottom: -2px;
  }
}

.tool-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  padding: 0.5rem 0;
  margin: -0.25rem;
}

.tool-chip {
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.9rem;
  color: #4a6cf7;
  font-weight: 500;
  border: 1px solid #e0e7ff;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(74, 108, 247, 0.1);
  cursor: default;
  user-select: none;
  position: relative;
  overflow: hidden;
  
  i {
    font-size: 1rem;
    opacity: 0.9;
    transition: transform 0.3s ease;
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &:hover {
    background: linear-gradient(135deg, #e0e7ff 0%, #d1dbff 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(74, 108, 247, 0.15);
    
    &::before {
      opacity: 1;
    }
    
    i {
      transform: scale(1.1);
    }
  }
}

.combination-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: #777;
}

.usage-count {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  
  i {
    color: #4a6cf7;
    opacity: 0.8;
  }
}

.creator {
  font-weight: 500;
  color: #666;
}

.combination-actions {
  display: flex;
  gap: 0.8rem;
}

.use-combination-btn, .save-combination-btn {
  flex: 1;
  padding: 0.8rem 0;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.6rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.use-combination-btn i, .save-combination-btn i {
  font-size: 1rem;
  transition: transform 0.3s ease;
}

.use-combination-btn:hover i, .save-combination-btn:hover i {
  transform: scale(1.1);
}

.use-combination-btn:active, .save-combination-btn:active {
  transform: translateY(1px);
}

.use-combination-btn {
  background: linear-gradient(135deg, #4a6cf7 0%, #6d8bff 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(74, 108, 247, 0.2);
}

.use-combination-btn:hover {
  background: linear-gradient(135deg, #3a5ce5 0%, #5d7bff 100%);
  box-shadow: 0 6px 16px rgba(74, 108, 247, 0.25);
}

.save-combination-btn {
  background: white;
  color: #4a6cf7;
  border: 2px solid #e0e7ff;
  position: relative;
  z-index: 1;
  overflow: hidden;
}

.save-combination-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f0f5ff 0%, #e6edff 100%);
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.save-combination-btn:hover {
  border-color: #c8d5ff;
  color: #3a5ce5;
}

.save-combination-btn:hover::before {
  opacity: 1;
}

.my-combinations-link {
  text-align: center;
  margin: 2rem 0;
}

.view-my-combinations {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.9rem 1.8rem;
  font-size: 1rem;
  color: #4a6cf7;
  text-decoration: none;
  border: 2px solid #e0e7ff;
  border-radius: 8px;
  background: white;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 500;
  box-shadow: 0 2px 6px rgba(74, 108, 247, 0.08);
}

.view-my-combinations i {
  font-size: 1.1rem;
  transition: transform 0.3s ease;
}

.view-my-combinations:hover {
  background: linear-gradient(135deg, #f0f5ff 0%, #e6edff 100%);
  border-color: #c8d5ff;
  box-shadow: 0 4px 12px rgba(74, 108, 247, 0.12);
}

.view-my-combinations:hover i {
  transform: translateX(2px);
}



.no-combinations {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
  background: linear-gradient(135deg, #f8faff 0%, #f0f5ff 100%);
  border-radius: 12px;
  border: 1px dashed #c8d5ff;
  margin: 2rem 0;
}

.no-combinations p {
  font-size: 1.1rem;
  margin: 0;
}

.no-combinations p::before {
  content: '🔍';
  font-size: 1.4rem;
  margin-right: 0.5rem;
  vertical-align: middle;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .combinations-grid {
    grid-template-columns: 1fr;
  }
  
  .combination-actions {
    flex-direction: column;
  }
}
</style>

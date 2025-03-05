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
    const loading = computed(() => store.state.loading)
    const error = computed(() => store.state.error)
    const allCombinations = computed(() => store.state.toolCombinations)
    
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
      // This should be replaced with actual tool data from the store
      const toolNames = {
        1: 'AI 이미지 메이커',
        2: 'AI 보이스',
        3: 'AI 비디오 에디터',
        4: 'AI 글쓰기 도우미',
        5: 'AI 번역기',
        6: 'AI 자막 생성기'
      }
      return toolNames[toolId] || '알 수 없는 도구'
    }
    
    // Navigation to combination detail
    const goToCombinationDetail = (id) => {
      router.push({ name: 'ToolCombinationDetail', params: { id } })
    }
    
    // Use combination
    const useCombination = (id) => {
      // In a real implementation, this would track usage and redirect to appropriate page
      console.log(`Using combination with ID: ${id}`)
      // For demo purposes, just navigate to detail page
      goToCombinationDetail(id)
    }
    
    // Save combination to user's collection
    const saveCombination = (id) => {
      // In a real implementation, this would save to user's collection via API
      console.log(`Saving combination with ID: ${id} to user's collection`)
      const combinationToSave = allCombinations.value.find(c => c.id === id)
      
      if (combinationToSave) {
        // Save a copy to user's combinations
        store.dispatch('saveToolCombination', {
          ...combinationToSave,
          isPublic: false,
        }).then(() => {
          alert('도구 조합이 저장되었습니다.')
        }).catch(error => {
          console.error('Error saving combination:', error)
          alert('도구 조합 저장 중 오류가 발생했습니다.')
        })
      }
    }
    
    return {
      loading,
      error,
      selectedContentType,
      contentTypes,
      filteredCombinations,
      recommendedCombinations,
      getToolName,
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

.loading, .error-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error-message {
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
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.combination-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
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
  background: #f0f5ff;
  color: #4a6cf7;
  padding: 0.3rem 0.7rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
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
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #555;
}

.tool-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tool-chip {
  background: #f5f5f5;
  padding: 0.3rem 0.7rem;
  border-radius: 15px;
  font-size: 0.85rem;
  color: #555;
}

.combination-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: #777;
}

.combination-actions {
  display: flex;
  gap: 0.8rem;
}

.use-combination-btn, .save-combination-btn {
  flex: 1;
  padding: 0.7rem 0;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s ease;
}

.use-combination-btn {
  background: #4a6cf7;
  color: white;
  border: none;
}

.use-combination-btn:hover {
  background: #3a5ce5;
}

.save-combination-btn {
  background: white;
  color: #4a6cf7;
  border: 1px solid #4a6cf7;
}

.save-combination-btn:hover {
  background: #f0f5ff;
}

.my-combinations-link {
  text-align: center;
  margin: 2rem 0;
}

.view-my-combinations {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  color: #555;
  text-decoration: none;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #f9f9f9;
  transition: background 0.2s ease;
}

.view-my-combinations:hover {
  background: #f0f0f0;
}

.no-combinations {
  text-align: center;
  padding: 3rem;
  color: #777;
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

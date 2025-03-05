<template>
  <div class="my-combinations-page">
    <div class="page-header">
      <h1>내 AI 도구 조합</h1>
      <p>저장한 AI 도구 조합을 관리하고 사용하세요.</p>
    </div>

    <div v-if="loading" class="loading">
      <i class="fas fa-spinner fa-spin"></i> 로딩 중...
    </div>
    <div v-else-if="error" class="error-message">
      <i class="fas fa-exclamation-circle"></i> {{ error }}
    </div>
    <div v-else>
      <!-- 내 도구 조합 섹션 -->
      <section class="user-combinations">
        <div class="d-flex justify-content-between flex-wrap mb-4">
          <h2 class="mb-3">내 도구 조합</h2>
          <div>
            <router-link to="/tools/combinations" class="btn btn-outline-primary me-2">
              <i class="fas fa-list me-1"></i>모든 도구 조합 보기
            </router-link>
            <router-link to="/tools/combinations/create" class="btn btn-primary">
              <i class="fas fa-plus me-1"></i>새 도구 조합 만들기
            </router-link>
          </div>
        </div>

        <div v-if="userCombinations.length === 0" class="no-combinations">
          <p>저장된 도구 조합이 없습니다.</p>
          <router-link to="/tools/combinations" class="browse-combinations-btn">
            추천 도구 조합 살펴보기
          </router-link>
        </div>
        <div v-else class="combinations-grid">
          <div 
            v-for="combination in userCombinations" 
            :key="combination.id" 
            class="combination-card"
          >
            <div class="card-body">
              <h5 class="card-title">{{ combination.name }}</h5>
              <p class="card-text">{{ combination.description }}</p>
              <p class="card-text">
                <small class="text-muted">
                  <i class="fas fa-tag me-1"></i>{{ combination.contentType }} | 
                  <i class="fas fa-toolbox me-1"></i>도구 {{ combination.toolIds.length }}개
                </small>
              </p>
              <div class="mt-3">
                <router-link 
                  :to="`/tools/combinations/${combination.id}`" 
                  class="btn btn-sm btn-outline-primary me-2"
                >
                  <i class="fas fa-info-circle me-1"></i>상세 보기
                </router-link>
                <router-link 
                  :to="`/tools/combinations/edit/${combination.id}`" 
                  class="btn btn-sm btn-outline-secondary me-2"
                >
                  <i class="fas fa-edit me-1"></i>수정하기
                </router-link>
                <button 
                  @click="confirmDelete(combination.id)" 
                  class="btn btn-sm btn-outline-danger"
                >
                  <i class="fas fa-trash-alt me-1"></i>삭제
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 최근 사용한 콘텐츠 섹션 -->
      <section class="recent-content" v-if="recentContents.length > 0">
        <h2>최근 제작한 콘텐츠</h2>
        <div class="recent-content-grid">
          <div 
            v-for="content in recentContents" 
            :key="content.id" 
            class="content-card"
          >
            <img :src="content.thumbnail" :alt="content.title" class="content-thumbnail">
            <div class="content-info">
              <h3>{{ content.title }}</h3>
              <p>{{ content.description }}</p>
              <div class="content-meta">
                <span class="content-date">{{ formatDate(content.createdAt) }}</span>
                <span class="content-type">{{ content.type }}</span>
              </div>
              <div class="content-tools">
                <span>사용 도구:</span>
                <div class="tool-chips">
                  <span v-for="toolId in content.toolIds" :key="toolId" class="tool-chip">
                    {{ getToolName(toolId) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 삭제 확인 모달 -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-content">
        <h3>도구 조합 삭제</h3>
        <p>정말로 이 도구 조합을 삭제하시겠습니까?</p>
        <div class="modal-actions">
          <button @click="deleteCombination" class="confirm-delete-btn">삭제</button>
          <button @click="showDeleteModal = false" class="cancel-btn">취소</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'MyToolCombinations',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const showDeleteModal = ref(false)
    const combinationToDelete = ref(null)
    
    // 임시 최근 콘텐츠 데이터 
    const recentContents = ref([
      {
        id: 1,
        title: '브이로그: 제주도 여행 1편',
        description: 'AI 도구를 활용한 브이로그 제작 첫 번째 시리즈',
        thumbnail: '/images/content/vlog-thumbnail.jpg',
        type: '유튜브',
        createdAt: '2024-02-25T15:30:00Z',
        toolIds: [3, 6] // 영상 편집, 자막 생성
      },
      {
        id: 2,
        title: '신제품 리뷰: 최신 스마트폰',
        description: 'AI로 제작한 전문적인 제품 리뷰 콘텐츠',
        thumbnail: '/images/content/review-thumbnail.jpg',
        type: '블로그',
        createdAt: '2024-03-01T10:15:00Z',
        toolIds: [1, 4] // 이미지 생성, 텍스트 생성
      }
    ])
    
    // Fetch user's tool combinations on page load
    onMounted(() => {
      store.dispatch('fetchUserToolCombinations')
    })
    
    // Get state from store
    const loading = computed(() => store.state.loading)
    const error = computed(() => store.state.error)
    const userCombinations = computed(() => store.state.userToolCombinations)
    
    // Format date
    const formatDate = (dateString) => {
      if (!dateString) return '날짜 없음'
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(date)
    }
    
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
    
    // Use combination
    const useCombination = (id) => {
      console.log(`Using combination with ID: ${id}`)
      // For demo, navigate to tool combination detail page
      router.push({ name: 'ToolCombinationDetail', params: { id } })
    }
    
    // Edit combination
    const editCombination = (id) => {
      console.log(`Editing combination with ID: ${id}`)
      router.push({ 
        name: 'CreateToolCombination', 
        query: { edit: 'true', id: id } 
      })
    }
    
    // Show delete confirmation
    const confirmDelete = (id) => {
      combinationToDelete.value = id
      showDeleteModal.value = true
    }
    
    // Delete combination
    const deleteCombination = () => {
      if (combinationToDelete.value) {
        store.dispatch('deleteToolCombination', combinationToDelete.value)
          .then(() => {
            showDeleteModal.value = false
            combinationToDelete.value = null
          })
          .catch(error => {
            console.error('Error deleting combination:', error)
          })
      }
    }
    
    return {
      loading,
      error,
      userCombinations,
      recentContents,
      showDeleteModal,
      formatDate,
      getToolName,
      useCombination,
      editCombination,
      confirmDelete,
      deleteCombination
    }
  }
}
</script>

<style scoped>
.my-combinations-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  position: relative;
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

.no-combinations {
  text-align: center;
  padding: 3rem;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.browse-combinations-btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.8rem 1.5rem;
  background: #4a6cf7;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.browse-combinations-btn:hover {
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
  justify-content: flex-end;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: #777;
}

.combination-actions {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 0.8rem;
}

.use-combination-btn, .edit-combination-btn, .delete-combination-btn {
  padding: 0.7rem;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.use-combination-btn {
  background: #4a6cf7;
  color: white;
  border: none;
}

.use-combination-btn:hover {
  background: #3a5ce5;
}

.edit-combination-btn {
  background: white;
  color: #4a6cf7;
  border: 1px solid #4a6cf7;
}

.edit-combination-btn:hover {
  background: #f0f5ff;
}

.delete-combination-btn {
  background: white;
  color: #d9534f;
  border: 1px solid #d9534f;
}

.delete-combination-btn:hover {
  background: #ffe6e6;
}

/* 최근 콘텐츠 섹션 */
.recent-content {
  margin-top: 3rem;
}

.recent-content h2 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
}

.recent-content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 1.5rem;
}

.content-card {
  display: flex;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.content-thumbnail {
  width: 180px;
  height: 100%;
  object-fit: cover;
}

.content-info {
  flex: 1;
  padding: 1.2rem;
}

.content-info h3 {
  font-size: 1.2rem;
  margin: 0 0 0.5rem 0;
  color: #333;
}

.content-info p {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  line-height: 1.4;
}

.content-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: #777;
}

.content-tools {
  font-size: 0.85rem;
}

.content-tools > span {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
}

/* 모달 스타일 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.modal-content h3 {
  margin-top: 0;
  color: #333;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.confirm-delete-btn, .cancel-btn {
  padding: 0.7rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.confirm-delete-btn {
  background: #d9534f;
  color: white;
  border: none;
}

.confirm-delete-btn:hover {
  background: #c9302c;
}

.cancel-btn {
  background: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.cancel-btn:hover {
  background: #e9e9e9;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .combinations-grid, .recent-content-grid {
    grid-template-columns: 1fr;
  }
  
  .content-card {
    flex-direction: column;
  }
  
  .content-thumbnail {
    width: 100%;
    height: 200px;
  }
  
  .combination-actions {
    grid-template-columns: 1fr;
  }
}
</style>

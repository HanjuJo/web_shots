<template>
  <div class="create-combination-page">
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
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'CreateToolCombination',
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    
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
      isEditing,
      loading,
      contentTypes,
      availableTools,
      combinationForm,
      toolSelectionError,
      getCategoryName,
      isToolSelected,
      toggleToolSelection,
      saveCombination,
      cancel
    }
  }
}
</script>

<style scoped>
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

<template>
  <div class="container mt-4">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">도구 조합 정보를 불러오는 중...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger" role="alert">
      <i class="fas fa-exclamation-triangle me-2"></i> {{ error }}
    </div>
    
    <div v-else-if="combination" class="tool-detail">
      <!-- Header with combination info -->
      <div class="card mb-4 shadow-sm border-0">
        <div class="card-body p-4">
          <h1 class="card-title mb-3 d-flex align-items-center">
            {{ combination.name }}
            <span class="badge bg-primary ms-3">{{ combination.contentType }}</span>
          </h1>
          
          <p class="card-text text-muted mb-4">{{ combination.description }}</p>
          
          <div class="d-flex flex-wrap mb-3">
            <div class="me-4 mb-3">
              <small class="text-muted d-block">만든이</small>
              <span>{{ combination.creator || '관리자' }}</span>
            </div>
            <div class="me-4 mb-3">
              <small class="text-muted d-block">생성일</small>
              <span>{{ formatDate(combination.createdAt) }}</span>
            </div>
            <div class="me-4 mb-3" v-if="combination.usageCount">
              <small class="text-muted d-block">사용횟수</small>
              <span>{{ combination.usageCount.toLocaleString() }}회</span>
            </div>
          </div>
          
          <div class="d-flex flex-wrap">
            <button 
              v-if="!isUserCombination" 
              @click="saveToMyCombinations" 
              class="btn btn-primary me-2 mb-2"
            >
              <i class="fas fa-save me-2"></i>내 도구 조합으로 저장
            </button>
            <button 
              v-if="isUserCombination" 
              @click="editCombination" 
              class="btn btn-outline-primary me-2 mb-2"
            >
              <i class="fas fa-edit me-2"></i>수정하기
            </button>
            <button 
              @click="useToolCombination" 
              class="btn btn-success me-2 mb-2"
            >
              <i class="fas fa-play me-2"></i>이 조합으로 콘텐츠 만들기
            </button>
          </div>
        </div>
      </div>
      
      <!-- Tools in this combination -->
      <h4 class="mb-3">포함된 도구 ({{ toolsInCombination.length }})</h4>
      <div class="row row-cols-1 row-cols-md-2 g-4 mb-4">
        <div v-for="tool in toolsInCombination" :key="tool.id" class="col">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">{{ tool.name }}</h5>
              <p class="card-text">{{ tool.description }}</p>
              <router-link :to="`/tools/${tool.id}`" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-info-circle me-1"></i>도구 상세보기
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Usage Guide -->
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-header bg-light">
          <h4 class="mb-0">사용 가이드</h4>
        </div>
        <div class="card-body">
          <ol class="mb-0">
            <li class="mb-2">이 도구 조합을 활용하여 다음과 같은 콘텐츠를 만들 수 있습니다: <strong>{{ combination.contentType }}</strong></li>
            <li class="mb-2">각 도구는 순서대로 사용하는 것을 권장합니다.</li>
            <li class="mb-2">결과물은 자동으로 저장되며, 내 콘텐츠 페이지에서 확인할 수 있습니다.</li>
            <li class="mb-2">도구 조합을 사용하여 콘텐츠를 생성한 후에는 피드백을 제공해주세요.</li>
          </ol>
        </div>
      </div>
      
      <!-- Related Combinations -->
      <h4 class="mb-3">관련 도구 조합</h4>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div v-for="related in relatedCombinations" :key="related.id" class="col">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">{{ related.name }}</h5>
              <p class="card-text">{{ related.description }}</p>
              <router-link :to="`/tools/combinations/${related.id}`" class="btn btn-sm btn-outline-primary">
                자세히 보기
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="alert alert-warning mt-4" role="alert">
      <i class="fas fa-exclamation-circle me-2"></i> 해당 도구 조합을 찾을 수 없습니다.
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import dayjs from 'dayjs'

export default {
  name: 'ToolCombinationDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const store = useStore()
    
    // State
    const combination = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const allTools = ref([
      { id: 1, name: '이미지 생성 AI', description: '텍스트 프롬프트로 고품질 이미지를 생성합니다.' },
      { id: 2, name: '음성 합성 AI', description: '자연스러운 AI 보이스를 다양한 언어로 생성합니다.' },
      { id: 3, name: '영상 편집 AI', description: '영상을 자동으로 편집하고 하이라이트를 추출합니다.' },
      { id: 4, name: '텍스트 생성 AI', description: '콘텐츠 주제에 맞는 텍스트를 자동으로 생성합니다.' },
      { id: 5, name: '번역 AI', description: '여러 언어로 콘텐츠를 정확하게 번역합니다.' },
      { id: 6, name: '자막 생성 AI', description: '영상에서 음성을 인식하여 자동으로 자막을 생성합니다.' }
    ])
    
    // Get all tool combinations
    const allCombinations = computed(() => {
      return [
        ...store.getters.getToolCombinations,
        ...store.getters.getUserToolCombinations
      ]
    })
    
    // Determine if this is a user's combination
    const isUserCombination = computed(() => {
      return store.getters.getUserToolCombinations.some(
        c => c.id === parseInt(route.params.id)
      )
    })
    
    // Get tools in this combination
    const toolsInCombination = computed(() => {
      if (!combination.value) return []
      return allTools.value.filter(tool => 
        combination.value.toolIds.includes(tool.id)
      )
    })
    
    // Get related combinations with same content type
    const relatedCombinations = computed(() => {
      if (!combination.value) return []
      return allCombinations.value
        .filter(c => 
          c.contentType === combination.value.contentType && 
          c.id !== combination.value.id
        )
        .slice(0, 3)
    })
    
    // Load combinations on mount
    onMounted(async () => {
      try {
        loading.value = true
        error.value = null
        
        // Fetch all combinations if not already loaded
        if (store.getters.getToolCombinations.length === 0) {
          await store.dispatch('fetchToolCombinations')
        }
        if (store.getters.getUserToolCombinations.length === 0) {
          await store.dispatch('fetchUserToolCombinations')
        }
        
        // Find the combination with the matching ID
        const combinationId = parseInt(route.params.id)
        const found = allCombinations.value.find(c => c.id === combinationId)
        
        if (found) {
          combination.value = found
        } else {
          error.value = '도구 조합을 찾을 수 없습니다.'
        }
      } catch (err) {
        console.error('Error loading tool combination:', err)
        error.value = '도구 조합을 불러오는 중 오류가 발생했습니다.'
      } finally {
        loading.value = false
      }
    })
    
    // Methods
    const formatDate = (date) => {
      return dayjs(date).format('YYYY년 MM월 DD일')
    }
    
    const saveToMyCombinations = async () => {
      try {
        if (!combination.value) return
        
        // Create a copy for the user's collection
        const userCombination = {
          ...combination.value,
          id: null // Remove ID so a new one will be generated
        }
        
        await store.dispatch('saveToolCombination', userCombination)
        alert('도구 조합이 성공적으로 저장되었습니다.')
      } catch (err) {
        console.error('Error saving combination:', err)
        alert('도구 조합 저장 중 오류가 발생했습니다.')
      }
    }
    
    const editCombination = () => {
      router.push(`/tools/combinations/edit/${combination.value.id}`)
    }
    
    const useToolCombination = () => {
      alert('이 기능은 아직 개발 중입니다.') 
      // TODO: Implement content creation flow with this combination
    }
    
    return {
      combination,
      loading,
      error,
      toolsInCombination,
      relatedCombinations,
      isUserCombination,
      formatDate,
      saveToMyCombinations,
      editCombination,
      useToolCombination
    }
  }
}
</script>

<style scoped>
.tool-detail {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

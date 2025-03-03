<template>
  <div class="tools">
    <div class="container py-5">
      <h1 class="mb-4">AI 크리에이터 도구</h1>
      
      <!-- 검색 및 필터 -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-4">
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="도구 검색..."
                @input="filterTools"
              >
            </div>
            <div class="col-md-3">
              <select v-model="selectedCategory" class="form-select" @change="filterTools">
                <option value="">모든 카테고리</option>
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
            <div class="col-md-3">
              <select v-model="priceRange" class="form-select" @change="filterTools">
                <option value="">모든 가격대</option>
                <option value="free">무료</option>
                <option value="paid">유료</option>
                <option value="freemium">프리미엄</option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-primary w-100" @click="resetFilters">
                필터 초기화
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 도구 목록 -->
      <div class="row g-4">
        <div v-for="tool in filteredTools" :key="tool.id" class="col-md-4">
          <div class="card h-100">
            <img :src="tool.image" class="card-img-top" :alt="tool.name">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title mb-0">{{ tool.name }}</h5>
                <span :class="['badge', getPriceBadgeClass(tool.pricingType)]">
                  {{ tool.pricingType }}
                </span>
              </div>
              <p class="card-text">{{ tool.description }}</p>
              
              <!-- 기능 태그 -->
              <div class="mb-3">
                <span 
                  v-for="feature in tool.features" 
                  :key="feature"
                  class="badge bg-light text-dark me-2 mb-2"
                >
                  {{ feature }}
                </span>
              </div>
              
              <!-- 평점 -->
              <div class="mb-3">
                <div class="d-flex align-items-center">
                  <div class="stars me-2">
                    <i v-for="n in 5" :key="n"
                       :class="['fas', 'fa-star', n <= tool.rating ? 'text-warning' : 'text-muted']"
                    ></i>
                  </div>
                  <span class="text-muted">({{ tool.reviewCount }})</span>
                </div>
              </div>
              
              <!-- 액션 버튼 -->
              <div class="d-grid gap-2">
                <a :href="tool.websiteUrl" target="_blank" class="btn btn-primary">
                  웹사이트 방문
                </a>
                <button class="btn btn-outline-primary" @click="showToolModal(tool)">
                  자세히 보기
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 도구 상세 모달 -->
      <div class="modal fade" id="toolModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ selectedTool?.name }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" v-if="selectedTool">
              <div class="row">
                <div class="col-md-6">
                  <img :src="selectedTool.image" class="img-fluid rounded" :alt="selectedTool.name">
                </div>
                <div class="col-md-6">
                  <h6>가격 정보</h6>
                  <p>{{ selectedTool.pricing }}</p>
                  
                  <h6 class="mt-4">주요 기능</h6>
                  <ul class="list-unstyled">
                    <li v-for="feature in selectedTool.features" :key="feature">
                      <i class="fas fa-check text-success me-2"></i>{{ feature }}
                    </li>
                  </ul>
                </div>
              </div>
              
              <div class="mt-4">
                <h6>사용 사례</h6>
                <div class="row g-3">
                  <div v-for="useCase in selectedTool.useCases" :key="useCase.title" class="col-md-6">
                    <div class="card">
                      <div class="card-body">
                        <h6>{{ useCase.title }}</h6>
                        <p class="mb-0">{{ useCase.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="mt-4">
                <h6>튜토리얼</h6>
                <div class="list-group">
                  <a v-for="tutorial in selectedTool.tutorials" 
                     :key="tutorial.id"
                     :href="tutorial.url"
                     target="_blank"
                     class="list-group-item list-group-item-action"
                  >
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1">{{ tutorial.title }}</h6>
                      <small>{{ tutorial.duration }}</small>
                    </div>
                    <p class="mb-1">{{ tutorial.description }}</p>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'

export default {
  name: 'ToolsPage',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      priceRange: '',
      selectedTool: null,
      categories: ['이미지 생성', '영상 편집', '음성 합성', '텍스트 생성', '3D 모델링'],
      tools: [
        {
          id: 1,
          name: 'Midjourney',
          category: '이미지 생성',
          description: '고품질 AI 이미지 생성 도구',
          pricingType: '유료',
          pricing: '기본 플랜 $10/월',
          image: require('@/assets/tool-1.jpg'),
          features: ['고해상도 출력', '다양한 스타일', '빠른 생성 속도'],
          rating: 4.8,
          reviewCount: 1250,
          websiteUrl: 'https://www.midjourney.com',
          useCases: [
            {
              title: '제품 이미지 생성',
              description: '상세한 제품 이미지를 빠르게 생성'
            },
            {
              title: '컨셉 아트',
              description: '게임과 영화를 위한 컨셉 아트 제작'
            }
          ],
          tutorials: [
            {
              id: 1,
              title: '기초 사용법',
              description: '프롬프트 작성부터 이미지 생성까지',
              duration: '15분',
              url: '#'
            }
          ]
        },
        // 더 많은 도구들...
      ]
    }
  },
  computed: {
    filteredTools() {
      return this.tools.filter(tool => {
        const matchesSearch = tool.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                            tool.description.toLowerCase().includes(this.searchQuery.toLowerCase())
        const matchesCategory = !this.selectedCategory || tool.category === this.selectedCategory
        const matchesPrice = !this.priceRange || tool.pricingType === this.priceRange
        
        return matchesSearch && matchesCategory && matchesPrice
      })
    }
  },
  methods: {
    getPriceBadgeClass(type) {
      const classes = {
        '무료': 'bg-success',
        '유료': 'bg-primary',
        '프리미엄': 'bg-warning'
      }
      return classes[type] || 'bg-secondary'
    },
    
    showToolModal(tool) {
      this.selectedTool = tool
      new Modal(document.getElementById('toolModal')).show()
    },
    
    resetFilters() {
      this.searchQuery = ''
      this.selectedCategory = ''
      this.priceRange = ''
    }
  }
}
</script>

<style scoped>
.tools {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.stars {
  font-size: 0.9rem;
}

.modal-body {
  max-height: 80vh;
  overflow-y: auto;
}
</style>

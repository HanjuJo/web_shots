<template>
  <div class="tutorials">
    <div class="container py-5">
      <h1 class="mb-4">튜토리얼</h1>
      
      <!-- 검색 및 필터 -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="튜토리얼 검색..."
                @input="filterTutorials"
              >
            </div>
            <div class="col-md-4">
              <select v-model="selectedCategory" class="form-select" @change="filterTutorials">
                <option value="">모든 카테고리</option>
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
            <div class="col-md-2">
              <select v-model="selectedLevel" class="form-select" @change="filterTutorials">
                <option value="">모든 레벨</option>
                <option value="beginner">입문</option>
                <option value="intermediate">중급</option>
                <option value="advanced">고급</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- 튜토리얼 목록 -->
      <div class="row g-4">
        <div v-for="tutorial in filteredTutorials" :key="tutorial.id" class="col-md-4">
          <div class="card h-100">
            <img :src="tutorial.thumbnail" class="card-img-top" :alt="tutorial.title">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title">{{ tutorial.title }}</h5>
                <span :class="['badge', getLevelBadgeClass(tutorial.level)]">
                  {{ tutorial.level }}
                </span>
              </div>
              <p class="card-text">{{ tutorial.description }}</p>
              
              <!-- 태그 -->
              <div class="mb-3">
                <span 
                  v-for="tag in tutorial.tags" 
                  :key="tag"
                  class="badge bg-light text-dark me-2 mb-2"
                >
                  #{{ tag }}
                </span>
              </div>
              
              <!-- 튜토리얼 정보 -->
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div class="d-flex align-items-center">
                  <i class="far fa-clock me-1"></i>
                  <small>{{ tutorial.duration }}</small>
                </div>
                <div class="d-flex align-items-center">
                  <i class="far fa-eye me-1"></i>
                  <small>{{ formatNumber(tutorial.views) }} 조회</small>
                </div>
              </div>
              
              <!-- 작성자 정보 -->
              <div class="d-flex align-items-center mb-3">
                <img :src="tutorial.author.avatar" class="rounded-circle me-2" width="30" height="30">
                <span>{{ tutorial.author.name }}</span>
              </div>
              
              <!-- 액션 버튼 -->
              <div class="d-grid">
                <button class="btn btn-primary" @click="showTutorial(tutorial)">
                  학습하기
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 튜토리얼 상세 모달 -->
      <div class="modal fade" id="tutorialModal" tabindex="-1">
        <div class="modal-dialog modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ selectedTutorial?.title }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" v-if="selectedTutorial">
              <!-- 비디오 플레이어 -->
              <div class="ratio ratio-16x9 mb-4">
                <iframe 
                  :src="selectedTutorial.videoUrl" 
                  title="Tutorial video player" 
                  frameborder="0" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                  allowfullscreen
                ></iframe>
              </div>
              
              <!-- 튜토리얼 내용 -->
              <div class="row">
                <div class="col-md-8">
                  <div class="mb-4">
                    <h6>설명</h6>
                    <p>{{ selectedTutorial.description }}</p>
                  </div>
                  
                  <div class="mb-4">
                    <h6>학습 목표</h6>
                    <ul>
                      <li v-for="objective in selectedTutorial.objectives" 
                          :key="objective">
                        {{ objective }}
                      </li>
                    </ul>
                  </div>
                  
                  <div class="mb-4">
                    <h6>필요한 도구</h6>
                    <ul>
                      <li v-for="tool in selectedTutorial.requiredTools" 
                          :key="tool.name">
                        {{ tool.name }} - {{ tool.version }}
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div class="col-md-4">
                  <div class="card">
                    <div class="card-body">
                      <h6>목차</h6>
                      <div class="list-group list-group-flush">
                        <a v-for="(chapter, index) in selectedTutorial.chapters" 
                           :key="index"
                           href="#"
                           class="list-group-item list-group-item-action"
                        >
                          {{ index + 1 }}. {{ chapter.title }}
                          <span class="float-end text-muted">{{ chapter.duration }}</span>
                        </a>
                      </div>
                    </div>
                  </div>
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
export default {
  name: 'TutorialsPage',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      selectedLevel: '',
      selectedTutorial: null,
      categories: ['Midjourney', 'ChatGPT', 'Runway', 'Stable Diffusion'],
      tutorials: [
        {
          id: 1,
          title: 'Midjourney 마스터하기',
          description: '프롬프트 작성부터 고급 이미지 생성까지 완벽 가이드',
          thumbnail: require('@/assets/tool-1.jpg'),
          level: '입문',
          duration: '2시간 30분',
          views: 15000,
          tags: ['Midjourney', 'AI아트', '프롬프트'],
          author: {
            name: '크리에이터123',
            avatar: require('@/assets/avatar-1.jpg')
          },
          videoUrl: 'https://www.youtube.com/embed/example',
          objectives: [
            '프롬프트 작성 기초 습득',
            '이미지 스타일 컨트롤 방법 이해',
            '효과적인 이미지 생성 워크플로우 구축'
          ],
          requiredTools: [
            { name: 'Discord', version: '최신 버전' },
            { name: 'Midjourney Bot', version: 'V5' }
          ],
          chapters: [
            { title: '기초 설정', duration: '10:00' },
            { title: '프롬프트 작성법', duration: '30:00' },
            { title: '이미지 스타일 컨트롤', duration: '45:00' },
            { title: '고급 테크닉', duration: '35:00' },
            { title: '실전 예제', duration: '30:00' }
          ]
        }
        // 더 많은 튜토리얼...
      ]
    }
  },
  computed: {
    filteredTutorials() {
      return this.tutorials.filter(tutorial => {
        const matchesSearch = tutorial.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                            tutorial.description.toLowerCase().includes(this.searchQuery.toLowerCase())
        const matchesCategory = !this.selectedCategory || tutorial.tags.includes(this.selectedCategory)
        const matchesLevel = !this.selectedLevel || tutorial.level === this.selectedLevel
        
        return matchesSearch && matchesCategory && matchesLevel
      })
    }
  },
  methods: {
    getLevelBadgeClass(level) {
      const classes = {
        '입문': 'bg-success',
        '중급': 'bg-warning',
        '고급': 'bg-danger'
      }
      return classes[level] || 'bg-secondary'
    },
    
    showTutorial(tutorial) {
      this.selectedTutorial = tutorial
      new bootstrap.Modal(document.getElementById('tutorialModal')).show()
    },
    
    formatNumber(num) {
      return new Intl.NumberFormat('ko-KR').format(num)
    },
    
    filterTutorials() {
      // 필터링은 computed 속성을 통해 자동으로 처리됨
    }
  }
}
</script>

<style scoped>
.tutorials {
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

.modal-body {
  max-height: 80vh;
  overflow-y: auto;
}

.list-group-item {
  border-left: none;
  border-right: none;
}

.list-group-item:first-child {
  border-top: none;
}

.list-group-item:last-child {
  border-bottom: none;
}
</style>

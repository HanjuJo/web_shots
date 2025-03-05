<template>
  <div class="tutorials">
    <div class="container py-5">
      <h1 class="mb-4">튜토리얼</h1>
      
      <!-- 검색 및 필터 -->
      <div class="search-filters">
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

      <!-- 튜토리얼 목록 -->
      <div class="tutorial-grid">
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
              <div class="tag-list">
                <span 
                  v-for="tag in tutorial.tags" 
                  :key="tag"
                  class="tag"
                >
                  #{{ tag }}
                </span>
              </div>
              
              <!-- 튜토리얼 정보 -->
              <div class="tutorial-stats">
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
              <div class="author-info">
                <img :src="tutorial.author.avatar" class="author-avatar me-2" :alt="tutorial.author.name">
                <span class="author-name">{{ tutorial.author.name }}</span>
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
                    <ul class="objectives-list">
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
import { Modal } from 'bootstrap/dist/js/bootstrap.bundle.min.js'

export default {
  name: 'TutorialsPage',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      selectedLevel: '',
      selectedTutorial: null,
      modal: null,
      categories: ['Midjourney', 'ChatGPT', 'Runway', 'Stable Diffusion', 'Claude', 'Leonardo.ai'],
      tutorials: [
        {
          id: 1,
          title: 'ChatGPT 프롬프트 엔지니어링 마스터하기',
          description: 'ChatGPT를 200% 활용하는 프롬프트 작성법',
          thumbnail: 'https://placehold.co/600x400/6366f1/white?text=ChatGPT+Tutorial',
          level: '중급',
          duration: '3시간',
          views: 25000,
          tags: ['ChatGPT', 'AI챗봇', '프롬프트'],
          author: {
            name: 'AI마스터',
            avatar: 'https://placehold.co/100x100/6366f1/white?text=Avatar'
          }
        },
        {
          id: 2,
          title: 'Midjourney V6 완벽 가이드',
          description: '최신 버전 Midjourney로 전문가급 이미지 생성하기',
          thumbnail: 'https://placehold.co/600x400/8b5cf6/white?text=Midjourney+Tutorial',
          level: '입문',
          duration: '4시간',
          views: 32000,
          tags: ['Midjourney', 'AI아트', '이미지생성'],
          author: {
            name: '디자인프로',
            avatar: 'https://placehold.co/100x100/8b5cf6/white?text=Avatar'
          }
        },
        {
          id: 3,
          title: 'Runway Gen-2로 AI 영상 제작하기',
          description: 'AI 비디오 제작의 모든 것',
          thumbnail: 'https://placehold.co/600x400/f43f5e/white?text=Runway+Tutorial',
          level: '고급',
          duration: '5시간',
          views: 18000,
          tags: ['Runway', 'AI비디오', '영상편집'],
          author: {
            name: '영상크리에이터',
            avatar: 'https://placehold.co/100x100/f43f5e/white?text=Avatar'
          }
        },
        {
          id: 4,
          title: 'Leonardo.ai로 게임 아트 만들기',
          description: '게임 캐릭터와 배경 디자인을 위한 AI 활용법',
          thumbnail: 'https://placehold.co/600x400/14b8a6/white?text=Leonardo+Tutorial',
          level: '중급',
          duration: '4시간 30분',
          views: 15000,
          tags: ['Leonardo.ai', 'AI아트', '게임디자인'],
          author: {
            name: '게임아티스트',
            avatar: 'https://placehold.co/100x100/14b8a6/white?text=Avatar'
          }
        },
        {
          id: 5,
          title: 'Claude로 전문 문서 작성하기',
          description: '비즈니스 문서 작성을 위한 Claude 활용 가이드',
          thumbnail: 'https://placehold.co/600x400/ec4899/white?text=Claude+Tutorial',
          level: '입문',
          duration: '2시간 30분',
          views: 12000,
          tags: ['Claude', 'AI글쓰기', '비즈니스'],
          author: {
            name: '비즈니스프로',
            avatar: 'https://placehold.co/100x100/ec4899/white?text=Avatar'
          }
        },
        {
          id: 6,
          title: 'Stable Diffusion으로 웹툰 제작하기',
          description: 'AI로 만드는 나만의 웹툰 제작 가이드',
          thumbnail: 'https://placehold.co/600x400/0ea5e9/white?text=SD+Tutorial',
          level: '중급',
          duration: '6시간',
          views: 20000,
          tags: ['Stable Diffusion', 'AI아트', '웹툰'],
          author: {
            name: '웹툰작가',
            avatar: 'https://placehold.co/100x100/0ea5e9/white?text=Avatar'
          }
        }
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
      this.modal.show()
    },
    formatNumber(num) {
      return new Intl.NumberFormat('ko-KR').format(num)
    },
    filterTutorials() {
      // 필터링은 computed property에서 처리됨
    }
  },
  mounted() {
    this.modal = new Modal(document.getElementById('tutorialModal'))
  }
}
</script>

<style scoped>
.tutorials {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 2rem;
}

.search-filters {
  max-width: 1200px;
  margin: 0 auto 2rem;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
}

.card {
  transition: transform 0.2s;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  height: 100%;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.badge {
  padding: 0.5em 1em;
  font-weight: 500;
}

.tutorial-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.tutorial-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.tutorial-stats i {
  margin-right: 0.25rem;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.author-name {
  font-size: 0.875rem;
  color: #4b5563;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0;
}

.tag {
  background: #f3f4f6;
  color: #4b5563;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
}

.level-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 1;
}

.level-입문 { background-color: #10b981; }
.level-중급 { background-color: #f59e0b; }
.level-고급 { background-color: #ef4444; }

.modal-content {
  border: none;
  border-radius: 1rem;
}

.modal-header {
  border-bottom: 1px solid #e5e7eb;
  padding: 1.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.objectives-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.objectives-list li {
  padding-left: 1.5rem;
  position: relative;
  margin-bottom: 0.5rem;
}

.objectives-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #6366f1;
}
</style>

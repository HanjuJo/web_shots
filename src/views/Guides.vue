<template>
  <div class="guides">
    <div class="container py-5">
      <h1 class="mb-4">AI 도구 활용 가이드</h1>

      <!-- 카테고리 탭 -->
      <ul class="nav nav-pills mb-4">
        <li class="nav-item" v-for="category in categories" :key="category.id">
          <button 
            class="nav-link me-2" 
            :class="{ active: selectedCategory === category.id }"
            @click="selectedCategory = category.id"
          >
            <i :class="category.icon"></i>
            {{ category.name }}
          </button>
        </li>
      </ul>

      <!-- 가이드 목록 -->
      <div class="row g-4">
        <div v-for="guide in filteredGuides" :key="guide.id" class="col-md-6 col-lg-4">
          <div class="card h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between mb-3">
                <span class="badge bg-primary">{{ guide.category }}</span>
                <span class="text-muted">{{ guide.duration }}</span>
              </div>
              <div class="d-flex align-items-center mb-3">
                <i class="fas fa-graduation-cap text-primary me-2"></i>
                <h5 class="card-title mb-0">{{ guide.title }}</h5>
              </div>
              <p class="card-text">{{ guide.description }}</p>
              <button @click="showGuideModal(guide)" class="btn btn-primary w-100">
                <i class="fas fa-book-reader me-2"></i>
                가이드 보기
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 가이드 모달 -->
      <div class="modal fade" id="guideModal" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-scrollable">
          <div class="modal-content" v-if="selectedGuide">
            <div class="modal-header">
              <h5 class="modal-title">{{ selectedGuide.title }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <img :src="selectedGuide.image" class="img-fluid rounded mb-4" :alt="selectedGuide.title">
              <div class="content" v-html="selectedGuide.content"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GuidesPage',
  data() {
    return {
      selectedCategory: 'all',
      selectedGuide: null,
      categories: [
        { id: 'all', name: '전체', icon: 'fas fa-th' },
        { id: 'beginner', name: '입문', icon: 'fas fa-star' },
        { id: 'intermediate', name: '중급', icon: 'fas fa-star-half-alt' },
        { id: 'advanced', name: '고급', icon: 'fas fa-stars' }
      ],
      guides: [
        {
          id: 1,
          title: 'ChatGPT로 시작하는 AI 글쓰기',
          description: 'ChatGPT를 활용한 효과적인 글쓰기 방법을 알아봅니다.',
          image: '/images/tutorial-1.jpg',
          category: '초급',
          duration: '15분'
        },
        {
          id: 2,
          title: 'Midjourney 마스터하기',
          description: 'Midjourney로 고품질 이미지를 생성하는 방법을 배웁니다.',
          image: '/images/tutorial-2.jpg',
          category: '중급',
          duration: '20분'
        }
      ]
    }
  },
  computed: {
    filteredGuides() {
      if (this.selectedCategory === 'all') {
        return this.guides
      }
      return this.guides.filter(guide => 
        guide.category.toLowerCase() === this.selectedCategory
      )
    }
  },
  methods: {
    showGuideModal(guide) {
      this.selectedGuide = guide
      const modal = new window.bootstrap.Modal(document.getElementById('guideModal'))
      modal.show()
    }
  }
}
</script>

<style scoped>
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

.nav-pills .nav-link {
  color: #6c757d;
  background-color: #f8f9fa;
  border: none;
  margin-bottom: 10px;
}

.nav-pills .nav-link.active {
  background-color: #0d6efd;
  color: white;
}

.modal-body img {
  max-width: 100%;
  height: auto;
}

.modal-body .content {
  font-size: 1.1rem;
  line-height: 1.6;
}

.modal-body h2 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.modal-body h3 {
  margin-top: 1.2rem;
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
}
</style>

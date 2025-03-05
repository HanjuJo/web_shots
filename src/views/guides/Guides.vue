<template>
  <div class="guides-page">
    <!-- 가이드 헤더 -->
    <section class="guides-header">
      <div class="header-content">
        <h1>AI 크리에이터 가이드</h1>
        <p>AI 도구를 활용한 콘텐츠 제작의 모든 것</p>
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="가이드 검색..."
            @input="filterGuides"
          >
        </div>
      </div>
    </section>

    <!-- 카테고리 필터 -->
    <section class="category-filter">
      <button 
        v-for="category in categories" 
        :key="category.id"
        :class="['category-button', { active: selectedCategory === category.id }]"
        @click="selectCategory(category.id)"
      >
        <i :class="category.icon"></i>
        {{ category.name }}
      </button>
    </section>

    <!-- 추천 가이드 -->
    <section class="featured-guides" v-if="featuredGuides.length && !searchQuery">
      <h2>추천 가이드</h2>
      <div class="featured-grid">
        <div 
          v-for="guide in featuredGuides" 
          :key="guide.id"
          class="featured-card"
          @click="goToGuide(guide.id)"
        >
          <img :src="guide.image" :alt="guide.title">
          <div class="featured-content">
            <span class="guide-category">{{ getCategoryName(guide.categoryId) }}</span>
            <h3>{{ guide.title }}</h3>
            <p>{{ guide.description }}</p>
            <div class="guide-meta">
              <span class="author">
                <img :src="guide.author.avatar" :alt="guide.author.name">
                {{ guide.author.name }}
              </span>
              <span class="reading-time">
                <i class="fas fa-clock"></i>
                {{ guide.readingTime }}분
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 가이드 목록 -->
    <section class="guides-grid">
      <div 
        v-for="guide in filteredGuides" 
        :key="guide.id"
        class="guide-card"
        @click="goToGuide(guide.id)"
      >
        <img :src="guide.image" :alt="guide.title" class="guide-image">
        <div class="guide-content">
          <span class="guide-category">{{ getCategoryName(guide.categoryId) }}</span>
          <h3>{{ guide.title }}</h3>
          <p>{{ guide.description }}</p>
          <div class="guide-meta">
            <span class="author">
              <img :src="guide.author.avatar" :alt="guide.author.name">
              {{ guide.author.name }}
            </span>
            <span class="reading-time">
              <i class="fas fa-clock"></i>
              {{ guide.readingTime }}분
            </span>
          </div>
          <div class="guide-tags">
            <span v-for="tag in guide.tags" :key="tag" class="guide-tag">
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- 페이지네이션 -->
    <div class="pagination" v-if="totalPages > 1">
      <button 
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        <i class="fas fa-chevron-left"></i>
      </button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button 
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GuidesView',
  data() {
    return {
      searchQuery: '',
      selectedCategory: null,
      currentPage: 1,
      itemsPerPage: 9,
      categories: [
        { id: 1, name: '시작하기', icon: 'fas fa-rocket' },
        { id: 2, name: '이미지 생성', icon: 'fas fa-image' },
        { id: 3, name: '영상 편집', icon: 'fas fa-video' },
        { id: 4, name: '음성/자막', icon: 'fas fa-microphone' },
        { id: 5, name: '마케팅', icon: 'fas fa-bullhorn' }
      ],
      guides: [
        {
          id: 1,
          title: 'AI 이미지 생성 완벽 가이드',
          description: 'Stable Diffusion과 Midjourney를 활용한 고품질 이미지 생성 방법',
          image: '/images/guides/image-guide.jpg',
          categoryId: 2,
          author: {
            name: '크리에이터J',
            avatar: '/images/avatars/creator-j.jpg'
          },
          readingTime: 15,
          tags: ['이미지 생성', 'Stable Diffusion', 'Midjourney']
        },
        {
          id: 2,
          title: 'AI 음성 더빙 마스터하기',
          description: '자연스러운 AI 음성 더빙으로 영상의 퀄리티를 높이는 방법',
          image: '/images/guides/voice-guide.jpg',
          categoryId: 4,
          author: {
            name: '보이스프로',
            avatar: '/images/avatars/voice-pro.jpg'
          },
          readingTime: 20,
          tags: ['음성 합성', '더빙', 'TTS']
        },
        {
          id: 3,
          title: '초보자를 위한 AI 도구 입문',
          description: 'AI 크리에이터가 되기 위한 첫걸음',
          image: '/images/guides/beginner-guide.jpg',
          categoryId: 1,
          author: {
            name: 'AI튜터',
            avatar: '/images/avatars/ai-tutor.jpg'
          },
          readingTime: 10,
          tags: ['입문', '기초', '시작하기']
        }
      ],
      featuredGuides: [
        {
          id: 4,
          title: 'AI로 수익 창출하기',
          description: 'AI 도구를 활용한 수익화 전략과 성공 사례',
          image: '/images/guides/monetization.jpg',
          categoryId: 5,
          author: {
            name: '마케팅프로',
            avatar: '/images/avatars/marketing-pro.jpg'
          },
          readingTime: 25
        },
        {
          id: 5,
          title: 'AI 영상 편집 워크플로우',
          description: 'AI 도구로 영상 편집 시간 단축하기',
          image: '/images/guides/workflow.jpg',
          categoryId: 3,
          author: {
            name: '영상편집장인',
            avatar: '/images/avatars/editor-pro.jpg'
          },
          readingTime: 30
        }
      ]
    }
  },
  computed: {
    filteredGuides() {
      let filtered = this.guides

      // 검색어 필터링
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(guide => 
          guide.title.toLowerCase().includes(query) ||
          guide.description.toLowerCase().includes(query) ||
          guide.tags?.some(tag => tag.toLowerCase().includes(query))
        )
      }

      // 카테고리 필터링
      if (this.selectedCategory) {
        filtered = filtered.filter(guide => 
          guide.categoryId === this.selectedCategory
        )
      }

      return filtered
    },
    totalPages() {
      return Math.ceil(this.filteredGuides.length / this.itemsPerPage)
    },
    paginatedGuides() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredGuides.slice(start, end)
    }
  },
  methods: {
    filterGuides() {
      this.currentPage = 1
    },
    selectCategory(categoryId) {
      this.selectedCategory = this.selectedCategory === categoryId ? null : categoryId
      this.currentPage = 1
    },
    getCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId)
      return category ? category.name : ''
    },
    goToGuide(guideId) {
      this.$router.push(`/guides/${guideId}`)
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    }
  }
}
</script>

<style scoped>
.guides-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* 가이드 헤더 */
.guides-header {
  background: linear-gradient(135deg, var(--primary-color) 0%, #6366f1 100%);
  border-radius: 20px;
  padding: 4rem 2rem;
  margin-bottom: 3rem;
  text-align: center;
  color: white;
}

.header-content h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.header-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.search-box {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-box input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
}

/* 카테고리 필터 */
.category-filter {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.category-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.category-button i {
  font-size: 1.1rem;
}

.category-button.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* 추천 가이드 */
.featured-guides {
  margin-bottom: 4rem;
}

.featured-guides h2 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.featured-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.featured-card:hover {
  transform: translateY(-5px);
}

.featured-card img {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.featured-content {
  padding: 1.5rem;
}

/* 가이드 그리드 */
.guides-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.guide-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.guide-card:hover {
  transform: translateY(-5px);
}

.guide-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.guide-content {
  padding: 1.5rem;
}

.guide-category {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border-radius: 15px;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.guide-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.guide-content p {
  color: #666;
  margin-bottom: 1rem;
}

.guide-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.author {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.author img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.reading-time {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #666;
  font-size: 0.875rem;
}

.guide-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.guide-tag {
  padding: 0.25rem 0.75rem;
  background: #f3f4f6;
  border-radius: 15px;
  font-size: 0.875rem;
  color: #666;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination button:not(:disabled):hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .guides-header {
    padding: 3rem 1rem;
  }

  .header-content h1 {
    font-size: 2rem;
  }

  .category-filter {
    padding-bottom: 1rem;
  }

  .featured-grid {
    grid-template-columns: 1fr;
  }

  .guides-grid {
    grid-template-columns: 1fr;
  }
}
</style>

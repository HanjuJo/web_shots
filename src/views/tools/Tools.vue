<template>
  <div class="tools-page">
    <!-- 검색 및 필터 섹션 -->
    <section class="search-section">
      <div class="search-container">
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="AI 도구 검색..."
            @input="filterTools"
          >
        </div>
        <div class="filter-tags">
          <button 
            v-for="category in categories" 
            :key="category.id"
            :class="['filter-tag', { active: selectedCategories.includes(category.id) }]"
            @click="toggleCategory(category.id)"
          >
            {{ category.name }}
          </button>
        </div>
      </div>
    </section>

    <!-- 도구 그리드 -->
    <section class="tools-grid">
      <div 
        v-for="tool in filteredTools" 
        :key="tool.id" 
        class="tool-card"
        @click="goToToolDetail(tool.id)"
      >
        <div class="tool-image">
          <img :src="tool.image" :alt="tool.name">
          <span class="tool-category">{{ getCategoryName(tool.categoryId) }}</span>
        </div>
        <div class="tool-content">
          <h3>{{ tool.name }}</h3>
          <p>{{ tool.description }}</p>
          <div class="tool-meta">
            <span class="tool-rating">
              <i class="fas fa-star"></i>
              {{ tool.rating }}
            </span>
            <span class="tool-reviews">
              {{ tool.reviewCount }}개의 리뷰
            </span>
          </div>
          <div class="tool-tags">
            <span v-for="tag in tool.tags" :key="tag" class="tool-tag">
              {{ tag }}
            </span>
          </div>
          <div class="tool-buttons">
            <a :href="tool.websiteUrl" target="_blank" class="use-tool-btn">
              <i class="fas fa-external-link-alt"></i>
              도구 사용하기
            </a>
            <router-link :to="{ name: 'GuideDetail', params: { id: tool.guideId || tool.id }}" class="guide-btn">
              <i class="fas fa-book"></i>
              사용 가이드
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 추천 도구 섹션 -->
    <section class="featured-tools" v-if="featuredTools.length">
      <h2>추천 AI 도구</h2>
      <div class="featured-grid">
        <div 
          v-for="tool in featuredTools" 
          :key="tool.id"
          class="featured-card"
          @click="goToToolDetail(tool.id)"
        >
          <img :src="tool.image" :alt="tool.name">
          <div class="featured-content">
            <h3>{{ tool.name }}</h3>
            <p>{{ tool.description }}</p>
            <div class="featured-buttons">
              <a :href="tool.websiteUrl" target="_blank" class="try-button">
                <i class="fas fa-external-link-alt"></i>
                지금 사용해보기
              </a>
              <router-link :to="{ name: 'GuideDetail', params: { id: tool.guideId || tool.id }}" class="guide-button">
                <i class="fas fa-book"></i>
                사용 가이드
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'ToolsView',
  data() {
    return {
      searchQuery: '',
      selectedCategories: [],
      categories: [
        { id: 1, name: '이미지 생성' },
        { id: 2, name: '음성 합성' },
        { id: 3, name: '영상 편집' },
        { id: 4, name: '텍스트 생성' },
        { id: 5, name: '번역' },
        { id: 6, name: '자막 생성' }
      ],
      tools: [
        {
          id: 1,
          name: 'AI 이미지 메이커',
          description: '고품질 AI 이미지를 빠르고 쉽게 생성하세요',
          image: '/images/tools/image-maker.jpg',
          categoryId: 1,
          rating: 4.8,
          reviewCount: 1234,
          tags: ['Stable Diffusion', '이미지 생성', '아트'],
          websiteUrl: 'https://example.com/ai-image-maker',
          guideId: 101
        },
        {
          id: 2,
          name: 'AI 보이스',
          description: '자연스러운 AI 음성으로 나레이션을 제작하세요',
          image: '/images/tools/voice-maker.jpg',
          categoryId: 2,
          rating: 4.7,
          reviewCount: 892,
          tags: ['음성 합성', 'TTS', '나레이션'],
          websiteUrl: 'https://example.com/ai-voice',
          guideId: 102
        },
        {
          id: 3,
          name: 'AI 비디오 에디터',
          description: '원클릭으로 전문적인 영상을 편집하세요',
          image: '/images/tools/video-editor.jpg',
          categoryId: 3,
          rating: 4.6,
          reviewCount: 567,
          tags: ['영상 편집', '자동 편집', '트랜지션'],
          websiteUrl: 'https://example.com/ai-video-editor',
          guideId: 103
        },
        {
          id: 4,
          name: 'AI 글쓰기 도우미',
          description: '블로그, 광고, 소셜 미디어 등 다양한 콘텐츠를 AI로 작성하세요',
          image: '/images/tools/text-generator.jpg',
          categoryId: 4,
          rating: 4.9,
          reviewCount: 1543,
          tags: ['콘텐츠 생성', '카피라이팅', 'SEO'],
          websiteUrl: 'https://example.com/ai-writing-assistant',
          guideId: 104
        },
        {
          id: 5,
          name: 'AI 번역기',
          description: '100개 이상의 언어를 자연스럽게 번역하는 AI 도구',
          image: '/images/tools/translator.jpg',
          categoryId: 5,
          rating: 4.8,
          reviewCount: 2134,
          tags: ['번역', '다국어', '글로벌'],
          websiteUrl: 'https://example.com/ai-translator',
          guideId: 105
        },
        {
          id: 6,
          name: 'AI 자막 생성기',
          description: '영상에 자동으로 정확한 자막을 생성하고 번역까지 가능한 AI 도구',
          image: '/images/tools/subtitle-generator.jpg',
          categoryId: 6,
          rating: 4.7,
          reviewCount: 876,
          tags: ['자막', 'STT', '영상 접근성'],
          websiteUrl: 'https://example.com/ai-subtitle-generator',
          guideId: 106
        }
      ],
      featuredTools: [
        {
          id: 1,
          name: 'AI 이미지 메이커',
          description: '고품질 AI 이미지를 빠르고 쉽게 생성하세요',
          image: '/images/tools/image-maker.jpg',
          websiteUrl: 'https://example.com/ai-image-maker',
          guideId: 101
        },
        {
          id: 4,
          name: 'AI 글쓰기 도우미',
          description: '블로그, 광고, 소셜 미디어 등 다양한 콘텐츠를 AI로 작성하세요',
          image: '/images/tools/text-generator.jpg',
          websiteUrl: 'https://example.com/ai-writing-assistant',
          guideId: 104
        }
      ]
    }
  },
  computed: {
    filteredTools() {
      let filtered = this.tools

      // 검색어로 필터링
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(tool => 
          tool.name.toLowerCase().includes(query) || 
          tool.description.toLowerCase().includes(query) ||
          tool.tags.some(tag => tag.toLowerCase().includes(query))
        )
      }

      // 카테고리로 필터링
      if (this.selectedCategories.length > 0) {
        filtered = filtered.filter(tool => 
          this.selectedCategories.includes(tool.categoryId)
        )
      }

      return filtered
    }
  },
  methods: {
    filterTools() {
      // 이벤트 핸들러 (실제 필터링은 computed에서 처리)
    },
    toggleCategory(categoryId) {
      const index = this.selectedCategories.indexOf(categoryId)
      if (index === -1) {
        this.selectedCategories.push(categoryId)
      } else {
        this.selectedCategories.splice(index, 1)
      }
    },
    getCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId)
      return category ? category.name : ''
    },
    goToToolDetail(toolId) {
      this.$router.push(`/tools/${toolId}`)
    }
  }
}
</script>

<style scoped>
.tools-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.search-section {
  margin-bottom: 2.5rem;
}

.search-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.search-box {
  position: relative;
  margin-bottom: 1.5rem;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 1.1rem;
}

.search-box input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 1px solid #eee;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #f9f9f9;
}

.search-box input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(var(--primary-color-rgb), 0.1);
  background: white;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.filter-tag {
  padding: 0.5rem 1rem;
  border: 1px solid #eee;
  border-radius: 24px;
  background: white;
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-tag:hover {
  background: #f5f5f5;
  border-color: #ddd;
}

.filter-tag.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.tool-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.tool-image {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 180px;
}

.tool-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.tool-card:hover .tool-image img {
  transform: scale(1.05);
}

.tool-category {
  position: absolute;
  top: 1rem;
  left: 1rem;
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  z-index: 2;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tool-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.tool-content h3 {
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  line-height: 1.4;
  font-weight: 600;
  color: #333;
}

.tool-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 0.95rem;
}

.tool-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
}

.tool-rating {
  color: #FFB900;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 500;
}

.tool-reviews {
  color: #777;
}

.tool-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tool-tag {
  padding: 0.2rem 0.5rem;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #666;
}

.tool-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-top: auto;
}

.use-tool-btn, .guide-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 0.5rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
}

.use-tool-btn {
  background: var(--primary-color);
  color: white;
}

.use-tool-btn:hover {
  background: var(--primary-color-dark, #0056b3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.guide-btn {
  background: #f5f5f5;
  color: #555;
  border: 1px solid #eee;
}

.guide-btn:hover {
  background: #eee;
  color: #333;
}

.featured-tools {
  margin-top: 4rem;
  margin-bottom: 3rem;
}

.featured-tools h2 {
  font-size: 1.75rem;
  margin-bottom: 2rem;
  font-weight: 600;
  color: #333;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f5f5f5;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 2rem;
}

.featured-card {
  display: flex;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
}

.featured-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.featured-card img {
  width: 150px;
  height: 150px;
  object-fit: cover;
}

.featured-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.featured-content h3 {
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: #333;
}

.featured-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  flex: 1;
}

.featured-buttons {
  display: flex;
  gap: 1rem;
}

.try-button, .guide-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 0.5rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
}

.try-button {
  background: var(--primary-color);
  color: white;
}

.try-button:hover {
  background: var(--primary-color-dark, #0056b3);
}

.guide-button {
  background: #f5f5f5;
  color: #555;
  border: 1px solid #eee;
}

.guide-button:hover {
  background: #eee;
  color: #333;
}

@media (max-width: 768px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }

  .featured-grid {
    grid-template-columns: 1fr;
  }

  .featured-card {
    flex-direction: column;
  }

  .featured-card img {
    width: 100%;
    height: 200px;
  }

  .tool-buttons {
    grid-template-columns: 1fr;
  }

  .filter-tags {
    gap: 0.5rem;
  }

  .filter-tag {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
}
</style>

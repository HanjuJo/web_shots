<template>
  <div class="features">
    <div class="features-header">
      <h1>AI 크리에이터 도구의 핵심 기능</h1>
      <p>영상 제작의 모든 과정을 AI로 더 쉽고 빠르게</p>
    </div>

    <div class="feature-categories">
      <button 
        v-for="category in categories" 
        :key="category.id"
        :class="['category-btn', { active: selectedCategory === category.id }]"
        @click="selectedCategory = category.id"
      >
        <i :class="category.icon"></i>
        {{ category.name }}
      </button>
    </div>

    <div class="features-grid">
      <div 
        v-for="feature in filteredFeatures" 
        :key="feature.id"
        class="feature-card"
        :class="{ 'coming-soon': feature.comingSoon }"
      >
        <div class="feature-icon">
          <i :class="feature.icon"></i>
        </div>
        <h3>{{ feature.name }}</h3>
        <p>{{ feature.description }}</p>
        <div class="feature-footer">
          <span v-if="feature.comingSoon" class="coming-soon-badge">
            Coming Soon
          </span>
          <router-link 
            v-else 
            :to="feature.link" 
            class="try-button"
          >
            체험하기
            <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
      </div>
    </div>

    <div class="features-cta">
      <div class="cta-content">
        <h2>프리미엄 기능 더 알아보기</h2>
        <p>모든 기능을 무제한으로 사용하고 싶다면 프리미엄 멤버가 되어보세요</p>
        <router-link to="/premium" class="cta-button">
          프리미엄 혜택 보기
          <i class="fas fa-crown"></i>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FeatureList',
  data() {
    return {
      selectedCategory: 'all',
      categories: [
        { id: 'all', name: '전체', icon: 'fas fa-th-large' },
        { id: 'video', name: '영상 편집', icon: 'fas fa-video' },
        { id: 'audio', name: '음성/음악', icon: 'fas fa-music' },
        { id: 'text', name: '텍스트/자막', icon: 'fas fa-closed-captioning' },
        { id: 'thumbnail', name: '썸네일', icon: 'fas fa-image' }
      ],
      features: [
        {
          id: 1,
          name: 'AI 자동 편집',
          description: '긴 영상을 자동으로 분석하여 하이라이트 장면을 추출하고 숏폼 영상으로 편집해줍니다.',
          icon: 'fas fa-cut',
          category: 'video',
          link: '/editor'
        },
        {
          id: 2,
          name: '음성 합성',
          description: '자연스러운 AI 보이스로 나레이션을 생성하고 감정과 톤을 조절할 수 있습니다.',
          icon: 'fas fa-microphone',
          category: 'audio',
          link: '/try-ai'
        },
        {
          id: 3,
          name: '자동 자막 생성',
          description: '영상의 음성을 자동으로 인식하여 정확한 자막을 생성하고 여러 언어로 번역합니다.',
          icon: 'fas fa-closed-captioning',
          category: 'text',
          link: '/editor'
        },
        {
          id: 4,
          name: 'AI 썸네일 생성',
          description: '영상 내용을 분석하여 매력적인 썸네일을 자동으로 생성하고 A/B 테스트를 수행합니다.',
          icon: 'fas fa-image',
          category: 'thumbnail',
          link: '/try-ai'
        },
        {
          id: 5,
          name: '배경음악 추천',
          description: '영상의 분위기를 분석하여 최적의 배경음악을 추천하고 자동으로 믹싱합니다.',
          icon: 'fas fa-music',
          category: 'audio',
          link: '/editor'
        },
        {
          id: 6,
          name: '스크립트 생성',
          description: '키워드만 입력하면 AI가 영상 스크립트를 자동으로 생성해줍니다.',
          icon: 'fas fa-pen-fancy',
          category: 'text',
          link: '/try-ai'
        },
        {
          id: 7,
          name: '장면 전환 효과',
          description: 'AI가 영상 내용에 맞는 자연스러운 장면 전환 효과를 추천하고 적용합니다.',
          icon: 'fas fa-film',
          category: 'video',
          link: '/editor'
        },
        {
          id: 8,
          name: '썸네일 최적화',
          description: 'AI가 클릭률이 높은 썸네일 디자인을 분석하여 최적의 썸네일을 제안합니다.',
          icon: 'fas fa-chart-line',
          category: 'thumbnail',
          comingSoon: true
        }
      ]
    }
  },
  computed: {
    filteredFeatures() {
      if (this.selectedCategory === 'all') {
        return this.features
      }
      return this.features.filter(feature => feature.category === this.selectedCategory)
    }
  }
}
</script>

<style scoped>
.features {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.features-header {
  text-align: center;
  margin-bottom: 3rem;
}

.features-header h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.features-header p {
  font-size: 1.1rem;
  color: var(--text-secondary);
}

.feature-categories {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
}

.category-btn {
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 2rem;
  background: white;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.category-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.category-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.feature-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

.feature-icon {
  width: 3rem;
  height: 3rem;
  background: var(--primary-color);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.feature-icon i {
  font-size: 1.5rem;
  color: white;
}

.feature-card h3 {
  font-size: 1.25rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.feature-card p {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.feature-footer {
  margin-top: auto;
}

.try-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.try-button:hover {
  color: var(--primary-dark);
}

.try-button i {
  transition: transform 0.3s ease;
}

.try-button:hover i {
  transform: translateX(4px);
}

.coming-soon {
  opacity: 0.7;
}

.coming-soon-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  color: var(--text-secondary);
  border-radius: 1rem;
  font-size: 0.875rem;
}

.features-cta {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  border-radius: 1rem;
  padding: 3rem;
  text-align: center;
  color: white;
}

.cta-content h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.cta-content p {
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  color: var(--primary-color);
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

@media (max-width: 768px) {
  .features {
    padding: 1rem;
  }

  .features-header h1 {
    font-size: 2rem;
  }

  .feature-categories {
    gap: 0.5rem;
  }

  .category-btn {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }

  .features-cta {
    padding: 2rem;
  }

  .cta-content h2 {
    font-size: 1.5rem;
  }
}
</style>
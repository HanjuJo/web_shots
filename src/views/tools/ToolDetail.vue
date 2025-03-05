<template>
  <div class="tool-detail">
    <div class="tool-header">
      <div class="tool-info">
        <h1>{{ tool.name }}</h1>
        <div class="tool-meta">
          <span class="tool-category">{{ tool.category }}</span>
          <span class="tool-rating">
            <i class="fas fa-star"></i>
            {{ tool.rating }}
          </span>
        </div>
        <p class="tool-description">{{ tool.description }}</p>
      </div>
      <div class="tool-actions">
        <a :href="tool.url" target="_blank" class="primary-button">
          <i class="fas fa-external-link-alt"></i>
          도구 사용하기
        </a>
        <button class="secondary-button" @click="toggleBookmark">
          <i :class="['fas', isBookmarked ? 'fa-bookmark' : 'fa-bookmark-o']"></i>
          북마크
        </button>
      </div>
    </div>

    <div class="tool-content">
      <section class="tool-features">
        <h2>주요 기능</h2>
        <ul>
          <li v-for="feature in tool.features" :key="feature">
            <i class="fas fa-check"></i>
            {{ feature }}
          </li>
        </ul>
      </section>

      <section class="tool-usage">
        <h2>사용 방법</h2>
        <div class="usage-steps">
          <div v-for="(step, index) in tool.usageSteps" :key="index" class="step">
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-content">
              <h3>{{ step.title }}</h3>
              <p>{{ step.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="tool-reviews">
        <div class="reviews-header">
          <h2>사용자 리뷰</h2>
          <button class="write-review-button" @click="openReviewModal">
            리뷰 작성
          </button>
        </div>
        
        <div class="reviews-list">
          <article v-for="review in tool.reviews" :key="review.id" class="review">
            <div class="review-header">
              <div class="reviewer-info">
                <img :src="review.author.avatar" :alt="review.author.name">
                <div>
                  <strong>{{ review.author.name }}</strong>
                  <div class="review-rating">
                    <i v-for="n in 5" :key="n" 
                       :class="['fas', n <= review.rating ? 'fa-star' : 'fa-star-o']">
                    </i>
                  </div>
                </div>
              </div>
              <span class="review-date">{{ formatDate(review.date) }}</span>
            </div>
            <p class="review-content">{{ review.content }}</p>
          </article>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ToolDetail',
  data() {
    return {
      isBookmarked: false,
      tool: {
        name: 'AI 이미지 생성기',
        category: '이미지 생성',
        rating: 4.8,
        description: '최신 AI 기술을 활용한 고품질 이미지 생성 도구입니다. 자연스러운 이미지 생성과 다양한 스타일 적용이 가능합니다.',
        url: 'https://example.com/tool',
        features: [
          '고품질 이미지 생성',
          '다양한 스타일 프리셋',
          '빠른 처리 속도',
          '직관적인 인터페이스',
          '커스텀 설정 지원'
        ],
        usageSteps: [
          {
            title: '프롬프트 입력',
            description: '원하는 이미지를 설명하는 프롬프트를 입력하세요.'
          },
          {
            title: '스타일 선택',
            description: '제공되는 스타일 중에서 원하는 스타일을 선택하세요.'
          },
          {
            title: '설정 조정',
            description: '이미지 크기, 품질 등 세부 설정을 조정하세요.'
          },
          {
            title: '이미지 생성',
            description: '생성 버튼을 클릭하고 결과를 확인하세요.'
          }
        ],
        reviews: [
          {
            id: 1,
            author: {
              name: '김창작',
              avatar: '/images/avatars/user1.jpg'
            },
            rating: 5,
            date: new Date(2025, 2, 1),
            content: '정말 놀라운 퀄리티의 이미지를 생성해냅니다. UI도 직관적이고 사용하기 편리해요.'
          },
          {
            id: 2,
            author: {
              name: '이디자인',
              avatar: '/images/avatars/user2.jpg'
            },
            rating: 4,
            date: new Date(2025, 2, 3),
            content: '작업 시간을 크게 단축시켜주는 훌륭한 도구입니다. 다만 가끔 서버가 불안정한 점이 아쉽네요.'
          }
        ]
      }
    }
  },
  methods: {
    toggleBookmark() {
      this.isBookmarked = !this.isBookmarked
    },
    openReviewModal() {
      // 리뷰 작성 모달 구현
    },
    formatDate(date) {
      return new Intl.DateTimeFormat('ko-KR').format(date)
    }
  }
}
</script>

<style scoped>
.tool-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.tool-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
}

.tool-info {
  flex: 1;
}

.tool-info h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.tool-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.tool-category {
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border-radius: 15px;
  font-size: 0.875rem;
}

.tool-rating {
  color: #ffc107;
}

.tool-description {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
}

.tool-actions {
  display: flex;
  gap: 1rem;
}

.primary-button,
.secondary-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-button {
  background: var(--primary-color);
  color: white;
  border: none;
}

.secondary-button {
  background: white;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.tool-content {
  display: grid;
  gap: 3rem;
}

.tool-features h2,
.tool-usage h2,
.tool-reviews h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.tool-features ul {
  list-style: none;
  padding: 0;
}

.tool-features li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.tool-features li i {
  color: var(--primary-color);
}

.usage-steps {
  display: grid;
  gap: 2rem;
}

.step {
  display: flex;
  gap: 1.5rem;
}

.step-number {
  width: 40px;
  height: 40px;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
}

.step-content h3 {
  margin-bottom: 0.5rem;
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.write-review-button {
  padding: 0.5rem 1rem;
  background: white;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.write-review-button:hover {
  background: var(--primary-color);
  color: white;
}

.reviews-list {
  display: grid;
  gap: 2rem;
}

.review {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.reviewer-info img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.review-rating {
  color: #ffc107;
  margin-top: 0.25rem;
}

.review-date {
  color: #666;
  font-size: 0.875rem;
}

.review-content {
  color: #333;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .tool-header {
    flex-direction: column;
    gap: 2rem;
  }

  .tool-actions {
    width: 100%;
  }

  .primary-button,
  .secondary-button {
    flex: 1;
    justify-content: center;
  }
}
</style>

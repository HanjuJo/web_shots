<template>
  <div class="tool-detail">
    <div class="container py-5">
      <div v-if="tool">
        <!-- 헤더 섹션 -->
        <div class="header mb-5">
          <div class="row align-items-center">
            <div class="col-md-8">
              <div class="d-flex align-items-center mb-3">
                <img :src="tool.logo" :alt="tool.name" class="tool-logo me-3">
                <h1 class="mb-0">{{ tool.name }}</h1>
              </div>
              <p class="lead mb-3">{{ tool.description }}</p>
              <div class="tags mb-3">
                <span v-for="tag in tool.tags" :key="tag" class="badge bg-light text-dark me-2">
                  {{ tag }}
                </span>
              </div>
              <div class="d-flex align-items-center">
                <a :href="tool.website" target="_blank" class="btn btn-primary me-3">
                  <i class="fas fa-external-link-alt me-2"></i>웹사이트 방문
                </a>
                <button class="btn btn-outline-primary me-3" @click="toggleBookmark">
                  <i :class="['far', isBookmarked ? 'fas fa-bookmark' : 'far fa-bookmark']"></i>
                </button>
                <div class="rating ms-3">
                  <i v-for="n in 5" :key="n" 
                     :class="['fas fa-star', n <= tool.rating ? 'text-warning' : 'text-muted']"
                  ></i>
                  <span class="ms-2">({{ tool.reviewCount }})</span>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">가격 정보</h5>
                  <div class="pricing-info">
                    <div v-for="plan in tool.pricing" :key="plan.name" class="mb-3">
                      <h6>{{ plan.name }}</h6>
                      <div class="d-flex justify-content-between">
                        <span>{{ plan.price }}</span>
                        <span class="text-muted">{{ plan.period }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 탭 네비게이션 -->
        <ul class="nav nav-tabs mb-4">
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'features' }"
                    @click="activeTab = 'features'">
              주요 기능
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'tutorial' }"
                    @click="activeTab = 'tutorial'">
              사용 방법
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'reviews' }"
                    @click="activeTab = 'reviews'">
              리뷰
            </button>
          </li>
        </ul>

        <!-- 탭 컨텐츠 -->
        <div class="tab-content">
          <!-- 주요 기능 탭 -->
          <div v-show="activeTab === 'features'" class="features">
            <div class="row g-4">
              <div v-for="feature in tool.features" :key="feature.title" class="col-md-6">
                <div class="card h-100">
                  <div class="card-body">
                    <div class="d-flex align-items-center mb-3">
                      <i :class="feature.icon + ' fa-2x text-primary me-3'"></i>
                      <h5 class="card-title mb-0">{{ feature.title }}</h5>
                    </div>
                    <p class="card-text">{{ feature.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 사용 방법 탭 -->
          <div v-show="activeTab === 'tutorial'" class="tutorial">
            <div class="steps">
              <div v-for="(step, index) in tool.tutorial" :key="index" class="step mb-5">
                <h4>Step {{ index + 1 }}: {{ step.title }}</h4>
                <p>{{ step.description }}</p>
                <img v-if="step.image" :src="step.image" class="img-fluid rounded" :alt="step.title">
              </div>
            </div>
          </div>

          <!-- 리뷰 탭 -->
          <div v-show="activeTab === 'reviews'" class="reviews">
            <div class="review-summary card mb-4">
              <div class="card-body">
                <div class="row align-items-center">
                  <div class="col-md-4 text-center">
                    <h2 class="display-4">{{ tool.rating }}/5</h2>
                    <div class="rating mb-2">
                      <i v-for="n in 5" :key="n" 
                         :class="['fas fa-star', n <= tool.rating ? 'text-warning' : 'text-muted']"
                      ></i>
                    </div>
                    <p class="text-muted">{{ tool.reviewCount }} 리뷰</p>
                  </div>
                  <div class="col-md-8">
                    <div v-for="n in 5" :key="n" class="rating-bar mb-2">
                      <div class="d-flex align-items-center">
                        <span class="me-2">{{ 6-n }}점</span>
                        <div class="progress flex-grow-1">
                          <div class="progress-bar bg-warning" 
                               :style="{ width: (tool.ratingDistribution[5-n] / tool.reviewCount * 100) + '%' }">
                          </div>
                        </div>
                        <span class="ms-2">{{ tool.ratingDistribution[5-n] }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="review-list">
              <div v-for="review in tool.reviews" :key="review.id" class="card mb-3">
                <div class="card-body">
                  <div class="d-flex justify-content-between mb-3">
                    <div class="user-info d-flex align-items-center">
                      <img :src="review.author.avatar" class="rounded-circle me-2" width="40" height="40">
                      <div>
                        <h6 class="mb-0">{{ review.author.name }}</h6>
                        <small class="text-muted">{{ review.date }}</small>
                      </div>
                    </div>
                    <div class="rating">
                      <i v-for="n in 5" :key="n" 
                         :class="['fas fa-star', n <= review.rating ? 'text-warning' : 'text-muted']"
                      ></i>
                    </div>
                  </div>
                  <h6 class="review-title">{{ review.title }}</h6>
                  <p class="review-text">{{ review.content }}</p>
                  <div v-if="review.images && review.images.length" class="review-images mb-3">
                    <div class="row g-2">
                      <div v-for="image in review.images" :key="image" class="col-4">
                        <img :src="image" class="img-fluid rounded" :alt="review.title">
                      </div>
                    </div>
                  </div>
                  <div class="review-actions">
                    <button class="btn btn-sm btn-link text-muted me-3" @click="likeReview(review)">
                      <i :class="['far', review.isLiked ? 'fas fa-thumbs-up' : 'far fa-thumbs-up']"></i>
                      도움됨 ({{ review.likes }})
                    </button>
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
  name: 'ToolDetail',
  data() {
    return {
      activeTab: 'features',
      isBookmarked: false,
      tool: {
        id: 1,
        name: 'Midjourney',
        description: '고품질 AI 이미지 생성 도구',
        logo: require('@/assets/midjourney-logo.png'),
        tags: ['이미지 생성', 'AI 아트', '일러스트레이션'],
        website: 'https://midjourney.com',
        rating: 4.8,
        reviewCount: 1280,
        pricing: [
          {
            name: '기본 요금제',
            price: '$10/월',
            period: '월간'
          },
          {
            name: '프로 요금제',
            price: '$30/월',
            period: '월간'
          }
        ],
        features: [
          {
            title: '고품질 이미지 생성',
            description: '최첨단 AI 기술을 사용하여 고품질의 이미지를 생성합니다.',
            icon: 'fas fa-image'
          },
          {
            title: '다양한 스타일',
            description: '수천 가지의 아트 스타일과 테마를 지원합니다.',
            icon: 'fas fa-palette'
          },
          {
            title: '빠른 생성 속도',
            description: '몇 초 만에 고품질 이미지를 생성할 수 있습니다.',
            icon: 'fas fa-bolt'
          },
          {
            title: '커뮤니티 기반',
            description: '전 세계 크리에이터들과 아이디어를 공유할 수 있습니다.',
            icon: 'fas fa-users'
          }
        ],
        tutorial: [
          {
            title: 'Discord 서버 가입하기',
            description: 'Midjourney Discord 서버에 가입하여 시작합니다.',
            image: require('@/assets/tutorial-1.jpg')
          },
          {
            title: '기본 명령어 사용하기',
            description: '/imagine 명령어를 사용하여 이미지를 생성합니다.',
            image: require('@/assets/tutorial-2.jpg')
          }
        ],
        ratingDistribution: [800, 300, 100, 50, 30],
        reviews: [
          {
            id: 1,
            author: {
              name: '디자인러버',
              avatar: require('@/assets/avatar-1.jpg')
            },
            rating: 5,
            title: '놀라운 퀄리티!',
            content: '처음 사용해봤는데 정말 놀라운 퀄리티의 이미지가 나왔습니다. 프롬프트 작성법만 잘 익히면 원하는 이미지를 거의 완벽하게 만들 수 있어요.',
            date: '2025-03-02',
            likes: 24,
            isLiked: false,
            images: [
              require('@/assets/review-1-1.jpg'),
              require('@/assets/review-1-2.jpg')
            ]
          }
        ]
      }
    }
  },
  methods: {
    toggleBookmark() {
      this.isBookmarked = !this.isBookmarked
    },
    likeReview(review) {
      review.isLiked = !review.isLiked
      review.likes += review.isLiked ? 1 : -1
    }
  }
}
</script>

<style scoped>
.tool-logo {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.nav-tabs .nav-link {
  color: #6c757d;
  border: none;
  padding: 1rem 1.5rem;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  border-bottom: 2px solid #0d6efd;
}

.rating-bar .progress {
  height: 8px;
}

.review-images img {
  height: 150px;
  object-fit: cover;
}

.user-info img {
  object-fit: cover;
}

.btn-link {
  text-decoration: none;
}
</style>

<template>
  <div class="trends">
    <div class="container py-5">
      <h1 class="mb-4">AI 트렌드</h1>
      
      <!-- 트렌드 필터 -->
      <div class="filters mb-4">
        <div class="row g-3">
          <div class="col-md-4">
            <select v-model="selectedCategory" class="form-select">
              <option value="">모든 카테고리</option>
              <option value="image">이미지</option>
              <option value="video">비디오</option>
              <option value="audio">오디오</option>
              <option value="text">텍스트</option>
            </select>
          </div>
          <div class="col-md-4">
            <select v-model="sortBy" class="form-select">
              <option value="date">최신순</option>
              <option value="popularity">인기순</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 트렌드 그리드 -->
      <div class="row g-4">
        <div class="col-md-4" v-for="trend in filteredTrends" :key="trend.id">
          <div class="card h-100">
            <div class="card-body">
              <div class="d-flex align-items-center mb-3">
                <i class="fas fa-chart-line text-primary me-2"></i>
                <span class="badge bg-primary">{{ trend.category }}</span>
              </div>
              <h5 class="card-title">{{ trend.title }}</h5>
              <p class="card-text">{{ trend.description }}</p>
              <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">{{ trend.date }}</small>
                <div>
                  <span class="me-3">
                    <i class="far fa-eye"></i>
                    {{ trend.views }}
                  </span>
                  <span>
                    <i class="far fa-heart"></i>
                    {{ trend.likes }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 더보기 버튼 -->
      <div class="text-center mt-5">
        <button @click="loadMore" class="btn btn-primary btn-lg" :disabled="loading">
          <span v-if="loading">
            <span class="spinner-border spinner-border-sm me-2"></span>
            로딩중...
          </span>
          <span v-else>더보기</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrendsPage',
  data() {
    return {
      selectedCategory: '',
      sortBy: 'date',
      loading: false,
      trends: [
        {
          id: 1,
          title: '이미지 생성 AI의 발전',
          description: '이미지 생성 AI 기술의 최신 트렌드와 발전 방향을 알아봅니다.',
          image: '/images/trend-1.jpg',
          category: 'AI 기술',
          date: '2025-03-03',
          views: 1200,
          likes: 340
        },
        {
          id: 2,
          title: '크리에이터 경제의 성장',
          description: 'AI 도구를 활용한 크리에이터 경제의 성장과 기회',
          image: '/images/trend-2.jpg',
          category: '시장 동향',
          date: '2025-03-02',
          views: 980,
          likes: 250
        },
        {
          id: 3,
          title: '생성형 AI의 미래',
          description: '생성형 AI가 가져올 미래의 변화와 영향',
          image: '/images/trend-3.jpg',
          category: '미래 전망',
          date: '2025-03-01',
          views: 850,
          likes: 180
        }
      ]
    }
  },
  computed: {
    filteredTrends() {
      let result = [...this.trends]
      
      if (this.selectedCategory) {
        result = result.filter(trend => trend.category === this.selectedCategory)
      }
      
      if (this.sortBy === 'date') {
        result.sort((a, b) => new Date(b.date) - new Date(a.date))
      } else if (this.sortBy === 'popularity') {
        result.sort((a, b) => b.views - a.views)
      }
      
      return result
    }
  },
  methods: {
    async loadMore() {
      this.loading = true
      // TODO: API 호출하여 추가 트렌드 데이터 로드
      await new Promise(resolve => setTimeout(resolve, 1000))
      this.loading = false
    },
    shareTrend(trend) {
      // TODO: 공유 기능 구현
      alert(`'${trend.title}' 공유하기`)
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

.stats {
  color: #6c757d;
  font-size: 0.9rem;
}

.badge {
  font-size: 0.8rem;
  padding: 0.5em 0.8em;
}
</style>

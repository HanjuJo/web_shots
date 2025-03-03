<template>
  <div class="youtube-analytics container mt-4">
    <h2 class="text-center mb-4">
      <i class="fas fa-youtube text-danger me-2"></i>
      유튜브 콘텐츠 분석
    </h2>

    <!-- 분석 유형 선택 -->
    <div class="analysis-type-selector mb-4">
      <div class="btn-group w-100" role="group">
        <button 
          :class="['btn', analysisType === 'shorts' ? 'btn-primary' : 'btn-outline-primary']"
          @click="analysisType = 'shorts'">
          쇼츠 분석
        </button>
        <button 
          :class="['btn', analysisType === 'videos' ? 'btn-primary' : 'btn-outline-primary']"
          @click="analysisType = 'videos'">
          일반 영상 분석
        </button>
      </div>
    </div>

    <!-- 검색 입력 -->
    <div class="search-section mb-4">
      <div class="input-group">
        <input 
          type="text" 
          class="form-control" 
          v-model="keyword"
          :placeholder="analysisType === 'shorts' ? '쇼츠 검색 키워드 입력...' : '영상 검색 키워드 입력...'"
          @keyup.enter="startAnalysis">
        <button 
          class="btn btn-primary" 
          @click="startAnalysis"
          :disabled="loading">
          {{ loading ? '분석 중...' : '분석 시작' }}
        </button>
      </div>
    </div>

    <!-- 로딩 표시 -->
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <!-- 분석 결과 -->
    <div v-if="analysisResults && !loading" class="analysis-results">
      <!-- 통계 대시보드 (쇼츠 분석일 때만) -->
      <div v-if="analysisType === 'shorts' && analysisResults.statistics" class="statistics-dashboard mb-4">
        <div class="row g-4">
          <div class="col-md-3">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">총 조회수</h5>
                <p class="card-text display-6">{{ formatNumber(analysisResults.statistics.totalViews) }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">평균 조회수</h5>
                <p class="card-text display-6">{{ formatNumber(analysisResults.statistics.averageViews) }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">평균 참여율</h5>
                <p class="card-text display-6">{{ analysisResults.statistics.averageEngagement }}%</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">분석된 영상</h5>
                <p class="card-text display-6">{{ analysisResults.statistics.totalVideos }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 인사이트 (쇼츠 분석일 때만) -->
      <div v-if="analysisType === 'shorts' && analysisResults.insights" class="insights mb-4">
        <h3 class="mb-3">📊 주요 인사이트</h3>
        <div class="list-group">
          <div v-for="(insight, index) in analysisResults.insights" 
               :key="index" 
               class="list-group-item">
            {{ insight }}
          </div>
        </div>
      </div>

      <!-- 인기 해시태그 (쇼츠 분석일 때만) -->
      <div v-if="analysisType === 'shorts' && analysisResults.statistics.popularHashtags" class="hashtags mb-4">
        <h3 class="mb-3">🏷 인기 해시태그</h3>
        <div class="d-flex flex-wrap gap-2">
          <span v-for="(count, tag) in analysisResults.statistics.popularHashtags" 
                :key="tag" 
                class="badge bg-primary fs-6">
            {{ tag }} ({{ count }})
          </span>
        </div>
      </div>

      <!-- 영상 목록 -->
      <div class="videos-grid">
        <h3 class="mb-3">🎬 분석된 영상</h3>
        <div class="row g-4">
          <div v-for="video in getVideos" 
               :key="video.url" 
               class="col-md-6 col-lg-4">
            <div class="card h-100">
              <img :src="video.thumbnail" class="card-img-top" :alt="video.title">
              <div class="card-body">
                <h5 class="card-title">{{ video.title }}</h5>
                <p class="card-text">
                  <small class="text-muted">
                    채널: {{ video.channelName }}<br>
                    조회수: {{ formatNumber(video.viewCount) }}회
                  </small>
                </p>
                <div v-if="analysisType === 'shorts'" class="mb-2">
                  <span class="badge bg-success me-2">
                    참여율: {{ video.engagementRate }}%
                  </span>
                  <span class="badge bg-info">
                    좋아요: {{ formatNumber(video.likeCount) }}
                  </span>
                </div>
                <a :href="video.url" 
                   target="_blank" 
                   class="btn btn-primary btn-sm">
                  영상 보기
                </a>
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
  name: 'YoutubeAnalytics',
  data() {
    return {
      analysisType: 'shorts',
      keyword: '',
      loading: false,
      error: null,
      analysisResults: null
    }
  },
  computed: {
    getVideos() {
      if (!this.analysisResults) return [];
      return this.analysisType === 'shorts' 
        ? this.analysisResults.videos 
        : this.analysisResults;
    }
  },
  methods: {
    async startAnalysis() {
      if (!this.keyword) {
        this.error = '키워드를 입력해주세요';
        return;
      }

      this.loading = true;
      this.error = null;
      this.analysisResults = null;

      try {
        const endpoint = this.analysisType === 'shorts' 
          ? '/api/youtube/shorts-analysis'
          : '/api/youtube/video-analysis';

        const response = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            keyword: this.keyword,
            maxResults: 15
          }),
        });

        if (!response.ok) {
          throw new Error('분석 중 오류가 발생했습니다');
        }

        this.analysisResults = await response.json();
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    formatNumber(num) {
      return new Intl.NumberFormat().format(num);
    }
  }
}
</script>

<style scoped>
.youtube-analytics {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.statistics-dashboard .card {
  text-align: center;
}

.statistics-dashboard .display-6 {
  font-size: 1.5rem;
  font-weight: bold;
  color: #0d6efd;
}

.insights .list-group-item {
  border-left: 4px solid #0d6efd;
}

.badge {
  font-weight: normal;
}
</style>

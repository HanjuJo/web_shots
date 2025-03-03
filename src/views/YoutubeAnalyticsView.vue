<template>
  <div class="container py-5">
    <h2 class="mb-4">유튜브 분석</h2>
    
    <!-- 채널 분석 섹션 -->
    <div class="card mb-4">
      <div class="card-body">
        <h4 class="card-title mb-4">
          <i class="fab fa-youtube text-danger me-2"></i>
          채널 분석
        </h4>
        <div class="mb-3">
          <label class="form-label">유튜브 채널 URL</label>
          <div class="input-group">
            <input type="text" class="form-control" v-model="channelUrl" placeholder="https://youtube.com/c/channel">
            <button class="btn btn-primary" @click="analyzeChannel" :disabled="isAnalyzing">
              <i class="fas fa-search me-2"></i>
              분석하기
            </button>
          </div>
        </div>

        <!-- 채널 통계 -->
        <div v-if="channelStats" class="row g-4">
          <div class="col-md-3">
            <div class="card bg-light">
              <div class="card-body text-center">
                <i class="fas fa-users fa-2x text-primary mb-2"></i>
                <h5>구독자</h5>
                <h3>{{ channelStats.subscribers }}</h3>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card bg-light">
              <div class="card-body text-center">
                <i class="fas fa-video fa-2x text-primary mb-2"></i>
                <h5>총 영상</h5>
                <h3>{{ channelStats.videos }}</h3>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card bg-light">
              <div class="card-body text-center">
                <i class="fas fa-eye fa-2x text-primary mb-2"></i>
                <h5>총 조회수</h5>
                <h3>{{ channelStats.views }}</h3>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card bg-light">
              <div class="card-body text-center">
                <i class="fas fa-chart-line fa-2x text-primary mb-2"></i>
                <h5>월간 성장률</h5>
                <h3>{{ channelStats.growth }}%</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 영상 분석 섹션 -->
    <div class="card mb-4">
      <div class="card-body">
        <h4 class="card-title mb-4">
          <i class="fas fa-chart-bar text-primary me-2"></i>
          영상 성과 분석
        </h4>
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>제목</th>
                <th>업로드일</th>
                <th>조회수</th>
                <th>좋아요</th>
                <th>댓글</th>
                <th>참여율</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="video in videoStats" :key="video.id">
                <td>{{ video.title }}</td>
                <td>{{ video.uploadDate }}</td>
                <td>{{ video.views }}</td>
                <td>{{ video.likes }}</td>
                <td>{{ video.comments }}</td>
                <td>
                  <div class="progress">
                    <div class="progress-bar" role="progressbar" :style="{ width: video.engagementRate + '%' }" :aria-valuenow="video.engagementRate" aria-valuemin="0" aria-valuemax="100">
                      {{ video.engagementRate }}%
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 키워드 분석 섹션 -->
    <div class="card">
      <div class="card-body">
        <h4 class="card-title mb-4">
          <i class="fas fa-tags text-primary me-2"></i>
          키워드 분석
        </h4>
        <div class="row">
          <div class="col-md-6">
            <h5 class="mb-3">인기 태그</h5>
            <div class="d-flex flex-wrap gap-2">
              <span v-for="tag in popularTags" :key="tag.name" class="badge bg-primary p-2">
                {{ tag.name }} ({{ tag.count }})
              </span>
            </div>
          </div>
          <div class="col-md-6">
            <h5 class="mb-3">추천 태그</h5>
            <div class="d-flex flex-wrap gap-2">
              <span v-for="tag in recommendedTags" :key="tag.name" class="badge bg-success p-2">
                {{ tag.name }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'YoutubeAnalyticsView',
  data() {
    return {
      channelUrl: '',
      isAnalyzing: false,
      channelStats: null,
      videoStats: [
        {
          id: 1,
          title: '샘플 영상 1',
          uploadDate: '2025-03-01',
          views: '1.2K',
          likes: '150',
          comments: '45',
          engagementRate: 75
        },
        {
          id: 2,
          title: '샘플 영상 2',
          uploadDate: '2025-02-28',
          views: '2.5K',
          likes: '320',
          comments: '89',
          engagementRate: 85
        }
      ],
      popularTags: [
        { name: '#AI', count: 15 },
        { name: '#프로그래밍', count: 12 },
        { name: '#코딩', count: 10 },
        { name: '#개발자', count: 8 }
      ],
      recommendedTags: [
        { name: '#인공지능' },
        { name: '#머신러닝' },
        { name: '#데이터사이언스' },
        { name: '#파이썬' }
      ]
    }
  },
  methods: {
    async analyzeChannel() {
      this.isAnalyzing = true
      try {
        // 실제 API 호출 대신 임시 데이터
        await new Promise(resolve => setTimeout(resolve, 2000))
        this.channelStats = {
          subscribers: '10.5K',
          videos: '125',
          views: '500K',
          growth: '12.5'
        }
      } catch (error) {
        console.error('채널 분석 오류:', error)
      } finally {
        this.isAnalyzing = false
      }
    }
  }
}
</script>

<style scoped>
.progress {
  height: 20px;
}

.badge {
  font-size: 0.9rem;
}
</style>

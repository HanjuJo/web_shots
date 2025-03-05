<template>
  <div class="channel-view">
    <h1>채널 분석</h1>

    <div class="search-box">
      <input 
        v-model="channelId"
        @keyup.enter="handleAnalyze"
        placeholder="채널 ID를 입력하세요"
        type="text"
      >
      <button @click="handleAnalyze" :disabled="!channelId || loading">
        분석하기
      </button>
    </div>

    <div v-if="loading" class="loading">
      채널을 분석하는 중...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="channelStats" class="channel-content">
      <div class="channel-header">
        <h1>채널 관리</h1>
      </div>
      
      <div class="channel-stats">
        <div class="stat-card">
          <h3>구독자</h3>
          <p class="stat-value">{{ formatNumber(channelStats.subscriber_count) }}</p>
        </div>
        <div class="stat-card">
          <h3>총 조회수</h3>
          <p class="stat-value">{{ formatNumber(channelStats.view_count) }}</p>
        </div>
        <div class="stat-card">
          <h3>동영상</h3>
          <p class="stat-value">{{ formatNumber(channelStats.video_count) }}</p>
        </div>
      </div>
      
      <div class="channel-actions">
        <button class="btn btn-primary" @click="handleAnalyze">
          <i class="fas fa-sync"></i> 새로고침
        </button>
        <button class="btn btn-outline-primary">
          <i class="fas fa-cog"></i> 설정
        </button>
      </div>
      
      <div class="recent-videos">
        <h3>최근 업로드된 동영상</h3>
        <div class="video-grid">
          <div v-for="video in channelStats.recent_videos" :key="video.id" class="video-card">
            <img :src="video.thumbnail_url" :alt="video.title" class="thumbnail">
            <div class="video-info">
              <h4>{{ video.title }}</h4>
              <div class="video-stats">
                <span><i class="fas fa-eye"></i> {{ formatNumber(video.view_count) }}</span>
                <span><i class="fas fa-thumbs-up"></i> {{ formatNumber(video.like_count) }}</span>
                <span><i class="fas fa-comment"></i> {{ formatNumber(video.comment_count) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'ChannelView',
  data() {
    return {
      channelId: ''
    }
  },
  computed: {
    ...mapState(['channelStats', 'loading', 'error'])
  },
  methods: {
    ...mapActions(['analyzeChannel']),
    formatNumber(num) {
      return new Intl.NumberFormat('ko-KR').format(num)
    },
    async handleAnalyze() {
      console.log('Analyzing channel:', this.channelId)
      if (this.channelId && !this.loading) {
        await this.analyzeChannel(this.channelId)
      }
    }
  },
  mounted() {
    console.log('ChannelView mounted')
  }
}
</script>

<style scoped>
.channel-view {
  padding: 20px;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

.search-box input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.search-box button {
  padding: 12px 24px;
  background: #1a73e8;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.2s;
}

.search-box button:hover:not(:disabled) {
  background: #1557b0;
}

.search-box button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #dc3545;
}

.channel-content {
  margin-top: 20px;
}

.channel-header {
  margin-bottom: 30px;
}

.channel-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin: 10px 0;
}

.channel-actions {
  display: flex;
  gap: 10px;
}

.recent-videos {
  margin-top: 30px;
}

.recent-videos h3 {
  margin-bottom: 20px;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.video-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.video-card:hover {
  transform: translateY(-2px);
}

.thumbnail {
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
}

.video-info {
  padding: 15px;
}

.video-info h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  line-height: 1.4;
  height: 2.8em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.video-stats {
  display: flex;
  gap: 15px;
  color: #666;
  font-size: 12px;
}

.video-stats i {
  margin-right: 4px;
}
</style>

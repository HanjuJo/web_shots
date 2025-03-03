&lt;template>
  &lt;div class="channel-view">
    &lt;h1>채널 분석&lt;/h1>

    &lt;div class="search-box">
      &lt;input 
        v-model="channelId"
        @keyup.enter="handleAnalyze"
        placeholder="채널 ID를 입력하세요"
        type="text"
      >
      &lt;button @click="handleAnalyze" :disabled="!channelId || loading">
        분석하기
      &lt;/button>
    &lt;/div>

    &lt;div v-if="loading" class="loading">
      채널을 분석하는 중...
    &lt;/div>

    &lt;div v-else-if="error" class="error">
      {{ error }}
    &lt;/div>

    &lt;div v-else-if="channelStats" class="channel-stats">
      &lt;div class="stats-card">
        &lt;div class="channel-header">
          &lt;img :src="channelStats.thumbnail_url" :alt="channelStats.title" class="channel-avatar">
          &lt;div class="channel-info">
            &lt;h2>{{ channelStats.title }}&lt;/h2>
            &lt;p>{{ channelStats.description }}&lt;/p>
          &lt;/div>
        &lt;/div>

        &lt;div class="stats-grid">
          &lt;div class="stat-item">
            &lt;i class="fas fa-users">&lt;/i>
            &lt;span class="stat-value">{{ formatNumber(channelStats.subscriber_count) }}&lt;/span>
            &lt;span class="stat-label">구독자&lt;/span>
          &lt;/div>
          &lt;div class="stat-item">
            &lt;i class="fas fa-eye">&lt;/i>
            &lt;span class="stat-value">{{ formatNumber(channelStats.view_count) }}&lt;/span>
            &lt;span class="stat-label">총 조회수&lt;/span>
          &lt;/div>
          &lt;div class="stat-item">
            &lt;i class="fas fa-video">&lt;/i>
            &lt;span class="stat-value">{{ formatNumber(channelStats.video_count) }}&lt;/span>
            &lt;span class="stat-label">동영상&lt;/span>
          &lt;/div>
        &lt;/div>
      &lt;/div>

      &lt;div class="recent-videos">
        &lt;h3>최근 업로드된 동영상&lt;/h3>
        &lt;div class="video-grid">
          &lt;div v-for="video in channelStats.recent_videos" :key="video.id" class="video-card">
            &lt;img :src="video.thumbnail_url" :alt="video.title" class="thumbnail">
            &lt;div class="video-info">
              &lt;h4>{{ video.title }}&lt;/h4>
              &lt;div class="video-stats">
                &lt;span>&lt;i class="fas fa-eye">&lt;/i> {{ formatNumber(video.view_count) }}&lt;/span>
                &lt;span>&lt;i class="fas fa-thumbs-up">&lt;/i> {{ formatNumber(video.like_count) }}&lt;/span>
                &lt;span>&lt;i class="fas fa-comment">&lt;/i> {{ formatNumber(video.comment_count) }}&lt;/span>
              &lt;/div>
            &lt;/div>
          &lt;/div>
        &lt;/div>
      &lt;/div>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script>
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
&lt;/script>

&lt;style scoped>
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

.channel-stats {
  margin-top: 20px;
}

.stats-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.channel-header {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.channel-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.channel-info h2 {
  margin: 0 0 10px 0;
}

.channel-info p {
  color: #666;
  margin: 0;
  line-height: 1.4;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-item i {
  font-size: 24px;
  color: #1a73e8;
  margin-bottom: 10px;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  margin: 10px 0;
}

.stat-label {
  color: #666;
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
&lt;/style>

&lt;template>
  &lt;div class="youtube-analyzer">
    &lt;div class="analyzer-header">
      &lt;h1>유튜브 영상 분석기&lt;/h1>
      &lt;p>영상 URL을 입력하면 AI가 자동으로 분석해드립니다&lt;/p>
    &lt;/div>

    &lt;div class="analyzer-input">
      &lt;div class="url-input">
        &lt;input 
          type="text" 
          v-model="videoUrl" 
          placeholder="유튜브 영상 URL을 입력하세요"
          @keyup.enter="analyzeVideo"
        >
        &lt;button @click="analyzeVideo" :disabled="!isValidUrl || loading">
          &lt;i class="fas fa-search" v-if="!loading">&lt;/i>
          &lt;i class="fas fa-spinner fa-spin" v-else>&lt;/i>
          분석하기
        &lt;/button>
      &lt;/div>
      &lt;p class="error" v-if="error">{{ error }}&lt;/p>
    &lt;/div>

    &lt;div v-if="loading" class="loading-state">
      &lt;div class="loading-animation">
        &lt;i class="fas fa-circle-notch fa-spin">&lt;/i>
      &lt;/div>
      &lt;h3>AI가 영상을 분석하고 있습니다&lt;/h3>
      &lt;p>잠시만 기다려주세요...&lt;/p>
    &lt;/div>

    &lt;div v-if="analysisResult" class="analysis-result">
      &lt;div class="video-preview">
        &lt;img :src="analysisResult.thumbnail" :alt="analysisResult.title">
        &lt;div class="video-info">
          &lt;h2>{{ analysisResult.title }}&lt;/h2>
          &lt;p>{{ analysisResult.channelName }}&lt;/p>
        &lt;/div>
      &lt;/div>

      &lt;div class="analysis-sections">
        &lt;div class="section">
          &lt;h3>&lt;i class="fas fa-chart-line">&lt;/i> 주요 지표&lt;/h3>
          &lt;div class="metrics-grid">
            &lt;div class="metric-card">
              &lt;span class="metric-value">{{ analysisResult.metrics.views }}&lt;/span>
              &lt;span class="metric-label">조회수&lt;/span>
            &lt;/div>
            &lt;div class="metric-card">
              &lt;span class="metric-value">{{ analysisResult.metrics.likes }}&lt;/span>
              &lt;span class="metric-label">좋아요&lt;/span>
            &lt;/div>
            &lt;div class="metric-card">
              &lt;span class="metric-value">{{ analysisResult.metrics.comments }}&lt;/span>
              &lt;span class="metric-label">댓글수&lt;/span>
            &lt;/div>
            &lt;div class="metric-card">
              &lt;span class="metric-value">{{ analysisResult.metrics.duration }}&lt;/span>
              &lt;span class="metric-label">영상 길이&lt;/span>
            &lt;/div>
          &lt;/div>
        &lt;/div>

        &lt;div class="section">
          &lt;h3>&lt;i class="fas fa-lightbulb">&lt;/i> AI 분석 결과&lt;/h3>
          &lt;div class="analysis-cards">
            &lt;div class="analysis-card">
              &lt;h4>콘텐츠 품질&lt;/h4>
              &lt;div class="rating">
                &lt;div class="stars" :style="{ '--rating': analysisResult.contentQuality }">&lt;/div>
                &lt;span>{{ analysisResult.contentQuality }}/5&lt;/span>
              &lt;/div>
              &lt;p>{{ analysisResult.qualityAnalysis }}&lt;/p>
            &lt;/div>

            &lt;div class="analysis-card">
              &lt;h4>시청자 참여도&lt;/h4>
              &lt;div class="engagement-bars">
                &lt;div 
                  v-for="(value, metric) in analysisResult.engagement" 
                  :key="metric"
                  class="engagement-bar"
                >
                  &lt;span class="label">{{ metric }}&lt;/span>
                  &lt;div class="bar-container">
                    &lt;div class="bar" :style="{ width: value + '%' }">&lt;/div>
                    &lt;span class="value">{{ value }}%&lt;/span>
                  &lt;/div>
                &lt;/div>
              &lt;/div>
            &lt;/div>
          &lt;/div>

        &lt;div class="section">
          &lt;h3>&lt;i class="fas fa-comment-dots">&lt;/i> 개선 제안&lt;/h3>
          &lt;div class="suggestions">
            &lt;div v-for="(suggestion, index) in analysisResult.suggestions" 
                 :key="index" 
                 class="suggestion-card"
            >
              &lt;i :class="suggestion.icon">&lt;/i>
              &lt;div class="suggestion-content">
                &lt;h4>{{ suggestion.title }}&lt;/h4>
                &lt;p>{{ suggestion.description }}&lt;/p>
              &lt;/div>
            &lt;/div>
          &lt;/div>
        &lt;/div>
      &lt;/div>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script>
export default {
  name: 'YoutubeAnalyzerView',
  data() {
    return {
      videoUrl: '',
      loading: false,
      error: null,
      analysisResult: null
    }
  },
  computed: {
    isValidUrl() {
      // 간단한 유튜브 URL 검증
      return this.videoUrl.includes('youtube.com/watch?v=') || 
             this.videoUrl.includes('youtu.be/')
    }
  },
  methods: {
    async analyzeVideo() {
      if (!this.isValidUrl) {
        this.error = '올바른 유튜브 URL을 입력해주세요'
        return
      }

      this.loading = true
      this.error = null
      this.analysisResult = null

      try {
        const response = await fetch(`${process.env.VUE_APP_API_URL}/api/analyze-video`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            videoUrl: this.videoUrl
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || '분석 중 오류가 발생했습니다')
        }

        this.analysisResult = await response.json()
        
        // ISO 8601 duration을 읽기 쉬운 형식으로 변환
        if (this.analysisResult.metrics.duration) {
          const duration = this.analysisResult.metrics.duration
          const match = duration.match(/PT(\d+H)?(\d+M)?(\d+S)?/)
          
          const hours = (match[1] || '').replace('H', '') || '0'
          const minutes = (match[2] || '').replace('M', '') || '0'
          const seconds = (match[3] || '').replace('S', '') || '0'
          
          this.analysisResult.metrics.duration = `${hours}:${minutes.padStart(2, '0')}:${seconds.padStart(2, '0')}`
        }

        // 큰 숫자를 읽기 쉬운 형식으로 변환
        this.analysisResult.metrics.views = this.formatNumber(this.analysisResult.metrics.views)
        this.analysisResult.metrics.likes = this.formatNumber(this.analysisResult.metrics.likes)
        this.analysisResult.metrics.comments = this.formatNumber(this.analysisResult.metrics.comments)

      } catch (err) {
        this.error = err.message
        console.error('Analysis error:', err)
      } finally {
        this.loading = false
      }
    },

    formatNumber(num) {
      num = parseInt(num)
      if (num >= 10000000) {
        return (num / 10000000).toFixed(1) + '천만'
      } else if (num >= 10000) {
        return (num / 10000).toFixed(1) + '만'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + '천'
      }
      return num.toString()
    }
  }
}
&lt;/script>

&lt;style scoped>
.youtube-analyzer {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.analyzer-header {
  text-align: center;
  margin-bottom: 3rem;
}

.analyzer-header h1 {
  font-size: 2.5rem;
  color: #1f2937;
  margin-bottom: 1rem;
}

.analyzer-header p {
  color: #6b7280;
  font-size: 1.1rem;
}

.analyzer-input {
  max-width: 800px;
  margin: 0 auto 3rem;
}

.url-input {
  display: flex;
  gap: 1rem;
}

.url-input input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s;
}

.url-input input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.url-input button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 2rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.url-input button:hover:not(:disabled) {
  background: #4f46e5;
}

.url-input button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.error {
  color: #dc2626;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

.loading-state {
  text-align: center;
  padding: 4rem 0;
}

.loading-animation {
  font-size: 3rem;
  color: #6366f1;
  margin-bottom: 1.5rem;
}

.loading-state h3 {
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.loading-state p {
  color: #6b7280;
}

.analysis-result {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  overflow: hidden;
}

.video-preview {
  position: relative;
  background: #1f2937;
  padding: 2rem;
  color: white;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.video-preview img {
  width: 240px;
  height: 135px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.video-info h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.analysis-sections {
  padding: 2rem;
}

.section {
  margin-bottom: 3rem;
}

.section h3 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.section h3 i {
  color: #6366f1;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
}

.metric-card {
  background: #f3f4f6;
  padding: 1.5rem;
  border-radius: 0.75rem;
  text-align: center;
}

.metric-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.metric-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.analysis-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.analysis-card {
  background: #f3f4f6;
  padding: 1.5rem;
  border-radius: 0.75rem;
}

.analysis-card h4 {
  color: #1f2937;
  margin-bottom: 1rem;
}

.rating {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stars {
  position: relative;
  display: inline-block;
  color: #fbbf24;
  font-size: 1.25rem;
}

.stars::before {
  content: '★★★★★';
}

.stars::after {
  content: '★★★★★';
  position: absolute;
  left: 0;
  color: #fbbf24;
  width: calc(var(--rating) * 20%);
  overflow: hidden;
}

.engagement-bars {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.engagement-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.engagement-bar .label {
  flex: 0 0 100px;
  font-size: 0.875rem;
  color: #4b5563;
}

.bar-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.bar {
  flex: 1;
  height: 8px;
  background: #6366f1;
  border-radius: 4px;
}

.value {
  font-size: 0.875rem;
  color: #4b5563;
  width: 40px;
}

.suggestions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.suggestion-card {
  display: flex;
  gap: 1rem;
  background: #f3f4f6;
  padding: 1.5rem;
  border-radius: 0.75rem;
}

.suggestion-card i {
  font-size: 1.5rem;
  color: #6366f1;
}

.suggestion-content h4 {
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.suggestion-content p {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .analyzer-header h1 {
    font-size: 2rem;
  }

  .url-input {
    flex-direction: column;
  }

  .url-input button {
    padding: 1rem;
  }

  .video-preview {
    flex-direction: column;
    text-align: center;
  }

  .video-preview img {
    width: 100%;
    height: auto;
  }

  .analysis-sections {
    padding: 1rem;
  }
}
&lt;/style>

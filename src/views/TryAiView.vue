<template>
  <div class="container py-5">
    <h2 class="mb-4">무료 AI 도구 체험</h2>
    <div class="row g-4">
      <!-- 텍스트 생성 AI -->
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">
              <i class="fas fa-pen-alt text-primary me-2"></i>
              텍스트 생성 AI
            </h5>
            <div class="mb-3">
              <label class="form-label">주제 또는 키워드</label>
              <input type="text" class="form-control" v-model="textPrompt" placeholder="예: 여행 블로그 글 작성">
            </div>
            <div class="mb-3">
              <label class="form-label">글자 수</label>
              <select class="form-select" v-model="textLength">
                <option value="short">짧게 (100자 내외)</option>
                <option value="medium">보통 (300자 내외)</option>
                <option value="long">길게 (500자 내외)</option>
              </select>
            </div>
            <button class="btn btn-primary" @click="generateText" :disabled="isGeneratingText">
              <i class="fas fa-magic me-2"></i>
              {{ isGeneratingText ? '생성 중...' : '텍스트 생성하기' }}
            </button>
            <div class="mt-3" v-if="generatedText">
              <div class="alert alert-success">
                <pre class="mb-0">{{ generatedText }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 이미지 생성 AI -->
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">
              <i class="fas fa-image text-primary me-2"></i>
              이미지 생성 AI
            </h5>
            <div class="mb-3">
              <label class="form-label">이미지 설명</label>
              <input type="text" class="form-control" v-model="imagePrompt" placeholder="예: 해변가의 일몰">
            </div>
            <div class="mb-3">
              <label class="form-label">이미지 스타일</label>
              <select class="form-select" v-model="imageStyle">
                <option value="realistic">사실적</option>
                <option value="artistic">예술적</option>
                <option value="cartoon">만화풍</option>
              </select>
            </div>
            <button class="btn btn-primary" @click="generateImage" :disabled="isGeneratingImage">
              <i class="fas fa-palette me-2"></i>
              {{ isGeneratingImage ? '생성 중...' : '이미지 생성하기' }}
            </button>
            <div class="mt-3" v-if="generatedImageUrl">
              <img :src="generatedImageUrl" class="img-fluid rounded" alt="Generated Image">
            </div>
          </div>
        </div>
      </div>

      <!-- 음성 합성 AI -->
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">
              <i class="fas fa-microphone text-primary me-2"></i>
              음성 합성 AI
            </h5>
            <div class="mb-3">
              <label class="form-label">텍스트 입력</label>
              <textarea class="form-control" v-model="voiceText" rows="3" placeholder="변환할 텍스트를 입력하세요"></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label">음성 선택</label>
              <select class="form-select" v-model="voiceType">
                <option value="female1">여성 음성 1</option>
                <option value="male1">남성 음성 1</option>
                <option value="child1">아동 음성 1</option>
              </select>
            </div>
            <button class="btn btn-primary" @click="generateVoice" :disabled="isGeneratingVoice">
              <i class="fas fa-volume-up me-2"></i>
              {{ isGeneratingVoice ? '생성 중...' : '음성 생성하기' }}
            </button>
            <div class="mt-3" v-if="generatedVoiceUrl">
              <audio controls class="w-100">
                <source :src="generatedVoiceUrl" type="audio/mp3">
                Your browser does not support the audio element.
              </audio>
            </div>
          </div>
        </div>
      </div>

      <!-- 감정 분석 AI -->
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">
              <i class="fas fa-smile text-primary me-2"></i>
              감정 분석 AI
            </h5>
            <div class="mb-3">
              <label class="form-label">분석할 텍스트</label>
              <textarea class="form-control" v-model="sentimentText" rows="3" placeholder="분석할 텍스트를 입력하세요"></textarea>
            </div>
            <button class="btn btn-primary" @click="analyzeSentiment" :disabled="isAnalyzingSentiment">
              <i class="fas fa-search me-2"></i>
              {{ isAnalyzingSentiment ? '분석 중...' : '감정 분석하기' }}
            </button>
            <div class="mt-3" v-if="sentimentResult">
              <div class="alert" :class="getSentimentAlertClass()">
                <h6 class="mb-2">분석 결과:</h6>
                <div class="d-flex align-items-center">
                  <i :class="getSentimentIcon()" class="me-2 fa-2x"></i>
                  <div>
                    <div>감정: {{ sentimentResult.emotion }}</div>
                    <div>신뢰도: {{ sentimentResult.confidence }}%</div>
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
  name: 'TryAiView',
  data() {
    return {
      // 텍스트 생성
      textPrompt: '',
      textLength: 'medium',
      generatedText: '',
      isGeneratingText: false,

      // 이미지 생성
      imagePrompt: '',
      imageStyle: 'realistic',
      generatedImageUrl: '',
      isGeneratingImage: false,

      // 음성 합성
      voiceText: '',
      voiceType: 'female1',
      generatedVoiceUrl: '',
      isGeneratingVoice: false,

      // 감정 분석
      sentimentText: '',
      sentimentResult: null,
      isAnalyzingSentiment: false
    }
  },
  methods: {
    async generateText() {
      this.isGeneratingText = true
      try {
        // 실제 API 호출 대신 임시 데이터
        await new Promise(resolve => setTimeout(resolve, 2000))
        this.generatedText = '여기에 생성된 텍스트가 표시됩니다...'
      } catch (error) {
        console.error('텍스트 생성 오류:', error)
      } finally {
        this.isGeneratingText = false
      }
    },

    async generateImage() {
      this.isGeneratingImage = true
      try {
        // 실제 API 호출 대신 임시 데이터
        await new Promise(resolve => setTimeout(resolve, 2000))
        this.generatedImageUrl = 'https://via.placeholder.com/400'
      } catch (error) {
        console.error('이미지 생성 오류:', error)
      } finally {
        this.isGeneratingImage = false
      }
    },

    async generateVoice() {
      this.isGeneratingVoice = true
      try {
        // 실제 API 호출 대신 임시 데이터
        await new Promise(resolve => setTimeout(resolve, 2000))
        this.generatedVoiceUrl = 'https://example.com/sample.mp3'
      } catch (error) {
        console.error('음성 생성 오류:', error)
      } finally {
        this.isGeneratingVoice = false
      }
    },

    async analyzeSentiment() {
      this.isAnalyzingSentiment = true
      try {
        // 실제 API 호출 대신 임시 데이터
        await new Promise(resolve => setTimeout(resolve, 2000))
        this.sentimentResult = {
          emotion: '긍정적',
          confidence: 85
        }
      } catch (error) {
        console.error('감정 분석 오류:', error)
      } finally {
        this.isAnalyzingSentiment = false
      }
    },

    getSentimentAlertClass() {
      if (!this.sentimentResult) return ''
      switch (this.sentimentResult.emotion) {
        case '긍정적':
          return 'alert-success'
        case '부정적':
          return 'alert-danger'
        default:
          return 'alert-info'
      }
    },

    getSentimentIcon() {
      if (!this.sentimentResult) return ''
      switch (this.sentimentResult.emotion) {
        case '긍정적':
          return 'fas fa-smile text-success'
        case '부정적':
          return 'fas fa-frown text-danger'
        default:
          return 'fas fa-meh text-info'
      }
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

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>

<template>
  <div class="ai-trends">
    <div class="container py-4">
      <!-- AI 트렌드 섹션 -->
      <section class="mb-5">
        <h2 class="mb-4">최신 AI 트렌드</h2>
        <div class="row">
          <!-- Twitter 업데이트 -->
          <div class="col-md-6">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="mb-0">AI 전문가 업데이트</h5>
              </div>
              <div class="card-body">
                <div v-if="loading.twitter" class="text-center">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div v-else-if="trends.twitter_updates && trends.twitter_updates.length">
                  <div v-for="tweet in trends.twitter_updates" :key="tweet.created_at" class="mb-3">
                    <div class="d-flex align-items-start">
                      <div class="flex-grow-1">
                        <h6 class="mb-1">@{{ tweet.author }}</h6>
                        <p class="mb-1">{{ tweet.text }}</p>
                        <small class="text-muted">
                          {{ formatDate(tweet.created_at) }}
                        </small>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="text-center text-muted">
                  트윗을 불러올 수 없습니다.
                </div>
              </div>
            </div>
          </div>
          
          <!-- Tech News -->
          <div class="col-md-6">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="mb-0">AI 뉴스</h5>
              </div>
              <div class="card-body">
                <div v-if="loading.news" class="text-center">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div v-else-if="trends.tech_news && trends.tech_news.length">
                  <div v-for="news in trends.tech_news" :key="news.url" class="mb-3">
                    <h6 class="mb-1">
                      <a :href="news.url" target="_blank" rel="noopener noreferrer">
                        {{ news.title }}
                      </a>
                    </h6>
                    <small class="text-muted">{{ news.source }} - {{ formatDate(news.timestamp) }}</small>
                  </div>
                </div>
                <div v-else class="text-center text-muted">
                  뉴스를 불러올 수 없습니다.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <!-- AI 도구 추천 섹션 -->
      <section class="mb-5">
        <h2 class="mb-4">AI 도구 추천</h2>
        <div class="card">
          <div class="card-body">
            <div class="mb-4">
              <input
                v-model="toolQuery"
                @keyup.enter="searchTools"
                type="text"
                class="form-control form-control-lg"
                placeholder="필요한 기능을 입력하세요 (예: 영상 편집, 텍스트 생성)"
              >
            </div>
            
            <div v-if="loading.tools" class="text-center">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            
            <div v-else-if="recommendations.length" class="row">
              <div v-for="tool in recommendations" :key="tool.id" class="col-md-4 mb-4">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title">{{ tool.name }}</h5>
                    <p class="card-text">{{ tool.description }}</p>
                    <div class="mb-2">
                      <span 
                        v-for="category in tool.categories" 
                        :key="category"
                        class="badge bg-primary me-1"
                      >
                        {{ category }}
                      </span>
                    </div>
                    <div class="mb-2">
                      <small class="text-muted">
                        난이도: {{ tool.difficulty }}
                      </small>
                    </div>
                    <div class="mb-2">
                      <small class="text-muted">
                        가격: 
                        <span v-if="tool.pricing.free_tier">무료 플랜 있음</span>
                        <span v-else>${{ tool.pricing.paid_tier_starts }}/월부터</span>
                      </small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center text-muted">
              도구를 검색하려면 위에 키워드를 입력하세요.
            </div>
          </div>
        </div>
      </section>
      
      <!-- API 통합 섹션 -->
      <section class="mb-5">
        <h2 class="mb-4">AI API 테스트</h2>
        <div class="row">
          <!-- 텍스트 생성 -->
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="mb-0">텍스트 생성</h5>
              </div>
              <div class="card-body">
                <textarea
                  v-model="textPrompt"
                  class="form-control mb-3"
                  rows="3"
                  placeholder="텍스트 생성을 위한 프롬프트를 입력하세요"
                ></textarea>
                <button
                  @click="generateText"
                  class="btn btn-primary"
                  :disabled="loading.text"
                >
                  생성하기
                </button>
                <div v-if="results.text" class="mt-3">
                  <strong>결과:</strong>
                  <p>{{ results.text }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 이미지 생성 -->
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="mb-0">이미지 생성</h5>
              </div>
              <div class="card-body">
                <textarea
                  v-model="imagePrompt"
                  class="form-control mb-3"
                  rows="3"
                  placeholder="이미지 생성을 위한 프롬프트를 입력하세요"
                ></textarea>
                <button
                  @click="generateImage"
                  class="btn btn-primary"
                  :disabled="loading.image"
                >
                  생성하기
                </button>
                <div v-if="results.image" class="mt-3">
                  <img :src="results.image" class="img-fluid" alt="Generated image">
                </div>
              </div>
            </div>
          </div>
          
          <!-- 비디오 스크립트 생성 -->
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="mb-0">비디오 스크립트 생성</h5>
              </div>
              <div class="card-body">
                <input
                  v-model="scriptTopic"
                  type="text"
                  class="form-control mb-3"
                  placeholder="비디오 주제를 입력하세요"
                >
                <select v-model="scriptDuration" class="form-select mb-3">
                  <option value="short">짧은 영상 (1-3분)</option>
                  <option value="medium">중간 길이 (3-7분)</option>
                  <option value="long">긴 영상 (7-15분)</option>
                </select>
                <button
                  @click="generateScript"
                  class="btn btn-primary"
                  :disabled="loading.script"
                >
                  생성하기
                </button>
                <div v-if="results.script" class="mt-3">
                  <strong>스크립트:</strong>
                  <p style="white-space: pre-line">{{ results.script }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AiTrendsView',
  
  data() {
    return {
      trends: {
        twitter_updates: [],
        tech_news: []
      },
      loading: {
        twitter: false,
        news: false,
        tools: false,
        text: false,
        image: false,
        script: false
      },
      toolQuery: '',
      recommendations: [],
      textPrompt: '',
      imagePrompt: '',
      scriptTopic: '',
      scriptDuration: 'short',
      results: {
        text: null,
        image: null,
        script: null
      }
    };
  },
  
  methods: {
    async fetchTrends() {
      this.loading.twitter = true;
      this.loading.news = true;
      try {
        const response = await axios.get('http://localhost:5003/api/trends');
        if (response.data.success) {
          this.trends = response.data;
        }
      } catch (error) {
        console.error('Error fetching trends:', error);
      } finally {
        this.loading.twitter = false;
        this.loading.news = false;
      }
    },
    
    async searchTools() {
      this.loading.tools = true;
      try {
        const response = await axios.post('http://localhost:5003/api/tools/recommend', {
          query: this.toolQuery
        });
        if (response.data.success) {
          this.recommendations = response.data.recommendations;
        }
      } catch (error) {
        console.error('Error searching tools:', error);
      } finally {
        this.loading.tools = false;
      }
    },
    
    async generateText() {
      this.loading.text = true;
      try {
        const response = await axios.post('http://localhost:5003/api/generate/text', {
          prompt: this.textPrompt
        });
        if (response.data.success) {
          this.results.text = response.data.text;
        }
      } catch (error) {
        console.error('Error generating text:', error);
      } finally {
        this.loading.text = false;
      }
    },
    
    async generateImage() {
      this.loading.image = true;
      try {
        const response = await axios.post('http://localhost:5003/api/generate/image', {
          prompt: this.imagePrompt
        });
        if (response.data.success) {
          this.results.image = response.data.image_url;
        }
      } catch (error) {
        console.error('Error generating image:', error);
      } finally {
        this.loading.image = false;
      }
    },
    
    async generateScript() {
      this.loading.script = true;
      try {
        const response = await axios.post('http://localhost:5003/api/generate/script', {
          topic: this.scriptTopic,
          duration: this.scriptDuration
        });
        if (response.data.success) {
          this.results.script = response.data.script;
        }
      } catch (error) {
        console.error('Error generating script:', error);
      } finally {
        this.loading.script = false;
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    }
  },
  
  mounted() {
    this.fetchTrends();
  }
};
</script>

<style scoped>
.ai-trends {
  background-color: #f8f9fa;
}

.card {
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.badge {
  font-size: 0.8rem;
  padding: 0.4em 0.8em;
}
</style>

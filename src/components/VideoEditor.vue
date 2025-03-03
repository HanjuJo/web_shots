<template>
  <section class="video-editor">
    <h2>AI 영상 편집</h2>
    
    <!-- 입력 섹션 -->
    <div class="input-section">
      <textarea 
        v-model="inputText" 
        placeholder="편집할 텍스트를 입력하세요. 예: '인트로 추가, 배경음악 삽입, 자막 생성'"
        :disabled="isLoading"
      ></textarea>
      
      <button 
        @click="editVideo" 
        :disabled="!inputText || isLoading"
        :class="{ loading: isLoading }"
      >
        <i class="fas fa-spinner fa-spin" v-if="isLoading"></i>
        {{ isLoading ? '편집 중...' : '편집 시작' }}
      </button>
    </div>

    <!-- 결과 섹션 -->
    <div v-if="result" class="result-section">
      <div class="result-card">
        <h3>편집 결과</h3>
        <div class="result-info">
          <p><i class="fas fa-film"></i> 상태: <span :class="result.status">{{ result.status }}</span></p>
          <p><i class="fas fa-clock"></i> 길이: {{ result.duration }}</p>
        </div>
        <div class="video-preview" v-if="result.edited_video">
          <video controls>
            <source :src="result.edited_video" type="video/mp4">
            브라우저가 비디오 재생을 지원하지 않습니다.
          </video>
        </div>
      </div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="error-message">
      <i class="fas fa-exclamation-circle"></i>
      {{ error }}
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VideoEditor',
  data() {
    return {
      inputText: '',
      result: null,
      isLoading: false,
      error: null
    };
  },
  methods: {
    async editVideo() {
      if (!this.inputText) return;
      
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await axios.post('/api/edit_video', { 
          text: this.inputText 
        });
        this.result = response.data;
      } catch (error) {
        this.error = error.response?.data?.message || 
                    '영상 편집 중 오류가 발생했습니다. 다시 시도해주세요.';
        console.error('Error editing video:', error);
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>
.video-editor {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

h2 {
  color: var(--primary-color);
  text-align: center;
  margin-bottom: 30px;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

textarea {
  width: 100%;
  height: 150px;
  padding: 15px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 16px;
  resize: vertical;
  transition: border-color 0.3s;
}

textarea:focus {
  border-color: var(--primary-color);
  outline: none;
}

button {
  padding: 15px 30px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

button:hover:not(:disabled) {
  background-color: var(--primary-dark);
}

button:disabled {
  background-color: var(--text-secondary);
  cursor: not-allowed;
}

.loading {
  opacity: 0.8;
}

.result-section {
  margin-top: 40px;
}

.result-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.result-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.result-info p {
  display: flex;
  align-items: center;
  gap: 10px;
}

.video-preview {
  margin-top: 20px;
}

.video-preview video {
  width: 100%;
  max-height: 500px;
  border-radius: 8px;
}

.error-message {
  margin-top: 20px;
  padding: 15px;
  background-color: #fee2e2;
  color: #dc2626;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

@media (max-width: 768px) {
  .video-editor {
    margin: 20px auto;
  }
  
  textarea {
    height: 120px;
  }
  
  .result-info {
    grid-template-columns: 1fr;
  }
}
</style>
<template>
  <div class="create-post">
    <div class="create-post-container">
      <header class="create-post-header">
        <h1>새 글 작성</h1>
        <div class="header-actions">
          <button class="preview-button" @click="togglePreview">
            <i class="fas fa-eye"></i>
            {{ isPreview ? '수정하기' : '미리보기' }}
          </button>
          <button class="publish-button" @click="publishPost" :disabled="!isValid">
            <i class="fas fa-paper-plane"></i>
            발행하기
          </button>
        </div>
      </header>

      <div v-if="!isPreview" class="editor-section">
        <div class="form-group">
          <input 
            type="text" 
            v-model="post.title"
            placeholder="제목을 입력하세요"
            class="title-input"
          >
        </div>

        <div class="form-group">
          <select v-model="post.category" class="category-select">
            <option value="">카테고리 선택</option>
            <option v-for="category in categories" 
                    :key="category.value" 
                    :value="category.value"
            >
              {{ category.label }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <div class="tag-input">
            <div class="tag-list">
              <span v-for="(tag, index) in post.tags" 
                    :key="index" 
                    class="tag"
              >
                {{ tag }}
                <button @click="removeTag(index)" class="remove-tag">
                  <i class="fas fa-times"></i>
                </button>
              </span>
            </div>
            <input 
              type="text" 
              v-model="newTag"
              @keydown.enter.prevent="addTag"
              placeholder="태그를 입력하고 Enter를 누르세요"
            >
          </div>
        </div>

        <div class="form-group">
          <div class="editor-toolbar">
            <button 
              v-for="tool in editorTools" 
              :key="tool.command"
              @click="executeCommand(tool.command)"
              :title="tool.label"
              class="toolbar-button"
            >
              <i :class="tool.icon"></i>
            </button>
          </div>
          <textarea 
            v-model="post.content"
            placeholder="내용을 입력하세요"
            class="content-editor"
            rows="20"
          ></textarea>
        </div>

        <div class="form-group">
          <div class="media-uploader" @click="triggerFileInput">
            <input 
              type="file" 
              ref="fileInput"
              @change="handleFileUpload"
              accept="image/*"
              multiple
              class="hidden"
            >
            <div class="upload-area">
              <i class="fas fa-cloud-upload-alt"></i>
              <p>클릭하여 이미지를 업로드하세요</p>
              <p class="upload-hint">또는 드래그 앤 드롭으로 파일을 추가하세요</p>
            </div>
          </div>
          <div v-if="post.images.length > 0" class="image-preview">
            <div v-for="(image, index) in post.images" 
                 :key="index"
                 class="image-item"
            >
              <img :src="image.url" :alt="image.name">
              <button @click="removeImage(index)" class="remove-image">
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="preview-section">
        <div class="post-preview">
          <h1>{{ post.title || '제목 없음' }}</h1>
          <div class="post-meta">
            <span class="category">{{ getCategoryLabel(post.category) }}</span>
            <div class="tags">
              <span v-for="(tag, index) in post.tags" 
                    :key="index"
                    class="tag"
              >
                #{{ tag }}
              </span>
            </div>
          </div>
          <div class="post-content" v-html="renderContent"></div>
          <div v-if="post.images.length > 0" class="post-images">
            <img v-for="(image, index) in post.images"
                 :key="index"
                 :src="image.url"
                 :alt="image.name"
                 class="content-image"
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import marked from 'marked'

export default {
  name: 'CreatePost',
  data() {
    return {
      isPreview: false,
      newTag: '',
      post: {
        title: '',
        category: '',
        tags: [],
        content: '',
        images: []
      },
      categories: [
        { value: 'guide', label: '가이드' },
        { value: 'tutorial', label: '튜토리얼' },
        { value: 'review', label: '리뷰' },
        { value: 'discussion', label: '토론' },
        { value: 'showcase', label: '작업물 공유' }
      ],
      editorTools: [
        { command: 'bold', label: '굵게', icon: 'fas fa-bold' },
        { command: 'italic', label: '기울임', icon: 'fas fa-italic' },
        { command: 'heading', label: '제목', icon: 'fas fa-heading' },
        { command: 'link', label: '링크', icon: 'fas fa-link' },
        { command: 'quote', label: '인용', icon: 'fas fa-quote-right' },
        { command: 'code', label: '코드', icon: 'fas fa-code' },
        { command: 'list-ul', label: '목록', icon: 'fas fa-list-ul' },
        { command: 'list-ol', label: '번호 목록', icon: 'fas fa-list-ol' }
      ]
    }
  },
  computed: {
    isValid() {
      return this.post.title.trim() && 
             this.post.category && 
             this.post.content.trim()
    },
    renderContent() {
      return marked(this.post.content)
    }
  },
  methods: {
    togglePreview() {
      this.isPreview = !this.isPreview
    },
    addTag() {
      const tag = this.newTag.trim()
      if (tag && !this.post.tags.includes(tag)) {
        this.post.tags.push(tag)
      }
      this.newTag = ''
    },
    removeTag(index) {
      this.post.tags.splice(index, 1)
    },
    executeCommand(command) {
      let insertion = ''
      switch (command) {
        case 'bold':
          insertion = '**굵은 텍스트**'
          break
        case 'italic':
          insertion = '*기울인 텍스트*'
          break
        case 'heading':
          insertion = '## 제목'
          break
        case 'link':
          insertion = '[링크 텍스트](URL)'
          break
        case 'quote':
          insertion = '> 인용문'
          break
        case 'code':
          insertion = '```\n코드\n```'
          break
        case 'list-ul':
          insertion = '- 목록 항목'
          break
        case 'list-ol':
          insertion = '1. 목록 항목'
          break
      }
      
      const textarea = document.querySelector('.content-editor')
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      
      this.post.content = this.post.content.substring(0, start) +
                         insertion +
                         this.post.content.substring(end)
    },
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    async handleFileUpload(event) {
      const files = Array.from(event.target.files)
      for (const file of files) {
        if (file.type.startsWith('image/')) {
          try {
            // 실제 구현에서는 서버에 업로드하고 URL을 받아와야 함
            const url = URL.createObjectURL(file)
            this.post.images.push({
              name: file.name,
              url: url
            })
          } catch (error) {
            console.error('이미지 업로드 실패:', error)
          }
        }
      }
    },
    removeImage(index) {
      URL.revokeObjectURL(this.post.images[index].url)
      this.post.images.splice(index, 1)
    },
    getCategoryLabel(value) {
      const category = this.categories.find(c => c.value === value)
      return category ? category.label : ''
    },
    async publishPost() {
      try {
        // 실제 구현에서는 서버에 게시글을 저장
        console.log('게시글 발행:', this.post)
        this.$router.push('/community')
      } catch (error) {
        console.error('게시글 발행 실패:', error)
      }
    }
  }
}
</script>

<style scoped>
.create-post {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.create-post-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.create-post-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.create-post-header h1 {
  font-size: 1.5rem;
  color: var(--primary-color);
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.preview-button,
.publish-button {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.preview-button {
  background: white;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}

.preview-button:hover {
  background: var(--primary-light-color);
}

.publish-button {
  background: var(--primary-color);
  border: none;
  color: white;
}

.publish-button:hover {
  background: var(--primary-dark-color);
}

.publish-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.editor-section,
.preview-section {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.title-input {
  width: 100%;
  padding: 1rem;
  font-size: 1.5rem;
  border: none;
  border-bottom: 2px solid #eee;
  transition: border-color 0.3s ease;
}

.title-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.category-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}

.tag-input {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0.5rem;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  background: var(--primary-light-color);
  color: var(--primary-color);
  border-radius: 15px;
  font-size: 0.875rem;
}

.remove-tag {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
}

.tag-input input {
  width: 100%;
  padding: 0.5rem;
  border: none;
}

.tag-input input:focus {
  outline: none;
}

.editor-toolbar {
  display: flex;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-bottom: none;
  border-radius: 8px 8px 0 0;
  background: #f8f9fa;
}

.toolbar-button {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: none;
  color: #666;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.toolbar-button:hover {
  background: #eee;
  color: var(--primary-color);
}

.content-editor {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 0 0 8px 8px;
  resize: vertical;
  min-height: 400px;
  line-height: 1.6;
}

.content-editor:focus {
  outline: none;
  border-color: var(--primary-color);
}

.media-uploader {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.media-uploader:hover {
  border-color: var(--primary-color);
  background: var(--primary-light-color);
}

.upload-area {
  color: #666;
}

.upload-area i {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.upload-hint {
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.hidden {
  display: none;
}

.image-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.image-item {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
}

.image-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.post-preview {
  max-width: 800px;
  margin: 0 auto;
}

.post-preview h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.post-meta {
  margin-bottom: 2rem;
}

.category {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border-radius: 15px;
  margin-right: 1rem;
}

.post-content {
  line-height: 1.8;
  color: #333;
}

.post-images {
  margin-top: 2rem;
  display: grid;
  gap: 1rem;
}

.content-image {
  width: 100%;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .create-post {
    padding: 1rem;
  }

  .create-post-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .title-input {
    font-size: 1.25rem;
  }

  .editor-toolbar {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>

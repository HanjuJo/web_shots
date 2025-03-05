<template>
  <div class="guide-detail">
    <article class="guide-content">
      <header class="guide-header">
        <div class="guide-meta">
          <span class="guide-category">{{ guide.category }}</span>
          <span class="guide-date">{{ formatDate(guide.publishedAt) }}</span>
        </div>
        <h1>{{ guide.title }}</h1>
        <p class="guide-description">{{ guide.description }}</p>
        <div class="author-info">
          <img :src="guide.author.avatar" :alt="guide.author.name">
          <div>
            <strong>{{ guide.author.name }}</strong>
            <p>{{ guide.author.bio }}</p>
          </div>
        </div>
      </header>

      <div class="guide-body" v-html="guide.content"></div>

      <footer class="guide-footer">
        <div class="guide-tags">
          <span v-for="tag in guide.tags" :key="tag" class="tag">
            #{{ tag }}
          </span>
        </div>
        <div class="guide-actions">
          <button class="action-button" @click="toggleLike">
            <i :class="['fas', isLiked ? 'fa-heart' : 'fa-heart-o']"></i>
            {{ guide.likes }}
          </button>
          <button class="action-button" @click="toggleBookmark">
            <i :class="['fas', isBookmarked ? 'fa-bookmark' : 'fa-bookmark-o']"></i>
            북마크
          </button>
          <button class="action-button" @click="shareGuide">
            <i class="fas fa-share"></i>
            공유
          </button>
        </div>
      </footer>
    </article>

    <aside class="guide-sidebar">
      <section class="table-of-contents">
        <h2>목차</h2>
        <nav>
          <ul>
            <li v-for="(section, index) in guide.sections" :key="index">
              <a :href="'#section-' + index" class="toc-link">
                {{ section.title }}
              </a>
            </li>
          </ul>
        </nav>
      </section>

      <section class="related-guides">
        <h2>관련 가이드</h2>
        <div class="related-list">
          <article v-for="related in relatedGuides" :key="related.id" 
                   class="related-guide" @click="goToGuide(related.id)">
            <img :src="related.thumbnail" :alt="related.title">
            <div class="related-content">
              <h3>{{ related.title }}</h3>
              <p>{{ related.excerpt }}</p>
            </div>
          </article>
        </div>
      </section>
    </aside>

    <section class="guide-comments">
      <h2>댓글</h2>
      <div class="comment-form">
        <textarea 
          v-model="newComment" 
          placeholder="댓글을 작성해주세요..."
          rows="3"
        ></textarea>
        <button @click="submitComment" :disabled="!newComment.trim()">
          댓글 작성
        </button>
      </div>

      <div class="comments-list">
        <article v-for="comment in guide.comments" :key="comment.id" class="comment">
          <div class="comment-header">
            <div class="commenter-info">
              <img :src="comment.author.avatar" :alt="comment.author.name">
              <div>
                <strong>{{ comment.author.name }}</strong>
                <span class="comment-date">{{ formatDate(comment.createdAt) }}</span>
              </div>
            </div>
            <button class="reply-button" @click="replyToComment(comment.id)">
              답글
            </button>
            <button class="delete-button" @click="deleteComment(comment.id)">
              삭제
            </button>
          </div>
          <p class="comment-content">{{ comment.content }}</p>
          <div v-if="comment.replies" class="comment-replies">
            <article v-for="reply in comment.replies" :key="reply.id" class="reply">
              <div class="comment-header">
                <div class="commenter-info">
                  <img :src="reply.author.avatar" :alt="reply.author.name">
                  <div>
                    <strong>{{ reply.author.name }}</strong>
                    <span class="comment-date">{{ formatDate(reply.createdAt) }}</span>
                  </div>
                </div>
              </div>
              <p class="comment-content">{{ reply.content }}</p>
            </article>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name: 'GuideDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  setup(props) {
    const guide = ref({
      title: '',
      description: '',
      category: '',
      publishedAt: new Date(),
      content: '',
      tags: [],
      likes: 0,
      author: {
        name: '',
        avatar: '',
        bio: ''
      },
      sections: [],
      comments: []
    })
    
    const relatedGuides = ref([])
    const isLoading = ref(true)
    const error = ref(null)
    const isLiked = ref(false)
    const isBookmarked = ref(false)
    const newComment = ref('')
    const replyContent = ref('')
    const router = useRouter()

    const fetchGuideData = async () => {
      isLoading.value = true
      error.value = null
      
      try {
        // First check if we can get the data from the API
        const response = await axios.get(`/api/guides/${props.id}`)
          .catch(err => {
            console.log('API fetch failed, using mock data:', err.message)
            // If API fails, use mock data
            return { 
              data: {
                guide: mockGuideData,
                relatedGuides: mockRelatedGuides
              }
            }
          })
        
        guide.value = response.data.guide
        relatedGuides.value = response.data.relatedGuides
      } catch (err) {
        console.error('Error fetching guide data:', err)
        error.value = 'Failed to load guide. Please try again later.'
        // Use mock data as fallback
        guide.value = mockGuideData
        relatedGuides.value = mockRelatedGuides
      } finally {
        isLoading.value = false
      }
    }

    const formatDate = (date) => {
      return new Intl.DateTimeFormat('ko-KR').format(date)
    }

    const toggleLike = () => {
      isLiked.value = !isLiked.value
      guide.value.likes += isLiked.value ? 1 : -1
      
      // Optional: Update the like count on the server
      if (process.env.VUE_APP_API_URL) {
        axios.post(`/api/guides/${props.id}/like`, { liked: isLiked.value })
          .catch(err => console.error('Failed to update like status:', err))
      }
    }

    const toggleBookmark = () => {
      isBookmarked.value = !isBookmarked.value
      
      // Optional: Update bookmark status on the server
      if (process.env.VUE_APP_API_URL) {
        axios.post(`/api/guides/${props.id}/bookmark`, { bookmarked: isBookmarked.value })
          .catch(err => console.error('Failed to update bookmark status:', err))
      }
    }

    const shareGuide = () => {
      // Implement share functionality
      if (navigator.share) {
        navigator.share({
          title: guide.value.title,
          text: guide.value.description,
          url: window.location.href
        }).catch(err => console.error('Error sharing:', err))
      } else {
        alert('공유 링크가 클립보드에 복사되었습니다.')
        navigator.clipboard.writeText(window.location.href)
      }
    }

    const goToGuide = (guideId) => {
      router.push({ name: 'GuideDetail', params: { id: guideId }})
    }

    const submitComment = async () => {
      if (!newComment.value.trim()) return
      
      try {
        // Create a new comment object
        const comment = {
          id: Date.now(),
          content: newComment.value,
          createdAt: new Date(),
          author: {
            name: '사용자',
            avatar: '/images/avatars/default.jpg'
          }
        }
        
        // Optional: Send to server if API is available
        if (process.env.VUE_APP_API_URL) {
          await axios.post(`/api/guides/${props.id}/comments`, { content: newComment.value })
        }
        
        // Update local state
        guide.value.comments.unshift(comment)
        newComment.value = ''
      } catch (err) {
        console.error('Failed to submit comment:', err)
        alert('댓글 작성에 실패했습니다. 다시 시도해주세요.')
      }
    }

    const replyToComment = async (commentId) => {
      if (!replyContent.value.trim()) return
      
      try {
        const reply = {
          id: Date.now(),
          content: replyContent.value,
          parentId: commentId,
          createdAt: new Date(),
          author: {
            name: '사용자',
            avatar: '/images/avatars/default.jpg'
          }
        }
        
        // Add the reply to the comment
        const comment = guide.value.comments.find(c => c.id === commentId)
        if (comment) {
          if (!comment.replies) {
            comment.replies = []
          }
          comment.replies.push(reply)
        }
        
        replyContent.value = ''
      } catch (error) {
        console.error('답글 작성 실패:', error)
        alert('답글 작성에 실패했습니다. 다시 시도해주세요.')
      }
    }

    const deleteComment = async (commentId) => {
      try {
        // Optional: Remove on server if API is available
        if (process.env.VUE_APP_API_URL) {
          await axios.delete(`/api/guides/${props.id}/comments/${commentId}`)
        }
        
        // Remove from local state
        const commentIndex = guide.value.comments.findIndex(c => c.id === commentId)
        if (commentIndex !== -1) {
          guide.value.comments.splice(commentIndex, 1)
        }
      } catch (err) {
        console.error('Failed to delete comment:', err)
        alert('댓글 삭제에 실패했습니다. 다시 시도해주세요.')
      }
    }

    // Mock data for fallback
    const mockGuideData = {
      title: 'AI 이미지 생성 가이드',
      description: 'Stable Diffusion을 활용한 고품질 이미지 생성하기',
      category: '이미지 생성',
      publishedAt: new Date(2025, 1, 1),
      content: '<h2>Stable Diffusion으로 고품질 이미지 생성하기</h2><p>이 가이드에서는 Stable Diffusion을 사용하여 고품질 이미지를 생성하는 방법을 배우게 됩니다.</p><h3>프롬프트 작성법</h3><p>효과적인 프롬프트 작성법은 좋은 이미지 생성의 비결입니다...</p>',
      tags: ['AI', 'Stable Diffusion', '이미지 생성'],
      likes: 128,
      author: {
        name: '김창작',
        avatar: '/images/avatars/user1.jpg',
        bio: 'AI 크리에이터 | 디지털 아티스트'
      },
      sections: [
        { title: '소개', id: 'intro' },
        { title: '프롬프트 작성법', id: 'prompts' },
        { title: '모델 선택하기', id: 'models' },
        { title: '후처리 기법', id: 'post-processing' }
      ],
      comments: [
        {
          id: 1,
          author: {
            name: '이디자인',
            avatar: '/images/avatars/user2.jpg'
          },
          content: '정말 유용한 가이드네요! 프롬프트 작성법 섹션이 특히 도움이 되었습니다.',
          createdAt: new Date(2025, 1, 15),
          replies: [
            {
              id: 2,
              author: {
                name: '김창작',
                avatar: '/images/avatars/user1.jpg'
              },
              content: '좋은 의견 감사합니다. 더 많은 예시를 추가할 예정입니다.',
              createdAt: new Date(2025, 1, 16)
            }
          ]
        }
      ]
    }

    const mockRelatedGuides = [
      {
        id: 1,
        title: 'AI 이미지 생성 마스터하기',
        excerpt: 'Stable Diffusion과 Midjourney를 활용한 고품질 이미지 생성 노하우',
        thumbnail: '/images/guides/ai-image.jpg'
      },
      {
        id: 2,
        title: 'AI 음성 더빙 완벽 가이드',
        excerpt: '자연스러운 AI 음성 더빙을 위한 설정과 후보정 방법',
        thumbnail: '/images/guides/ai-voice.jpg'
      }
    ]

    onMounted(() => {
      fetchGuideData()
    })

    return {
      guide,
      relatedGuides,
      isLoading,
      error,
      isLiked,
      isBookmarked,
      newComment,
      replyContent,
      formatDate,
      toggleLike,
      toggleBookmark,
      shareGuide,
      goToGuide,
      submitComment,
      replyToComment,
      deleteComment
    }
  }
}
</script>

<style scoped>
.guide-detail {
  max-width: 1200px;
  margin: 2rem auto 4rem;
  padding: 0 1.5rem;
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 3rem;
  color: #333;
}

.guide-content {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.guide-header {
  margin-bottom: 3rem;
}

.guide-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
}

.guide-category {
  padding: 0.35rem 1rem;
  background: var(--primary-color);
  color: white;
  border-radius: 24px;
  font-size: 0.85rem;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.guide-date {
  color: #777;
  font-size: 0.9rem;
}

.guide-header h1 {
  font-size: 2.75rem;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  font-weight: 700;
  color: #222;
}

.guide-description {
  font-size: 1.25rem;
  color: #555;
  margin-bottom: 2.5rem;
  line-height: 1.5;
  font-weight: 400;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem;
  background: #f9f9f9;
  border-radius: 12px;
}

.author-info img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.author-info strong {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 0.35rem;
  color: #222;
}

.author-info p {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.4;
}

.guide-body {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
  margin-bottom: 3rem;
}

.guide-body h2 {
  font-size: 1.8rem;
  margin: 2.5rem 0 1.25rem;
  color: #222;
}

.guide-body h3 {
  font-size: 1.4rem;
  margin: 2rem 0 1rem;
  color: #333;
}

.guide-body p {
  margin-bottom: 1.5rem;
}

.guide-body ul, .guide-body ol {
  margin-bottom: 1.5rem;
  padding-left: 1.5rem;
}

.guide-body li {
  margin-bottom: 0.75rem;
}

.guide-body a {
  color: var(--primary-color);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s ease;
}

.guide-body a:hover {
  border-color: var(--primary-color);
}

.guide-body img {
  max-width: 100%;
  border-radius: 8px;
  margin: 1.5rem 0;
}

.guide-body blockquote {
  border-left: 4px solid var(--primary-color);
  padding: 1rem 1.5rem;
  margin: 1.5rem 0;
  background: #f9f9f9;
  border-radius: 0 8px 8px 0;
  font-style: italic;
  color: #555;
}

.guide-body code {
  background: #f1f1f1;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: Consolas, Monaco, 'Andale Mono', monospace;
}

.guide-body pre {
  background: #f8f8f8;
  padding: 1.25rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.5rem 0;
}

.guide-body pre code {
  background: transparent;
  padding: 0;
  font-size: 0.9rem;
  line-height: 1.6;
}

.guide-footer {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.guide-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
  margin-bottom: 2rem;
}

.tag {
  padding: 0.4rem 1rem;
  background: #f5f5f5;
  color: #555;
  border-radius: 24px;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.tag:hover {
  background: #eee;
  color: #333;
}

.guide-actions {
  display: flex;
  gap: 1rem;
}

.action-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: 1px solid #eee;
  border-radius: 8px;
  background: white;
  color: #555;
  cursor: pointer;
  transition: all 0.25s ease;
  font-weight: 500;
  font-size: 0.95rem;
}

.action-button:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background: #f9f9f9;
}

.action-button i {
  font-size: 1.1rem;
}

.guide-sidebar {
  display: grid;
  gap: 2rem;
  align-self: start;
  position: sticky;
  top: 2rem;
}

.table-of-contents,
.related-guides {
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.table-of-contents h2,
.related-guides h2 {
  font-size: 1.35rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
  color: #222;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #f5f5f5;
}

.toc-link {
  display: block;
  padding: 0.65rem 0;
  color: #555;
  text-decoration: none;
  transition: all 0.2s ease;
  font-size: 1rem;
  border-bottom: 1px solid #f5f5f5;
}

.toc-link:hover {
  color: var(--primary-color);
  padding-left: 0.5rem;
}

.toc-link:last-child {
  border-bottom: none;
}

.related-list {
  display: grid;
  gap: 1.5rem;
}

.related-guide {
  display: flex;
  gap: 1rem;
  cursor: pointer;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #f5f5f5;
  transition: transform 0.2s ease;
}

.related-guide:hover {
  transform: translateX(5px);
}

.related-guide:last-child {
  padding-bottom: 0;
  border-bottom: none;
}

.related-guide img {
  width: 90px;
  height: 90px;
  border-radius: 10px;
  object-fit: cover;
}

.related-content h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  line-height: 1.4;
  font-weight: 600;
  color: #333;
}

.related-content p {
  font-size: 0.85rem;
  color: #666;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.guide-comments {
  grid-column: 1 / -1;
  margin-top: 4rem;
}

.guide-comments h2 {
  font-size: 1.75rem;
  margin-bottom: 2.5rem;
  font-weight: 600;
  color: #222;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #f5f5f5;
}

.comment-form {
  margin-bottom: 3rem;
}

.comment-form textarea {
  width: 100%;
  padding: 1.25rem;
  border: 1px solid #eee;
  border-radius: 12px;
  resize: vertical;
  margin-bottom: 1rem;
  font-size: 1rem;
  font-family: inherit;
  min-height: 120px;
  transition: all 0.25s ease;
}

.comment-form textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(var(--primary-color-rgb), 0.1);
}

.comment-form button {
  padding: 0.85rem 2rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
  transition: all 0.25s ease;
}

.comment-form button:hover {
  background: var(--primary-color-dark, #0056b3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.comment-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.comments-list {
  display: grid;
  gap: 2rem;
}

.comment {
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.commenter-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.commenter-info img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.commenter-info strong {
  display: block;
  font-size: 1.05rem;
  color: #333;
  margin-bottom: 0.25rem;
}

.comment-date {
  color: #777;
  font-size: 0.85rem;
}

.reply-button, .delete-button {
  padding: 0.4rem 1rem;
  border: 1px solid #eee;
  border-radius: 6px;
  background: white;
  color: #555;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.reply-button:hover, .delete-button:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background: #f9f9f9;
}

.delete-button {
  margin-left: 0.5rem;
  color: #dc3545;
}

.delete-button:hover {
  border-color: #dc3545;
  color: #dc3545;
}

.comment-content {
  color: #333;
  line-height: 1.7;
  font-size: 1.05rem;
}

.comment-replies {
  margin-top: 1.5rem;
  padding-left: 2.5rem;
  border-left: 3px solid #f0f0f0;
}

.reply {
  padding: 1.25rem 0;
  border-bottom: 1px solid #f5f5f5;
}

.reply:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

/* Loading state */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

.error-message {
  background: #ffe8e8;
  color: #d32f2f;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 1024px) {
  .guide-detail {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }

  .guide-sidebar {
    position: relative;
    top: 0;
  }

  .table-of-contents {
    display: none;
  }
}

@media (max-width: 768px) {
  .guide-detail {
    margin: 1rem auto 3rem;
    padding: 0 1rem;
  }

  .guide-content {
    padding: 1.75rem;
  }

  .guide-header h1 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .guide-description {
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
  }

  .author-info {
    flex-direction: column;
    align-items: flex-start;
    text-align: center;
  }

  .author-info img {
    margin: 0 auto 1rem;
  }

  .guide-actions {
    flex-wrap: wrap;
  }

  .action-button {
    flex: 1;
    padding: 0.75rem 0.5rem;
  }

  .comment-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .commenter-info {
    margin-bottom: 1rem;
    width: 100%;
  }

  .reply-button, .delete-button {
    margin-top: 0.5rem;
  }

  .comment-replies {
    padding-left: 1.5rem;
  }
}
</style>

<template>
  <div class="post-detail">
    <article class="post-content">
      <header class="post-header">
        <div class="post-meta">
          <span class="post-tag">{{ post.tag }}</span>
          <span class="post-time">{{ formatDate(post.createdAt) }}</span>
        </div>
        <h1>{{ post.title }}</h1>
        <div class="author-info">
          <img :src="post.author.avatar" :alt="post.author.name">
          <div>
            <strong>{{ post.author.name }}</strong>
            <p>{{ post.author.bio }}</p>
          </div>
        </div>
      </header>

      <div class="post-body" v-html="post.content"></div>

      <footer class="post-footer">
        <div class="post-stats">
          <button class="stat-button" @click="likePost">
            <i :class="['fas', post.isLiked ? 'fa-heart' : 'fa-heart-o']"></i>
            좋아요 {{ post.likes }}
          </button>
          <button class="stat-button">
            <i class="fas fa-comment"></i>
            댓글 {{ post.comments.length }}
          </button>
          <button class="stat-button">
            <i class="fas fa-eye"></i>
            조회 {{ post.views }}
          </button>
        </div>
        <div class="post-actions">
          <button class="action-button" @click="sharePost">
            <i class="fas fa-share"></i>
            공유하기
          </button>
          <button class="action-button" @click="reportPost">
            <i class="fas fa-flag"></i>
            신고하기
          </button>
        </div>
      </footer>
    </article>

    <section class="comments-section">
      <h2>댓글 {{ post.comments.length }}개</h2>
      
      <div class="comment-form">
        <img :src="currentUser.avatar" :alt="currentUser.name">
        <div class="form-content">
          <textarea 
            v-model="newComment" 
            placeholder="댓글을 작성해주세요..."
            rows="3"
          ></textarea>
          <div class="form-actions">
            <button class="cancel-button" @click="newComment = ''">취소</button>
            <button 
              class="submit-button" 
              @click="addComment"
              :disabled="!newComment.trim()"
            >
              댓글 작성
            </button>
          </div>
        </div>
      </div>

      <div class="comments-list">
        <article v-for="comment in post.comments" :key="comment.id" class="comment">
          <div class="comment-header">
            <div class="commenter-info">
              <img :src="comment.author.avatar" :alt="comment.author.name">
              <div>
                <strong>{{ comment.author.name }}</strong>
                <span class="comment-time">{{ formatDate(comment.createdAt) }}</span>
              </div>
            </div>
            <div class="comment-actions">
              <button v-if="canEdit(comment)" @click="deleteComment(comment.id)">
                삭제
              </button>
            </div>
          </div>
          
          <p class="comment-content">{{ comment.content }}</p>
          
          <div class="comment-footer">
            <button class="reply-button" @click="toggleReply(comment)">
              답글 달기
            </button>
          </div>

          <div v-if="comment.showReplyForm" class="reply-form">
            <img :src="currentUser.avatar" :alt="currentUser.name">
            <div class="form-content">
              <textarea 
                v-model="comment.replyContent" 
                placeholder="답글을 작성해주세요..."
                rows="2"
              ></textarea>
              <div class="form-actions">
                <button class="cancel-button" @click="comment.replyContent = ''">취소</button>
                <button 
                  class="submit-button"
                  @click="addReply(comment.id)"
                  :disabled="!comment.replyContent?.trim()"
                >
                  답글 작성
                </button>
              </div>
            </div>
          </div>

          <div v-if="comment.replies?.length" class="replies-list">
            <article v-for="reply in comment.replies" :key="reply.id" class="reply">
              <div class="comment-header">
                <div class="commenter-info">
                  <img :src="reply.author.avatar" :alt="reply.author.name">
                  <div>
                    <strong>{{ reply.author.name }}</strong>
                    <span class="comment-time">{{ formatDate(reply.createdAt) }}</span>
                  </div>
                </div>
                <div class="comment-actions">
                  <button v-if="canEdit(reply)" @click="deleteReply(reply.id)">
                    삭제
                  </button>
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
export default {
  name: 'CommunityPost',
  data() {
    return {
      post: {
        title: 'AI 크리에이터로 수익 창출하기: 나의 경험담',
        tag: '경험공유',
        createdAt: new Date(2025, 2, 4),
        author: {
          id: 'author1',
          name: '성공크리에이터',
          avatar: '/images/avatars/success-creator.jpg',
          bio: 'AI 콘텐츠 크리에이터 | 월 수익 1000만원 달성'
        },
        content: `
          <p>안녕하세요! 오늘은 제가 AI 크리에이터로서 수익을 창출하게 된 과정과 노하우를 공유하려고 합니다.</p>
          
          <h2>1. 시작하게 된 계기</h2>
          <p>처음에는 AI에 대한 호기심으로 시작했지만...</p>
          
          <h2>2. 주요 수익원</h2>
          <p>현재 제 수익의 대부분은 다음과 같은 sources에서 발생합니다:</p>
          <ul>
            <li>AI 생성 디지털 아트 판매</li>
            <li>AI 도구 활용 강의</li>
            <li>컨설팅 서비스</li>
          </ul>
          
          <h2>3. 성공 노하우</h2>
          <p>가장 중요한 것은 꾸준함입니다...</p>
        `,
        likes: 342,
        views: 2891,
        comments: [
          {
            id: 1,
            author: {
              id: 'user2',
              name: '열심히하자',
              avatar: '/images/avatars/user2.jpg'
            },
            content: '정말 좋은 인사이트네요! AI 아트 판매는 어떤 플랫폼을 주로 이용하시나요?',
            createdAt: new Date(2025, 2, 4, 15, 30),
            replies: [
              {
                id: 2,
                author: {
                  id: 'author1',
                  name: '성공크리에이터',
                  avatar: '/images/avatars/success-creator.jpg'
                },
                content: 'OpenSea와 Foundation을 주로 사용하고 있어요!',
                createdAt: new Date(2025, 2, 4, 16, 0)
              }
            ]
          }
        ]
      },
      newComment: '',
      replyContent: '',
      currentUser: {
        id: 'user1',
        name: '현재사용자',
        avatar: '/images/avatars/current-user.jpg'
      }
    }
  },
  methods: {
    canEdit(item) {
      return item.author.id === this.currentUser.id
    },
    canDelete(item) {
      return item.author.id === this.currentUser.id
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('ko-KR')
    },
    likePost() {
      this.post.isLiked = !this.post.isLiked
      this.post.likes += this.post.isLiked ? 1 : -1
    },
    sharePost() {
      // 공유 기능 구현
    },
    reportPost() {
      // 신고 기능 구현
    },
    async addComment() {
      if (this.newComment.trim()) {
        // 댓글 추가 로직 구현
        console.log('새 댓글:', this.newComment)
        this.newComment = ''
      }
    },
    async addReply(commentId) {
      if (this.replyContent.trim()) {
        // 답글 추가 로직 구현
        console.log('새 답글:', commentId, this.replyContent)
        this.replyContent = ''
      }
    },
    async deleteComment(commentId) {
      // 댓글 삭제 로직 구현
      console.log('댓글 삭제:', commentId)
    },
    async deleteReply(replyId) {
      // 답글 삭제 로직 구현
      console.log('답글 삭제:', replyId)
    },
    toggleReply(comment) {
      this.$set(comment, 'showReplyForm', !comment.showReplyForm)
    }
  }
}
</script>

<style scoped>
.post-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.post-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.post-header {
  margin-bottom: 2rem;
}

.post-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.post-tag {
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border-radius: 15px;
  font-size: 0.875rem;
}

.post-time {
  color: #666;
  font-size: 0.875rem;
}

.post-header h1 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-info img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.author-info p {
  color: #666;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.post-body {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
}

.post-body h2 {
  font-size: 1.5rem;
  margin: 2rem 0 1rem;
}

.post-body p {
  margin-bottom: 1rem;
}

.post-body ul {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.post-footer {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-stats {
  display: flex;
  gap: 1rem;
}

.stat-button,
.action-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.stat-button:hover,
.action-button:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.post-actions {
  display: flex;
  gap: 1rem;
}

.comments-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comments-section h2 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.comment-form {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.comment-form img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.form-content {
  flex: 1;
}

.form-content textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  resize: vertical;
  margin-bottom: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-button,
.submit-button {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
}

.cancel-button {
  background: white;
  border: 1px solid #eee;
  color: #666;
}

.submit-button {
  background: var(--primary-color);
  border: none;
  color: white;
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.comments-list {
  display: grid;
  gap: 2rem;
}

.comment {
  border-bottom: 1px solid #eee;
  padding-bottom: 2rem;
}

.comment:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.commenter-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.commenter-info img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.comment-time {
  color: #666;
  font-size: 0.75rem;
  margin-left: 0.5rem;
}

.comment-actions button {
  padding: 0.25rem 0.5rem;
  border: none;
  background: none;
  color: #666;
  cursor: pointer;
}

.comment-content {
  color: #333;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.comment-footer {
  display: flex;
  gap: 1rem;
}

.reply-button,
.like-button {
  padding: 0.25rem 0.75rem;
  border: 1px solid #eee;
  border-radius: 15px;
  background: white;
  color: #666;
  cursor: pointer;
}

.reply-form {
  margin: 1rem 0;
  display: flex;
  gap: 1rem;
}

.replies-list {
  margin-top: 1rem;
  padding-left: 3rem;
}

.reply {
  padding: 1rem 0;
  border-left: 2px solid #eee;
  padding-left: 1rem;
}

@media (max-width: 768px) {
  .post-header h1 {
    font-size: 1.5rem;
  }

  .post-footer {
    flex-direction: column;
    gap: 1rem;
  }

  .post-stats,
  .post-actions {
    width: 100%;
    justify-content: space-between;
  }

  .comment-form {
    flex-direction: column;
  }

  .comment-form img {
    display: none;
  }

  .replies-list {
    padding-left: 1rem;
  }
}
</style>

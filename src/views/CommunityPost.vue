<template>
  <div class="community-post">
    <div class="container py-5">
      <!-- 게시글 내용 -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start mb-4">
            <div class="post-meta">
              <span class="badge bg-primary me-2">{{ post.category }}</span>
              <small class="text-muted">{{ post.created_at }}</small>
            </div>
            <div class="dropdown">
              <button class="btn btn-link text-muted" data-bs-toggle="dropdown">
                <i class="fas fa-ellipsis-v"></i>
              </button>
              <ul class="dropdown-menu">
                <li v-if="isAuthor">
                  <a class="dropdown-item" href="#" @click="editPost">
                    <i class="fas fa-edit me-2"></i>수정하기
                  </a>
                </li>
                <li v-if="isAuthor">
                  <a class="dropdown-item text-danger" href="#" @click="deletePost">
                    <i class="fas fa-trash me-2"></i>삭제하기
                  </a>
                </li>
                <li v-if="!isAuthor">
                  <a class="dropdown-item" href="#" @click="reportPost">
                    <i class="fas fa-flag me-2"></i>신고하기
                  </a>
                </li>
                <li>
                  <a class="dropdown-item" href="#" @click="sharePost">
                    <i class="fas fa-share me-2"></i>공유하기
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <h1 class="mb-4">{{ post.title }}</h1>

          <div class="author-info d-flex align-items-center mb-4">
            <img :src="post.author.avatar" class="rounded-circle me-3" width="50" height="50">
            <div>
              <h5 class="mb-0">{{ post.author.username }}</h5>
              <small class="text-muted">
                <i class="fas fa-eye me-2"></i>{{ post.view_count }} 조회
              </small>
            </div>
          </div>

          <!-- 게시글 본문 -->
          <div class="post-content mb-4" v-html="post.content"></div>

          <!-- 이미지 갤러리 -->
          <div v-if="post.images && post.images.length" class="image-gallery mb-4">
            <div class="row g-3">
              <div v-for="image in post.images" :key="image" class="col-md-4">
                <img :src="image" class="img-fluid rounded" @click="showImageModal(image)">
              </div>
            </div>
          </div>

          <!-- 태그 -->
          <div class="post-tags mb-4">
            <a v-for="tag in post.tags" 
               :key="tag" 
               href="#" 
               class="badge bg-light text-dark me-2"
               @click="searchByTag(tag)"
            >
              #{{ tag }}
            </a>
          </div>

          <!-- 좋아요 & 공유 버튼 -->
          <div class="post-actions d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center">
              <button 
                class="btn btn-link text-muted me-4"
                @click="toggleLike"
              >
                <i :class="['far', 'fa-heart', {'fas text-danger': post.is_liked}]"></i>
                좋아요 {{ post.like_count }}
              </button>
              <button 
                class="btn btn-link text-muted me-4"
                @click="focusCommentInput"
              >
                <i class="far fa-comment"></i>
                댓글 {{ post.comment_count }}
              </button>
              <button 
                class="btn btn-link text-muted"
                @click="sharePost"
              >
                <i class="far fa-share-square"></i>
                공유하기
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <h4 class="mb-4">
          댓글 
          <span class="text-muted">{{ post.comment_count }}</span>
        </h4>

        <!-- 댓글 작성 폼 -->
        <div class="card mb-4">
          <div class="card-body">
            <form @submit.prevent="submitComment">
              <div class="mb-3">
                <textarea 
                  ref="commentInput"
                  v-model="newComment.content"
                  class="form-control"
                  rows="3"
                  placeholder="댓글을 작성해주세요..."
                  required
                ></textarea>
              </div>
              <div class="text-end">
                <button type="submit" class="btn btn-primary">
                  댓글 작성
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- 댓글 목록 -->
        <div class="comments-list">
          <div v-for="comment in post.comments" :key="comment.id" class="card mb-3">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div class="user-info d-flex align-items-center">
                  <img :src="comment.author.avatar" class="rounded-circle me-2" width="30" height="30">
                  <div>
                    <h6 class="mb-0">{{ comment.author.username }}</h6>
                    <small class="text-muted">{{ comment.created_at }}</small>
                  </div>
                </div>
                <div class="dropdown" v-if="isCommentAuthor(comment)">
                  <button class="btn btn-link text-muted" data-bs-toggle="dropdown">
                    <i class="fas fa-ellipsis-v"></i>
                  </button>
                  <ul class="dropdown-menu">
                    <li>
                      <a class="dropdown-item" href="#" @click="editComment(comment)">
                        <i class="fas fa-edit me-2"></i>수정
                      </a>
                    </li>
                    <li>
                      <a class="dropdown-item text-danger" href="#" @click="deleteComment(comment)">
                        <i class="fas fa-trash me-2"></i>삭제
                      </a>
                    </li>
                  </ul>
                </div>
              </div>

              <p class="mb-3">{{ comment.content }}</p>

              <div class="d-flex align-items-center">
                <button 
                  class="btn btn-link text-muted p-0 me-3"
                  @click="toggleCommentLike(comment)"
                >
                  <i :class="['far', 'fa-heart', {'fas text-danger': comment.is_liked}]"></i>
                  {{ comment.like_count }}
                </button>
                <button 
                  class="btn btn-link text-muted p-0"
                  @click="replyToComment(comment)"
                >
                  답글달기
                </button>
              </div>

              <!-- 대댓글 -->
              <div v-if="comment.replies && comment.replies.length" class="replies mt-3">
                <div v-for="reply in comment.replies" :key="reply.id" class="reply border-start ps-3 mt-3">
                  <div class="d-flex justify-content-between align-items-start">
                    <div class="user-info d-flex align-items-center">
                      <img :src="reply.author.avatar" class="rounded-circle me-2" width="25" height="25">
                      <div>
                        <h6 class="mb-0">{{ reply.author.username }}</h6>
                        <small class="text-muted">{{ reply.created_at }}</small>
                      </div>
                    </div>
                  </div>
                  <p class="mb-2 mt-2">{{ reply.content }}</p>
                  <button 
                    class="btn btn-link text-muted p-0"
                    @click="toggleCommentLike(reply)"
                  >
                    <i :class="['far', 'fa-heart', {'fas text-danger': reply.is_liked}]"></i>
                    {{ reply.like_count }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 더보기 버튼 -->
        <div v-if="hasMoreComments" class="text-center mt-4">
          <button 
            class="btn btn-outline-primary"
            @click="loadMoreComments"
            :disabled="loadingComments"
          >
            <span v-if="loadingComments" class="spinner-border spinner-border-sm me-2"></span>
            댓글 더보기
          </button>
        </div>
      </div>
    </div>

    <!-- 이미지 모달 -->
    <div class="modal fade" id="imageModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-body p-0">
            <img :src="selectedImage" class="img-fluid">
          </div>
        </div>
      </div>
    </div>

    <!-- 댓글 수정 모달 -->
    <div class="modal fade" id="editCommentModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">댓글 수정</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <textarea 
              v-model="editingComment.content"
              class="form-control"
              rows="3"
              required
            ></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              취소
            </button>
            <button type="button" class="btn btn-primary" @click="updateComment">
              수정하기
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'
import axios from 'axios'

export default {
  name: 'CommunityPost',
  data() {
    return {
      post: {
        id: null,
        title: '',
        content: '',
        category: '',
        author: {
          id: null,
          username: '',
          avatar: ''
        },
        created_at: '',
        view_count: 0,
        like_count: 0,
        comment_count: 0,
        is_liked: false,
        tags: [],
        images: [],
        comments: []
      },
      newComment: {
        content: ''
      },
      editingComment: {
        id: null,
        content: ''
      },
      selectedImage: '',
      loadingComments: false,
      hasMoreComments: false,
      currentPage: 1
    }
  },
  computed: {
    isAuthor() {
      return this.post.author.id === this.$store.state.user.id
    }
  },
  methods: {
    async fetchPost() {
      try {
        const response = await axios.get(`/api/posts/${this.$route.params.id}`, {
          params: {
            user_id: this.$store.state.user.id
          }
        })
        this.post = response.data
      } catch (error) {
        console.error('게시글 로드 실패:', error)
        this.$router.push('/community')
      }
    },

    async toggleLike() {
      try {
        const response = await axios.post(`/api/posts/${this.post.id}/like`, {
          user_id: this.$store.state.user.id
        })
        this.post.is_liked = response.data.is_liked
        this.post.like_count = response.data.like_count
      } catch (error) {
        console.error('좋아요 토글 실패:', error)
      }
    },

    async submitComment() {
      try {
        const response = await axios.post(`/api/posts/${this.post.id}/comments`, {
          user_id: this.$store.state.user.id,
          content: this.newComment.content
        })
        this.post.comments.unshift(response.data)
        this.post.comment_count++
        this.newComment.content = ''
      } catch (error) {
        console.error('댓글 작성 실패:', error)
      }
    },

    async toggleCommentLike(comment) {
      try {
        const response = await axios.post(`/api/comments/${comment.id}/like`, {
          user_id: this.$store.state.user.id
        })
        comment.is_liked = response.data.is_liked
        comment.like_count = response.data.like_count
      } catch (error) {
        console.error('댓글 좋아요 토글 실패:', error)
      }
    },

    editComment(comment) {
      this.editingComment = { ...comment }
      new Modal(document.getElementById('editCommentModal')).show()
    },

    async updateComment() {
      try {
        const response = await axios.put(`/api/comments/${this.editingComment.id}`, {
          content: this.editingComment.content
        })
        const index = this.post.comments.findIndex(c => c.id === this.editingComment.id)
        if (index !== -1) {
          this.post.comments[index] = response.data
        }
        new Modal(document.getElementById('editCommentModal')).hide()
      } catch (error) {
        console.error('댓글 수정 실패:', error)
      }
    },

    async deleteComment(comment) {
      if (!confirm('정말로 이 댓글을 삭제하시겠습니까?')) return

      try {
        await axios.delete(`/api/comments/${comment.id}`)
        const index = this.post.comments.findIndex(c => c.id === comment.id)
        if (index !== -1) {
          this.post.comments.splice(index, 1)
          this.post.comment_count--
        }
      } catch (error) {
        console.error('댓글 삭제 실패:', error)
      }
    },

    async loadMoreComments() {
      if (this.loadingComments) return

      this.loadingComments = true
      try {
        const response = await axios.get(`/api/posts/${this.post.id}/comments`, {
          params: {
            page: this.currentPage + 1
          }
        })
        this.post.comments.push(...response.data.comments)
        this.currentPage = response.data.page
        this.hasMoreComments = response.data.has_more
      } catch (error) {
        console.error('댓글 로드 실패:', error)
      } finally {
        this.loadingComments = false
      }
    },

    showImageModal(image) {
      this.selectedImage = image
      new Modal(document.getElementById('imageModal')).show()
    },

    focusCommentInput() {
      this.$refs.commentInput.focus()
    },

    isCommentAuthor(comment) {
      return comment.author.id === this.$store.state.user.id
    },

    searchByTag(tag) {
      this.$router.push({
        path: '/community',
        query: { tag }
      })
    },

    async editPost() {
      // TODO: 게시글 수정 구현
    },

    async deletePost() {
      if (!confirm('정말로 이 게시글을 삭제하시겠습니까?')) return

      try {
        await axios.delete(`/api/posts/${this.post.id}`)
        this.$router.push('/community')
      } catch (error) {
        console.error('게시글 삭제 실패:', error)
      }
    },

    async reportPost() {
      // TODO: 게시글 신고 구현
    },

    sharePost() {
      // TODO: 공유 기능 구현
    },

    replyToComment(comment) {
      this.newComment.content = `@${comment.author.username} `
      this.$refs.commentInput.focus()
    }
  },
  created() {
    this.fetchPost()
  }
}
</script>

<style scoped>
.community-post {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.post-content {
  font-size: 1.1rem;
  line-height: 1.8;
}

.image-gallery img {
  height: 200px;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.2s;
}

.image-gallery img:hover {
  transform: scale(1.05);
}

.user-info img {
  object-fit: cover;
}

.btn-link {
  text-decoration: none;
}

.replies {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
}

#imageModal .modal-body {
  padding: 0;
  background-color: #000;
}

#imageModal img {
  max-height: 80vh;
  width: 100%;
  object-fit: contain;
}
</style>

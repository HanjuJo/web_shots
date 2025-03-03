<template>
  <div class="community">
    <div class="container py-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>크리에이터 커뮤니티</h1>
        <button class="btn btn-primary" @click="showCreatePostModal">
          <i class="fas fa-plus me-2"></i>글쓰기
        </button>
      </div>

      <!-- 검색 및 필터 -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="게시글 검색..."
              >
            </div>
            <div class="col-md-3">
              <select v-model="selectedCategory" class="form-select">
                <option value="">모든 카테고리</option>
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
            <div class="col-md-3">
              <select v-model="sortBy" class="form-select">
                <option value="latest">최신순</option>
                <option value="popular">인기순</option>
                <option value="views">조회순</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- 인기 게시글 -->
      <div class="trending-posts mb-5" v-if="!searchQuery">
        <h4 class="mb-3">🔥 인기 게시글</h4>
        <div class="row g-4">
          <div v-for="post in trendingPosts" :key="post.id" class="col-md-4">
            <div class="card h-100">
              <img v-if="post.thumbnail" :src="post.thumbnail" class="card-img-top" :alt="post.title">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <span class="badge bg-primary">{{ post.category }}</span>
                  <small class="text-muted">{{ post.createdAt }}</small>
                </div>
                <h5 class="card-title">{{ post.title }}</h5>
                <p class="card-text">{{ post.excerpt }}</p>
                <div class="post-meta d-flex justify-content-between align-items-center">
                  <div class="user-info d-flex align-items-center">
                    <img :src="post.author.avatar" class="rounded-circle me-2" width="30" height="30">
                    <span>{{ post.author.name }}</span>
                  </div>
                  <div class="post-stats">
                    <span class="me-3"><i class="far fa-heart"></i> {{ post.likes }}</span>
                    <span><i class="far fa-comment"></i> {{ post.comments }}</span>
                  </div>
                </div>
              </div>
              <div class="card-footer bg-transparent">
                <router-link :to="'/community/post/' + post.id" class="btn btn-outline-primary w-100">
                  자세히 보기
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 게시글 목록 -->
      <div class="posts">
        <div class="row g-4">
          <div v-for="post in filteredPosts" :key="post.id" class="col-md-6">
            <div class="card h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <div>
                    <span class="badge bg-primary me-2">{{ post.category }}</span>
                    <small class="text-muted">{{ post.createdAt }}</small>
                  </div>
                  <div class="dropdown">
                    <button class="btn btn-link text-muted" data-bs-toggle="dropdown">
                      <i class="fas fa-ellipsis-v"></i>
                    </button>
                    <ul class="dropdown-menu">
                      <li><a class="dropdown-item" href="#"><i class="fas fa-flag me-2"></i>신고하기</a></li>
                      <li><a class="dropdown-item" href="#"><i class="fas fa-share me-2"></i>공유하기</a></li>
                    </ul>
                  </div>
                </div>

                <h5 class="card-title mb-3">{{ post.title }}</h5>
                <p class="card-text">{{ post.excerpt }}</p>

                <div class="post-tags mb-3">
                  <a v-for="tag in post.tags" 
                     :key="tag" 
                     href="#" 
                     class="badge bg-light text-dark me-2"
                  >
                    #{{ tag }}
                  </a>
                </div>

                <div class="d-flex justify-content-between align-items-center">
                  <div class="user-info d-flex align-items-center">
                    <img :src="post.author.avatar" class="rounded-circle me-2" width="30" height="30">
                    <span>{{ post.author.name }}</span>
                  </div>
                  <div class="post-stats">
                    <button class="btn btn-link text-muted me-3" @click="likePost(post)">
                      <i :class="['far', post.isLiked ? 'fas fa-heart text-danger' : 'far fa-heart']"></i>
                      {{ post.likes }}
                    </button>
                    <button class="btn btn-link text-muted">
                      <i class="far fa-comment"></i>
                      {{ post.comments }}
                    </button>
                  </div>
                </div>
              </div>
              <div class="card-footer bg-transparent">
                <router-link :to="'/community/post/' + post.id" class="btn btn-outline-primary w-100">
                  자세히 보기
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- 더보기 버튼 -->
        <div class="text-center mt-4">
          <button class="btn btn-outline-primary" @click="loadMorePosts" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            더보기
          </button>
        </div>
      </div>

      <!-- 글쓰기 모달 -->
      <div class="modal fade" id="createPostModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">새 게시글 작성</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="createPost">
                <div class="mb-3">
                  <label class="form-label">카테고리</label>
                  <select v-model="newPost.category" class="form-select" required>
                    <option v-for="category in categories" :key="category" :value="category">
                      {{ category }}
                    </option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label">제목</label>
                  <input v-model="newPost.title" type="text" class="form-control" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">내용</label>
                  <textarea v-model="newPost.content" class="form-control" rows="5" required></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">태그</label>
                  <input v-model="newPost.tags" type="text" class="form-control" placeholder="쉼표로 구분">
                </div>
                <div class="mb-3">
                  <label class="form-label">이미지 첨부</label>
                  <input type="file" class="form-control" accept="image/*" multiple>
                </div>
                <div class="text-end">
                  <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">
                    취소
                  </button>
                  <button type="submit" class="btn btn-primary">
                    작성하기
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'

export default {
  name: 'CommunityPage',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      sortBy: 'latest',
      loading: false,
      categories: ['작업물 공유', '질문/답변', '정보/팁', '모집/구인', '잡담'],
      newPost: {
        category: '',
        title: '',
        content: '',
        tags: ''
      },
      trendingPosts: [
        {
          id: 1,
          title: 'Midjourney로 만든 제 첫 작품입니다!',
          excerpt: '처음으로 Midjourney를 사용해서 작품을 만들어보았습니다. 여러분의 피드백 부탁드립니다!',
          category: '작업물 공유',
          thumbnail: require('@/assets/post-1-1.jpg'),
          author: {
            name: '크리에이터123',
            avatar: require('@/assets/avatar-1.jpg')
          },
          createdAt: '2025-03-03',
          likes: 24,
          comments: 12,
          tags: ['Midjourney', 'AI아트', '일러스트레이션']
        }
      ],
      posts: [
        {
          id: 1,
          title: 'ChatGPT로 시나리오 작성하는 팁',
          excerpt: 'ChatGPT를 활용해서 더 매력적인 시나리오를 작성하는 방법을 공유합니다.',
          category: '정보/팁',
          author: {
            name: '시나리오작가',
            avatar: require('@/assets/avatar-2.jpg')
          },
          createdAt: '2025-03-03',
          likes: 15,
          comments: 8,
          isLiked: false,
          tags: ['ChatGPT', '시나리오', '콘텐츠제작']
        }
      ]
    }
  },
  computed: {
    filteredPosts() {
      let result = [...this.posts]
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(post => 
          post.title.toLowerCase().includes(query) ||
          post.excerpt.toLowerCase().includes(query)
        )
      }
      
      if (this.selectedCategory) {
        result = result.filter(post => post.category === this.selectedCategory)
      }
      
      // 정렬
      switch (this.sortBy) {
        case 'popular':
          result.sort((a, b) => b.likes - a.likes)
          break
        case 'views':
          result.sort((a, b) => b.views - a.views)
          break
        default:
          result.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
      }
      
      return result
    }
  },
  methods: {
    showCreatePostModal() {
      new Modal(document.getElementById('createPostModal')).show()
    },
    
    async createPost() {
      // API 호출 및 게시글 생성 로직
      console.log('Creating post:', this.newPost)
    },
    
    likePost(post) {
      post.isLiked = !post.isLiked
      post.likes += post.isLiked ? 1 : -1
    },
    
    async loadMorePosts() {
      this.loading = true
      // API 호출 및 추가 게시글 로드 로직
      await new Promise(resolve => setTimeout(resolve, 1000))
      this.loading = false
    }
  }
}
</script>

<style scoped>
.community {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.user-info img {
  object-fit: cover;
}

.post-stats button {
  padding: 0;
  text-decoration: none;
}

.post-stats button:hover {
  color: var(--bs-primary) !important;
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.trending-posts .card {
  border-top: 3px solid var(--bs-primary);
}
</style>

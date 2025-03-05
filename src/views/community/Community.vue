<template>
  <div class="community-page">
    <!-- 커뮤니티 헤더 -->
    <section class="community-header">
      <div class="header-content">
        <h1>크리에이터 커뮤니티</h1>
        <p>다른 크리에이터들과 경험을 공유하고 함께 성장하세요</p>
        <router-link to="/community/post/new" class="create-post-button">
          <i class="fas fa-plus"></i>
          새 글 작성
        </router-link>
      </div>
    </section>

    <!-- 검색 및 필터 -->
    <section class="search-filter">
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="커뮤니티 검색..."
          @input="filterPosts"
        >
      </div>
      <div class="filter-tags">
        <button 
          v-for="tag in tags" 
          :key="tag.id"
          :class="['filter-tag', { active: selectedTags.includes(tag.id) }]"
          @click="toggleTag(tag.id)"
        >
          {{ tag.name }}
        </button>
      </div>
      <div class="sort-options">
        <select v-model="sortBy" @change="sortPosts">
          <option value="recent">최신순</option>
          <option value="popular">인기순</option>
          <option value="comments">댓글순</option>
        </select>
      </div>
    </section>

    <!-- 인기 게시글 -->
    <section class="trending-posts" v-if="trendingPosts.length && !searchQuery">
      <h2>인기 게시글</h2>
      <div class="trending-grid">
        <article 
          v-for="post in trendingPosts" 
          :key="post.id"
          class="trending-card"
          @click="goToPost(post.id)"
        >
          <img v-if="post.image" :src="post.image" :alt="post.title">
          <div class="trending-content">
            <div class="post-meta">
              <span class="post-tag">{{ post.tag }}</span>
              <span class="post-time">{{ formatTime(post.createdAt) }}</span>
            </div>
            <h3>{{ post.title }}</h3>
            <p>{{ post.excerpt }}</p>
            <div class="author-info">
              <img :src="post.author.avatar" :alt="post.author.name">
              <span>{{ post.author.name }}</span>
            </div>
            <div class="post-stats">
              <span><i class="fas fa-heart"></i> {{ post.likes }}</span>
              <span><i class="fas fa-comment"></i> {{ post.comments }}</span>
              <span><i class="fas fa-eye"></i> {{ post.views }}</span>
            </div>
          </div>
        </article>
      </div>
    </section>

    <!-- 게시글 목록 -->
    <section class="posts-grid">
      <article 
        v-for="post in filteredPosts" 
        :key="post.id"
        class="post-card"
        @click="goToPost(post.id)"
      >
        <img v-if="post.image" :src="post.image" :alt="post.title" class="post-image">
        <div class="post-content">
          <div class="post-meta">
            <span class="post-tag">{{ post.tag }}</span>
            <span class="post-time">{{ formatTime(post.createdAt) }}</span>
          </div>
          <h3>{{ post.title }}</h3>
          <p>{{ post.excerpt }}</p>
          <div class="author-info">
            <img :src="post.author.avatar" :alt="post.author.name">
            <span>{{ post.author.name }}</span>
          </div>
          <div class="post-stats">
            <span><i class="fas fa-heart"></i> {{ post.likes }}</span>
            <span><i class="fas fa-comment"></i> {{ post.comments }}</span>
            <span><i class="fas fa-eye"></i> {{ post.views }}</span>
          </div>
        </div>
      </article>
    </section>

    <!-- 페이지네이션 -->
    <div class="pagination" v-if="totalPages > 1">
      <button 
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        <i class="fas fa-chevron-left"></i>
      </button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button 
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommunityView',
  data() {
    return {
      searchQuery: '',
      selectedTags: [],
      sortBy: 'recent',
      currentPage: 1,
      itemsPerPage: 9,
      tags: [
        { id: 1, name: '질문/답변' },
        { id: 2, name: '팁/노하우' },
        { id: 3, name: '작업물 공유' },
        { id: 4, name: '토론' },
        { id: 5, name: '홍보' }
      ],
      posts: [
        {
          id: 1,
          title: 'AI로 썸네일 제작하는 꿀팁!',
          excerpt: 'Stable Diffusion을 활용한 매력적인 썸네일 제작 방법을 공유합니다.',
          image: '/images/posts/thumbnail-tips.jpg',
          tag: '팁/노하우',
          createdAt: new Date(Date.now() - 1000 * 60 * 30), // 30분 전
          author: {
            name: '썸네일장인',
            avatar: '/images/avatars/thumbnail-master.jpg'
          },
          likes: 128,
          comments: 32,
          views: 1502
        },
        {
          id: 2,
          title: 'AI 음성 더빙 퀄리티 높이는 방법',
          excerpt: '자연스러운 AI 음성 더빙을 위한 설정과 후보정 방법을 알려드립니다.',
          image: '/images/posts/voice-tips.jpg',
          tag: '팁/노하우',
          createdAt: new Date(Date.now() - 1000 * 60 * 60), // 1시간 전
          author: {
            name: '보이스프로',
            avatar: '/images/avatars/voice-pro.jpg'
          },
          likes: 95,
          comments: 28,
          views: 1205
        },
        {
          id: 3,
          title: '처음 시작하는 AI 크리에이터를 위한 조언',
          excerpt: '제가 AI 크리에이터로 활동하면서 얻은 경험과 조언을 공유합니다.',
          image: '/images/posts/beginner-tips.jpg',
          tag: '토론',
          createdAt: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2시간 전
          author: {
            name: 'AI튜터',
            avatar: '/images/avatars/ai-tutor.jpg'
          },
          likes: 156,
          comments: 45,
          views: 2103
        }
      ],
      trendingPosts: [
        {
          id: 4,
          title: 'AI 도구로 월 수익 1000만원 달성 후기',
          excerpt: 'AI 도구를 활용한 콘텐츠 제작으로 수익화에 성공한 경험을 공유합니다.',
          image: '/images/posts/success-story.jpg',
          tag: '팁/노하우',
          createdAt: new Date(Date.now() - 1000 * 60 * 60 * 3), // 3시간 전
          author: {
            name: '성공크리에이터',
            avatar: '/images/avatars/success-creator.jpg'
          },
          likes: 312,
          comments: 89,
          views: 5204
        },
        {
          id: 5,
          title: 'AI 편집 자동화로 작업 시간 단축하기',
          excerpt: '영상 편집 워크플로우를 자동화하여 제작 시간을 획기적으로 줄인 방법',
          image: '/images/posts/workflow.jpg',
          tag: '팁/노하우',
          createdAt: new Date(Date.now() - 1000 * 60 * 60 * 4), // 4시간 전
          author: {
            name: '효율왕',
            avatar: '/images/avatars/efficiency-king.jpg'
          },
          likes: 245,
          comments: 67,
          views: 3856
        }
      ]
    }
  },
  computed: {
    filteredPosts() {
      let filtered = this.posts

      // 검색어 필터링
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(post => 
          post.title.toLowerCase().includes(query) ||
          post.excerpt.toLowerCase().includes(query)
        )
      }

      // 태그 필터링
      if (this.selectedTags.length) {
        filtered = filtered.filter(post =>
          this.selectedTags.some(tagId => 
            this.tags.find(t => t.id === tagId)?.name === post.tag
          )
        )
      }

      // 정렬
      filtered = [...filtered].sort((a, b) => {
        switch (this.sortBy) {
          case 'popular':
            return b.likes - a.likes
          case 'comments':
            return b.comments - a.comments
          default: // recent
            return b.createdAt - a.createdAt
        }
      })

      return filtered
    },
    totalPages() {
      return Math.ceil(this.filteredPosts.length / this.itemsPerPage)
    },
    paginatedPosts() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredPosts.slice(start, end)
    }
  },
  methods: {
    filterPosts() {
      this.currentPage = 1
    },
    toggleTag(tagId) {
      const index = this.selectedTags.indexOf(tagId)
      if (index === -1) {
        this.selectedTags.push(tagId)
      } else {
        this.selectedTags.splice(index, 1)
      }
      this.currentPage = 1
    },
    sortPosts() {
      this.currentPage = 1
    },
    formatTime(time) {
      const now = new Date()
      const diff = now - time
      const minutes = Math.floor(diff / 1000 / 60)
      const hours = Math.floor(minutes / 60)
      const days = Math.floor(hours / 24)

      if (days > 0) return `${days}일 전`
      if (hours > 0) return `${hours}시간 전`
      if (minutes > 0) return `${minutes}분 전`
      return '방금 전'
    },
    goToPost(postId) {
      this.$router.push(`/community/post/${postId}`)
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    }
  }
}
</script>

<style scoped>
.community-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* 커뮤니티 헤더 */
.community-header {
  background: linear-gradient(135deg, var(--primary-color) 0%, #6366f1 100%);
  border-radius: 20px;
  padding: 4rem 2rem;
  margin-bottom: 3rem;
  text-align: center;
  color: white;
}

.header-content h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.header-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.create-post-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: white;
  color: var(--primary-color);
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: transform 0.3s ease;
}

.create-post-button:hover {
  transform: translateY(-2px);
}

/* 검색 및 필터 */
.search-filter {
  margin-bottom: 3rem;
  display: grid;
  gap: 1rem;
}

.search-box {
  position: relative;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-box input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-tag {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-tag.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.sort-options select {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: white;
  cursor: pointer;
}

/* 인기 게시글 */
.trending-posts {
  margin-bottom: 4rem;
}

.trending-posts h2 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.trending-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.trending-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.trending-card:hover {
  transform: translateY(-5px);
}

.trending-card img {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.trending-content {
  padding: 1.5rem;
}

/* 게시글 목록 */
.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.post-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.post-card:hover {
  transform: translateY(-5px);
}

.post-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.post-content {
  padding: 1.5rem;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.post-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.post-content p {
  color: #666;
  margin-bottom: 1rem;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.author-info img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.post-stats {
  display: flex;
  gap: 1rem;
  color: #666;
  font-size: 0.875rem;
}

.post-stats span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination button:not(:disabled):hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .community-header {
    padding: 3rem 1rem;
  }

  .header-content h1 {
    font-size: 2rem;
  }

  .trending-grid {
    grid-template-columns: 1fr;
  }

  .posts-grid {
    grid-template-columns: 1fr;
  }
}
</style>

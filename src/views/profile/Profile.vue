<template>
  <div class="profile-page">
    <div class="profile-header">
      <div class="profile-cover">
        <img :src="profile.coverImage" alt="커버 이미지">
        <button class="edit-cover" @click="editCover">
          <i class="fas fa-camera"></i>
        </button>
      </div>
      
      <div class="profile-info">
        <div class="profile-avatar">
          <img :src="profile.avatar" :alt="profile.name">
          <button class="edit-avatar" @click="editAvatar">
            <i class="fas fa-camera"></i>
          </button>
        </div>
        
        <div class="profile-details">
          <div class="profile-name">
            <h1>{{ profile.name }}</h1>
            <span class="profile-badge" v-if="profile.verified">
              <i class="fas fa-check-circle"></i> 인증된 크리에이터
            </span>
          </div>
          <p class="profile-bio">{{ profile.bio }}</p>
          <div class="profile-meta">
            <span><i class="fas fa-map-marker-alt"></i> {{ profile.location }}</span>
            <span><i class="fas fa-link"></i> {{ profile.website }}</span>
            <span><i class="fas fa-calendar"></i> 가입일: {{ formatDate(profile.joinDate) }}</span>
          </div>
        </div>

        <div class="profile-stats">
          <div class="stat">
            <span class="stat-value">{{ formatNumber(profile.followers) }}</span>
            <span class="stat-label">팔로워</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ formatNumber(profile.following) }}</span>
            <span class="stat-label">팔로잉</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ formatNumber(profile.posts) }}</span>
            <span class="stat-label">게시글</span>
          </div>
        </div>

        <div class="profile-actions">
          <button class="edit-profile-button" @click="editProfile">
            프로필 편집
          </button>
        </div>
      </div>
    </div>

    <div class="profile-content">
      <nav class="profile-nav">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['nav-button', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </nav>

      <!-- 게시글 탭 -->
      <div v-if="activeTab === 'posts'" class="posts-grid">
        <article v-for="post in posts" :key="post.id" 
                 class="post-card" @click="viewPost(post)">
          <img :src="post.thumbnail" :alt="post.title">
          <div class="post-overlay">
            <h3>{{ post.title }}</h3>
            <div class="post-stats">
              <span><i class="fas fa-heart"></i> {{ formatNumber(post.likes) }}</span>
              <span><i class="fas fa-comment"></i> {{ formatNumber(post.comments) }}</span>
              <span><i class="fas fa-eye"></i> {{ formatNumber(post.views) }}</span>
            </div>
          </div>
        </article>
      </div>

      <!-- 가이드 탭 -->
      <div v-if="activeTab === 'guides'" class="guides-grid">
        <article v-for="guide in guides" :key="guide.id" 
                 class="guide-card" @click="viewGuide(guide)">
          <img :src="guide.thumbnail" :alt="guide.title">
          <div class="guide-content">
            <span class="guide-category">{{ guide.category }}</span>
            <h3>{{ guide.title }}</h3>
            <p>{{ guide.excerpt }}</p>
            <div class="guide-meta">
              <span>{{ formatDate(guide.publishedAt) }}</span>
              <span>{{ formatNumber(guide.views) }} 조회</span>
            </div>
          </div>
        </article>
      </div>

      <!-- 북마크 탭 -->
      <div v-if="activeTab === 'bookmarks'" class="bookmarks-grid">
        <article v-for="bookmark in bookmarks" :key="bookmark.id" 
                 class="bookmark-card" @click="viewBookmark(bookmark)">
          <img :src="bookmark.thumbnail" :alt="bookmark.title">
          <div class="bookmark-content">
            <span class="bookmark-type">{{ bookmark.type }}</span>
            <h3>{{ bookmark.title }}</h3>
            <p>{{ bookmark.excerpt }}</p>
            <div class="bookmark-meta">
              <span>저장일: {{ formatDate(bookmark.savedAt) }}</span>
            </div>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserProfile',
  data() {
    return {
      activeTab: 'posts',
      tabs: [
        { id: 'posts', label: '게시글' },
        { id: 'guides', label: '가이드' },
        { id: 'bookmarks', label: '북마크' }
      ],
      profile: {
        name: '김크리에이터',
        bio: 'AI 크리에이터 | 콘텐츠 제작 전문가 | 10만 구독자',
        avatar: '/images/avatars/profile.jpg',
        coverImage: '/images/covers/profile-cover.jpg',
        verified: true,
        location: '서울',
        website: 'creator.example.com',
        joinDate: new Date(2024, 0, 1),
        followers: 100000,
        following: 1250,
        posts: 89
      },
      posts: [
        {
          id: 1,
          title: 'AI로 썸네일 제작하기',
          thumbnail: '/images/posts/thumbnail1.jpg',
          likes: 1200,
          comments: 85,
          views: 15000
        },
        {
          id: 2,
          title: '초보자를 위한 AI 작업 가이드',
          thumbnail: '/images/posts/thumbnail2.jpg',
          likes: 980,
          comments: 64,
          views: 12000
        }
      ],
      guides: [
        {
          id: 1,
          title: 'AI 이미지 생성 완벽 가이드',
          category: '초급',
          thumbnail: '/images/guides/guide1.jpg',
          excerpt: 'Stable Diffusion을 활용한 고품질 이미지 생성 방법',
          publishedAt: new Date(2025, 2, 1),
          views: 8500
        },
        {
          id: 2,
          title: 'AI 음성 더빙 마스터하기',
          category: '중급',
          thumbnail: '/images/guides/guide2.jpg',
          excerpt: '자연스러운 AI 음성 더빙을 위한 설정과 후보정',
          publishedAt: new Date(2025, 2, 3),
          views: 6200
        }
      ],
      bookmarks: [
        {
          id: 1,
          type: '도구',
          title: 'AI 이미지 생성기',
          thumbnail: '/images/tools/tool1.jpg',
          excerpt: '최신 AI 기술을 활용한 이미지 생성 도구',
          savedAt: new Date(2025, 2, 4)
        },
        {
          id: 2,
          type: '가이드',
          title: 'AI 작업 자동화 가이드',
          thumbnail: '/images/guides/guide3.jpg',
          excerpt: '작업 효율을 높이는 자동화 방법',
          savedAt: new Date(2025, 2, 5)
        }
      ]
    }
  },
  methods: {
    formatNumber(num) {
      return new Intl.NumberFormat('ko-KR').format(num)
    },
    formatDate(date) {
      return new Intl.DateTimeFormat('ko-KR').format(date)
    },
    editCover() {
      // 커버 이미지 편집 구현
    },
    editAvatar() {
      // 프로필 이미지 편집 구현
    },
    editProfile() {
      // 프로필 편집 구현
    },
    viewPost(post) {
      this.$router.push(`/community/post/${post.id}`)
    },
    viewGuide(guide) {
      this.$router.push(`/guides/${guide.id}`)
    },
    viewBookmark(bookmark) {
      // 북마크 타입에 따라 다른 페이지로 이동
      if (bookmark.type === '도구') {
        this.$router.push(`/tools/${bookmark.id}`)
      } else if (bookmark.type === '가이드') {
        this.$router.push(`/guides/${bookmark.id}`)
      }
    }
  }
}
</script>

<style scoped>
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.profile-header {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.profile-cover {
  position: relative;
  height: 300px;
}

.profile-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.edit-cover,
.edit-avatar {
  position: absolute;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.edit-cover {
  right: 1rem;
  bottom: 1rem;
}

.profile-info {
  position: relative;
  padding: 0 2rem 2rem;
}

.profile-avatar {
  position: relative;
  margin-top: -80px;
  margin-bottom: 1rem;
}

.profile-avatar img {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  border: 4px solid white;
  object-fit: cover;
}

.edit-avatar {
  right: 0;
  bottom: 0;
}

.profile-name {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.profile-name h1 {
  font-size: 2rem;
}

.profile-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border-radius: 15px;
  font-size: 0.875rem;
}

.profile-bio {
  color: #666;
  margin-bottom: 1rem;
}

.profile-meta {
  display: flex;
  gap: 2rem;
  color: #666;
  font-size: 0.875rem;
}

.profile-stats {
  display: flex;
  gap: 2rem;
  margin: 2rem 0;
}

.stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: #666;
  font-size: 0.875rem;
}

.profile-actions {
  display: flex;
  justify-content: flex-end;
}

.edit-profile-button {
  padding: 0.75rem 1.5rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.profile-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.nav-button {
  padding: 1rem;
  background: none;
  border: none;
  color: #666;
  font-weight: 500;
  cursor: pointer;
  position: relative;
}

.nav-button.active {
  color: var(--primary-color);
}

.nav-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--primary-color);
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
}

.post-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
}

.post-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.post-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
}

.post-overlay h3 {
  margin-bottom: 0.5rem;
}

.post-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
}

.guides-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.guide-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.guide-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.guide-content {
  padding: 1.5rem;
}

.guide-category {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border-radius: 15px;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.guide-content h3 {
  margin-bottom: 0.5rem;
}

.guide-content p {
  color: #666;
  margin-bottom: 1rem;
}

.guide-meta {
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 0.875rem;
}

.bookmarks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.bookmark-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.bookmark-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.bookmark-content {
  padding: 1.5rem;
}

.bookmark-type {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f8f9fa;
  color: #666;
  border-radius: 15px;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.bookmark-content h3 {
  margin-bottom: 0.5rem;
}

.bookmark-content p {
  color: #666;
  margin-bottom: 1rem;
}

.bookmark-meta {
  color: #666;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .profile-cover {
    height: 200px;
  }

  .profile-info {
    padding: 0 1rem 1rem;
  }

  .profile-avatar {
    margin-top: -60px;
  }

  .profile-avatar img {
    width: 120px;
    height: 120px;
  }

  .profile-name {
    flex-direction: column;
    align-items: flex-start;
  }

  .profile-meta {
    flex-direction: column;
    gap: 0.5rem;
  }

  .profile-stats {
    justify-content: space-around;
  }

  .profile-nav {
    overflow-x: auto;
    padding-bottom: 1rem;
  }
}
</style>

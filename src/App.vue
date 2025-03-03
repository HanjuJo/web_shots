<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
      <div class="container">
        <router-link class="navbar-brand d-flex align-items-center" to="/">
          <i class="fas fa-robot text-primary me-2"></i>
          AI Creator Tools
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <i class="fas fa-home me-1"></i>
                홈
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/tools">
                <i class="fas fa-tools me-1"></i>
                AI 도구
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/trends">
                <i class="fas fa-chart-line me-1"></i>
                트렌드
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/youtube-analytics">
                <i class="fas fa-chart-bar me-1"></i>
                유튜브 분석
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/community">
                <i class="fas fa-users me-1"></i>
                커뮤니티
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/try-ai">
                <i class="fas fa-magic me-1"></i>
                AI 체험
              </router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <button class="btn-login" v-if="!isLoggedIn">로그인</button>
              <div class="user-menu" v-else>
                <img :src="user.avatar" :alt="user.name" @click="toggleUserMenu">
                <div class="dropdown-menu" v-if="isUserMenuOpen">
                  <div class="user-info">
                    <img :src="user.avatar" :alt="user.name">
                    <div>
                      <h4>{{ user.name }}</h4>
                      <p>{{ user.email }}</p>
                    </div>
                  </div>
                  <div class="menu-items">
                    <a href="#" class="menu-item">
                      <i class="fas fa-user"></i>
                      프로필
                    </a>
                    <a href="#" class="menu-item">
                      <i class="fas fa-cog"></i>
                      설정
                    </a>
                    <a href="#" class="menu-item" @click="logout">
                      <i class="fas fa-sign-out-alt"></i>
                      로그아웃
                    </a>
                  </div>
                </div>
              </div>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/premium">
                <i class="fas fa-crown me-1"></i>
                프리미엄
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <router-view/>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>AI Creator Tools</h3>
          <p>크리에이터를 위한 최고의 AI 도구 모음</p>
          <div class="social-links">
            <a href="#" target="_blank"><i class="fab fa-youtube"></i></a>
            <a href="#" target="_blank"><i class="fab fa-twitter"></i></a>
            <a href="#" target="_blank"><i class="fab fa-instagram"></i></a>
          </div>
        </div>

        <div class="footer-section">
          <h4>빠른 링크</h4>
          <ul>
            <li><router-link to="/">홈</router-link></li>
            <li><router-link to="/tools">AI 도구</router-link></li>
            <li><router-link to="/trends">트렌드</router-link></li>
            <li><router-link to="/youtube-analytics">유튜브 분석</router-link></li>
            <li><router-link to="/try-ai">AI 체험</router-link></li>
            <li><router-link to="/community">커뮤니티</router-link></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4>고객 지원</h4>
          <ul>
            <li><a href="#">자주 묻는 질문</a></li>
            <li><a href="#">이용 가이드</a></li>
            <li><a href="#">문의하기</a></li>
            <li><router-link to="/premium">프리미엄</router-link></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4>뉴스레터 구독</h4>
          <p>최신 AI 도구 소식을 받아보세요</p>
          <div class="newsletter">
            <input type="email" placeholder="이메일 주소">
            <button><i class="fas fa-paper-plane"></i></button>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2025 AI Creator Tools. All rights reserved.</p>
        <div class="footer-links">
          <a href="#">이용약관</a>
          <a href="#">개인정보처리방침</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isMenuOpen: false,
      isUserMenuOpen: false,
      isLoggedIn: false, // 임시 데이터
      user: {
        name: '김크리에이터',
        email: 'creator@example.com',
        avatar: 'https://example.com/avatar.jpg'
      }
    }
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen
    },
    toggleUserMenu() {
      this.isUserMenuOpen = !this.isUserMenuOpen
    },
    logout() {
      // TODO: 로그아웃 로직 구현
      this.isLoggedIn = false
      this.isUserMenuOpen = false
    }
  }
}
</script>

<style>
/* 전역 스타일 */
:root {
  --primary-color: #6366f1;
  --primary-dark: #4f46e5;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --bg-light: #f9fafb;
  --border-color: #e5e7eb;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.5;
  color: var(--text-primary);
  background: var(--bg-light);
}

/* 네비게이션 스타일 */
.navbar {
  background: white;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  font-size: 1.25rem;
  font-weight: 600;
}

.nav-brand a {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: var(--text-primary);
}

.nav-brand img {
  height: 32px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.nav-link:hover {
  color: var(--text-primary);
  background: var(--bg-light);
}

.nav-link.router-link-active {
  color: var(--primary-color);
}

.nav-link.premium {
  color: var(--primary-color);
}

.nav-auth {
  display: flex;
  align-items: center;
}

.btn-login {
  padding: 0.5rem 1.5rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-login:hover {
  background: var(--primary-dark);
}

.user-menu {
  position: relative;
}

.user-menu img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  width: 280px;
  overflow: hidden;
}

.user-info {
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.user-info img {
  width: 48px;
  height: 48px;
}

.user-info h4 {
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.user-info p {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.menu-items {
  padding: 0.5rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.menu-item:hover {
  background: var(--bg-light);
  color: var(--text-primary);
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1.25rem;
  cursor: pointer;
}

/* 푸터 스타일 */
.footer {
  background: white;
  padding: 4rem 2rem 2rem;
  margin-top: 4rem;
  box-shadow: 0 -1px 3px 0 rgb(0 0 0 / 0.1);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.footer-section h3 {
  color: var(--text-primary);
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.footer-section h4 {
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.footer-section p {
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-links a {
  color: var(--text-secondary);
  font-size: 1.25rem;
  transition: all 0.2s;
}

.social-links a:hover {
  color: var(--primary-color);
}

.footer-section ul {
  list-style: none;
}

.footer-section ul li {
  margin-bottom: 0.5rem;
}

.footer-section ul li a {
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s;
}

.footer-section ul li a:hover {
  color: var(--primary-color);
}

.newsletter {
  display: flex;
  gap: 0.5rem;
}

.newsletter input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.newsletter button {
  padding: 0.75rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.newsletter button:hover {
  background: var(--primary-dark);
}

.footer-bottom {
  max-width: 1200px;
  margin: 2rem auto 0;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.footer-links {
  display: flex;
  gap: 1.5rem;
}

.footer-links a {
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s;
}

.footer-links a:hover {
  color: var(--primary-color);
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
  }

  .nav-links {
    display: none;
    position: fixed;
    top: 72px;
    left: 0;
    right: 0;
    background: white;
    padding: 1rem;
    flex-direction: column;
    align-items: stretch;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  }

  .nav-links.active {
    display: flex;
  }

  .nav-link {
    padding: 1rem;
  }

  .menu-toggle {
    display: block;
  }

  .footer {
    padding: 2rem 1rem 1rem;
  }

  .footer-bottom {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
}
</style>
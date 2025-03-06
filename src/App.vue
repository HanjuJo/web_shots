<template>
  <div id="app">
    <MainNavigation />

    <main class="main-content">
      <router-view></router-view>
    </main>

    <footer class="footer">
      <div class="container">
        <div class="row">
          <div class="col-md-4 mb-4">
            <h3>AI Creator Hub</h3>
            <p>컨텐츠 제작의 미래를 함께 만들어갑니다</p>
          </div>
          <div class="col-md-2 mb-4">
            <h5>도구</h5>
            <ul class="list-unstyled">
              <li><router-link to="/tools">AI 도구</router-link></li>
              <li><router-link to="/tools/combinations">도구 조합</router-link></li>
              <li><router-link to="/tools/my-combinations">내 조합</router-link></li>
            </ul>
          </div>
          <div class="col-md-2 mb-4">
            <h5>콘텐츠</h5>
            <ul class="list-unstyled">
              <li><router-link to="/guides">가이드</router-link></li>
              <li><router-link to="/tutorials">튜토리얼</router-link></li>
              <li><router-link to="/community">커뮤니티</router-link></li>
            </ul>
          </div>
          <div class="col-md-2 mb-4">
            <h5>분석</h5>
            <ul class="list-unstyled">
              <li><router-link to="/youtube-analytics">유튜브 분석</router-link></li>
              <li><router-link to="/trends">AI 트렌드</router-link></li>
              <li><router-link to="/dashboard">대시보드</router-link></li>
            </ul>
          </div>
          <div class="col-md-2 mb-4">
            <h5>계정</h5>
            <ul class="list-unstyled">
              <li><router-link to="/profile">프로필</router-link></li>
              <li><router-link to="/auth">로그인</router-link></li>
              <li><router-link to="/premium">프리미엄</router-link></li>
            </ul>
          </div>
        </div>
      </div>
      <div class="footer-bottom py-3 mt-4 border-top">
        <div class="container text-center">
          <p class="mb-0">&copy; 2025 AI Creator Hub. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import MainNavigation from '@/components/MainNavigation.vue'

export default {
  name: 'App',
  components: {
    MainNavigation
  }
}
</script>

<style>
:root {
  --primary-color: #4a90e2;
  --secondary-color: #50e3c2;
  --text-color: #2c3e50;
  --background-color: #f8f9fa;
  --border-color: #e9ecef;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Noto Sans KR', sans-serif;
  color: var(--text-color);
  background-color: var(--background-color);
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
}

.footer {
  background: white;
  padding: 3rem 0 0;
  margin-top: auto;
  box-shadow: 0 -2px 4px rgba(0,0,0,0.05);
}

.footer h3, .footer h5 {
  color: var(--text-color);
  margin-bottom: 1.2rem;
}

.footer a {
  display: block;
  color: #666;
  text-decoration: none;
  margin-bottom: 0.75rem;
  transition: color 0.3s ease;
}

.footer a:hover {
  color: var(--primary-color);
  text-decoration: none;
}

.footer-bottom {
  background-color: white;
}

.footer-bottom p {
  color: #666;
}

/* Bootstrap 기반 반응형 스타일 */
.container {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

@media (min-width: 576px) {
  .container {
    max-width: 540px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 720px;
  }
}

@media (min-width: 992px) {
  .container {
    max-width: 960px;
  }
}

@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
  }
}

.list-unstyled {
  list-style: none;
  padding-left: 0;
}
</style>
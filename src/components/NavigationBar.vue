<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/">
        <img src="@/assets/logo.png" alt="Creator Tool" height="30">
      </router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/tools">도구</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/youtube-analyzer" class="nav-link" active-class="active">
              <i class="fas fa-video me-1"></i> YouTube 분석
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/ai-trends" class="nav-link" active-class="active">
              <i class="fas fa-robot me-1"></i> AI 트렌드
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/community">커뮤니티</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/tutorials">튜토리얼</router-link>
          </li>
        </ul>
        
        <div class="d-flex">
          <router-link class="btn btn-outline-primary me-2" to="/login">로그인</router-link>
          <router-link class="btn btn-primary" to="/register">회원가입</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavigationBar'
}
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>

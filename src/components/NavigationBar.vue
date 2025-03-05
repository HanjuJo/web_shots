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
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="toolsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="fas fa-tools me-1"></i> 도구
            </a>
            <ul class="dropdown-menu" aria-labelledby="toolsDropdown">
              <li><router-link class="dropdown-item" to="/tools">모든 도구</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><h6 class="dropdown-header">도구 조합</h6></li>
              <li><router-link class="dropdown-item" to="/tools/combinations">도구 조합 모음</router-link></li>
              <li><router-link class="dropdown-item" to="/tools/my-combinations">내 도구 조합</router-link></li>
              <li><router-link class="dropdown-item" to="/tools/combinations/create">새 도구 조합 만들기</router-link></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="guidesDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="fas fa-book me-1"></i> 가이드
            </a>
            <ul class="dropdown-menu" aria-labelledby="guidesDropdown">
              <li><router-link class="dropdown-item" to="/guides">모든 가이드</router-link></li>
              <li><router-link class="dropdown-item" to="/tutorials">튜토리얼</router-link></li>
            </ul>
          </li>
          <li class="nav-item">
            <router-link to="/youtube-analytics" class="nav-link" active-class="active">
              <i class="fas fa-video me-1"></i> YouTube 분석
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/trends" class="nav-link" active-class="active">
              <i class="fas fa-chart-line me-1"></i> AI 트렌드
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/community">
              <i class="fas fa-users me-1"></i> 커뮤니티
            </router-link>
          </li>
        </ul>
        
        <div class="d-flex">
          <template v-if="isAuthenticated">
            <div class="dropdown">
              <button class="btn btn-outline-primary dropdown-toggle" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fas fa-user-circle me-1"></i> 내 계정
              </button>
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                <li><router-link class="dropdown-item" to="/profile">프로필</router-link></li>
                <li><router-link class="dropdown-item" to="/dashboard">대시보드</router-link></li>
                <li><router-link class="dropdown-item" to="/tools/my-combinations">내 도구 조합</router-link></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click.prevent="logout">로그아웃</a></li>
              </ul>
            </div>
          </template>
          <template v-else>
            <router-link class="btn btn-outline-primary me-2" to="/auth">로그인</router-link>
            <router-link class="btn btn-primary" to="/premium">프리미엄</router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'NavigationBar',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const isAuthenticated = computed(() => store.state.auth.token !== null)
    const currentUser = computed(() => store.state.auth.user)
    
    const logout = () => {
      store.dispatch('auth/logout')
      router.push('/')
    }
    
    return {
      isAuthenticated,
      currentUser,
      logout
    }
  }
}
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dropdown-item {
  padding: 0.5rem 1rem;
}

.dropdown-header {
  padding: 0.5rem 1rem;
  font-weight: 600;
}

.navbar-nav .nav-link {
  padding: 0.5rem 1rem;
}

.dropdown-menu-end {
  right: 0;
  left: auto;
}
</style>

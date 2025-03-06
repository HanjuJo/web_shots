<template>
  <nav class="navigation">
    <div class="nav-brand">
      <router-link to="/" class="brand-link">
        <i class="fas fa-robot"></i>
        <span>AI Creator Hub</span>
      </router-link>
    </div>

    <div class="nav-menu">
      <router-link to="/tools" class="nav-item">
        <i class="fas fa-tools"></i>
        <span>도구</span>
      </router-link>

      <div class="nav-dropdown" @mouseenter="showToolsMenu = true" @mouseleave="showToolsMenu = false">
        <router-link to="/tools/combinations" class="nav-item">
          <i class="fas fa-layer-group"></i>
          <span>도구 조합</span>
          <i class="fas fa-chevron-down"></i>
        </router-link>
        <div class="dropdown-menu" v-show="showToolsMenu">
          <router-link to="/tools/combinations" class="dropdown-item">
            <i class="fas fa-list"></i>
            <span>모든 도구 조합</span>
          </router-link>
          <router-link to="/tools/my-combinations" class="dropdown-item" v-if="isAuthenticated">
            <i class="fas fa-star"></i>
            <span>내 도구 조합</span>
          </router-link>
          <router-link to="/tools/combinations/create" class="dropdown-item" v-if="isAuthenticated">
            <i class="fas fa-plus"></i>
            <span>새 도구 조합 만들기</span>
          </router-link>
        </div>
      </div>

      <router-link to="/guides" class="nav-item">
        <i class="fas fa-book"></i>
        <span>가이드</span>
      </router-link>

      <router-link to="/community" class="nav-item">
        <i class="fas fa-users"></i>
        <span>커뮤니티</span>
      </router-link>

      <router-link to="/trends" class="nav-item">
        <i class="fas fa-chart-line"></i>
        <span>트렌드</span>
      </router-link>
    </div>

    <div class="nav-auth">
      <template v-if="isAuthenticated">
        <div class="nav-dropdown" @mouseenter="showUserMenu = true" @mouseleave="showUserMenu = false">
          <button class="nav-item">
            <img :src="userAvatar" alt="User avatar" class="user-avatar" v-if="userAvatar">
            <i class="fas fa-user-circle" v-else></i>
            <span>{{ userName }}</span>
            <i class="fas fa-chevron-down"></i>
          </button>
          <div class="dropdown-menu" v-show="showUserMenu">
            <router-link to="/dashboard" class="dropdown-item">
              <i class="fas fa-tachometer-alt"></i>
              <span>대시보드</span>
            </router-link>
            <router-link to="/profile" class="dropdown-item">
              <i class="fas fa-user"></i>
              <span>프로필</span>
            </router-link>
            <router-link to="/settings" class="dropdown-item">
              <i class="fas fa-cog"></i>
              <span>설정</span>
            </router-link>
            <button @click="logout" class="dropdown-item">
              <i class="fas fa-sign-out-alt"></i>
              <span>로그아웃</span>
            </button>
          </div>
        </div>
      </template>
      <template v-else>
        <router-link to="/auth" class="nav-item">
          <i class="fas fa-sign-in-alt"></i>
          <span>로그인</span>
        </router-link>
      </template>
    </div>
  </nav>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'MainNavigation',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const showToolsMenu = ref(false)
    const showUserMenu = ref(false)

    const isAuthenticated = computed(() => store.state.auth.isAuthenticated)
    const userName = computed(() => store.state.auth.user?.name || '사용자')
    const userAvatar = computed(() => store.state.auth.user?.avatar)

    const logout = async () => {
      await store.dispatch('auth/logout')
      router.push('/auth')
    }

    return {
      showToolsMenu,
      showUserMenu,
      isAuthenticated,
      userName,
      userAvatar,
      logout
    }
  }
}
</script>

<style scoped>
.navigation {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 2rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.nav-brand {
  display: flex;
  align-items: center;
}

.brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #333;
  font-size: 1.2rem;
  font-weight: bold;
}

.brand-link i {
  margin-right: 0.5rem;
  color: #2196F3;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  color: #666;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
  background: none;
  font-size: 1rem;
}

.nav-item:hover {
  background: #f5f5f5;
  color: #2196F3;
}

.nav-item i {
  margin-right: 0.5rem;
}

.nav-item .fa-chevron-down {
  margin-left: 0.5rem;
  font-size: 0.8rem;
}

.nav-dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  z-index: 1000;
  margin-top: 0.5rem;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #666;
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-size: 1rem;
}

.dropdown-item:hover {
  background: #f5f5f5;
  color: #2196F3;
}

.dropdown-item i {
  margin-right: 0.75rem;
  width: 1rem;
  text-align: center;
}

.user-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 0.5rem;
}
</style>

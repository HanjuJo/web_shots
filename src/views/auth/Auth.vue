<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <h1>{{ isLogin ? '로그인' : '회원가입' }}</h1>
        <p>AI 크리에이터 플랫폼에 오신 것을 환영합니다</p>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div v-if="!isLogin" class="form-group">
          <label for="username">사용자 이름</label>
          <input 
            type="text" 
            id="username" 
            v-model="form.username"
            placeholder="사용자 이름을 입력하세요"
            required
          >
        </div>

        <div class="form-group">
          <label for="email">이메일</label>
          <input 
            type="email" 
            id="email" 
            v-model="form.email"
            placeholder="이메일을 입력하세요"
            required
          >
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input 
            type="password" 
            id="password" 
            v-model="form.password"
            placeholder="비밀번호를 입력하세요"
            required
          >
        </div>

        <div v-if="!isLogin" class="form-group">
          <label for="confirmPassword">비밀번호 확인</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="form.confirmPassword"
            placeholder="비밀번호를 다시 입력하세요"
            required
          >
        </div>

        <button type="submit" class="auth-button">
          {{ isLogin ? '로그인' : '회원가입' }}
        </button>

        <div class="social-auth">
          <p>또는</p>
          <button 
            type="button" 
            class="social-button google"
            @click="handleGoogleAuth"
          >
            <i class="fab fa-google"></i>
            Google로 계속하기
          </button>
        </div>

        <p class="auth-switch">
          {{ isLogin ? '계정이 없으신가요?' : '이미 계정이 있으신가요?' }}
          <a href="#" @click.prevent="toggleAuthMode">
            {{ isLogin ? '회원가입' : '로그인' }}
          </a>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthPage',
  data() {
    return {
      isLogin: true,
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    handleSubmit() {
      if (this.isLogin) {
        this.login()
      } else {
        this.register()
      }
    },
    async login() {
      try {
        // 로그인 로직 구현
        console.log('로그인 시도:', this.form.email)
      } catch (error) {
        console.error('로그인 실패:', error)
      }
    },
    async register() {
      try {
        // 회원가입 로직 구현
        console.log('회원가입 시도:', this.form)
      } catch (error) {
        console.error('회원가입 실패:', error)
      }
    },
    async handleGoogleAuth() {
      try {
        // Google 인증 로직 구현
        console.log('Google 인증 시도')
      } catch (error) {
        console.error('Google 인증 실패:', error)
      }
    },
    toggleAuthMode() {
      this.isLogin = !this.isLogin
      this.form = {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.auth-container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header h1 {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.auth-header p {
  color: #666;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #333;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.auth-button {
  padding: 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.auth-button:hover {
  background: var(--primary-dark-color);
}

.social-auth {
  text-align: center;
}

.social-auth p {
  color: #666;
  margin: 1rem 0;
  position: relative;
}

.social-auth p::before,
.social-auth p::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 45%;
  height: 1px;
  background: #ddd;
}

.social-auth p::before {
  left: 0;
}

.social-auth p::after {
  right: 0;
}

.social-button {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  color: #333;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.social-button:hover {
  background: #f5f5f5;
}

.social-button i {
  font-size: 1.25rem;
}

.social-button.google i {
  color: #DB4437;
}

.auth-switch {
  text-align: center;
  color: #666;
}

.auth-switch a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.auth-switch a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .auth-container {
    padding: 1.5rem;
  }

  .auth-header h1 {
    font-size: 1.75rem;
  }
}
</style>

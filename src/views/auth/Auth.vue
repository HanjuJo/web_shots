<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow-lg">
            <div class="card-body p-5">
              <div class="text-center mb-4">
                <h1 class="h3">{{ isLogin ? '로그인' : '회원가입' }}</h1>
                <p class="text-muted">AI 크리에이터 플랫폼에 오신 것을 환영합니다</p>
              </div>

              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>

              <form @submit.prevent="handleSubmit">
                <div v-if="!isLogin" class="mb-3">
                  <label for="username" class="form-label">사용자 이름</label>
                  <input 
                    type="text" 
                    id="username" 
                    v-model="form.username"
                    class="form-control"
                    :class="{ 'is-invalid': validationErrors.username }"
                    placeholder="사용자 이름을 입력하세요"
                    required
                  >
                  <div class="invalid-feedback" v-if="validationErrors.username">
                    {{ validationErrors.username }}
                  </div>
                </div>

                <div class="mb-3">
                  <label for="email" class="form-label">이메일</label>
                  <input 
                    type="email" 
                    id="email" 
                    v-model="form.email"
                    class="form-control"
                    :class="{ 'is-invalid': validationErrors.email }"
                    placeholder="이메일을 입력하세요"
                    required
                  >
                  <div class="invalid-feedback" v-if="validationErrors.email">
                    {{ validationErrors.email }}
                  </div>
                </div>

                <div class="mb-3">
                  <label for="password" class="form-label">비밀번호</label>
                  <input 
                    type="password" 
                    id="password" 
                    v-model="form.password"
                    class="form-control"
                    :class="{ 'is-invalid': validationErrors.password }"
                    placeholder="비밀번호를 입력하세요"
                    required
                  >
                  <div class="invalid-feedback" v-if="validationErrors.password">
                    {{ validationErrors.password }}
                  </div>
                </div>

                <div v-if="!isLogin" class="mb-3">
                  <label for="confirmPassword" class="form-label">비밀번호 확인</label>
                  <input 
                    type="password" 
                    id="confirmPassword" 
                    v-model="form.confirmPassword"
                    class="form-control"
                    :class="{ 'is-invalid': validationErrors.confirmPassword }"
                    placeholder="비밀번호를 다시 입력하세요"
                    required
                  >
                  <div class="invalid-feedback" v-if="validationErrors.confirmPassword">
                    {{ validationErrors.confirmPassword }}
                  </div>
                </div>

                <button 
                  type="submit" 
                  class="btn btn-primary w-100 mb-3"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  {{ isLogin ? '로그인' : '회원가입' }}
                </button>


                <div class="text-center mt-3">
                  <p class="mb-0">
                    {{ isLogin ? '계정이 없으신가요?' : '이미 계정이 있으신가요?' }}
                    <a href="#" @click.prevent="toggleAuthMode" class="text-primary ms-1">
                      {{ isLogin ? '회원가입' : '로그인' }}
                    </a>
                  </p>
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
import { mapState, mapActions } from 'vuex';

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
      },
      validationErrors: {}
    }
  },
  computed: {
    ...mapState('auth', ['error', 'loading'])
  },
  methods: {
    ...mapActions('auth', ['login', 'register']),

    validateForm() {
      this.validationErrors = {};
      
      if (!this.form.email) {
        this.validationErrors.email = '이메일을 입력해주세요';
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
        this.validationErrors.email = '올바른 이메일 형식이 아닙니다';
      }

      if (!this.form.password) {
        this.validationErrors.password = '비밀번호를 입력해주세요';
      } else if (this.form.password.length < 6) {
        this.validationErrors.password = '비밀번호는 최소 6자 이상이어야 합니다';
      }

      if (!this.isLogin) {
        if (!this.form.username) {
          this.validationErrors.username = '사용자 이름을 입력해주세요';
        }

        if (!this.form.confirmPassword) {
          this.validationErrors.confirmPassword = '비밀번호 확인을 입력해주세요';
        } else if (this.form.password !== this.form.confirmPassword) {
          this.validationErrors.confirmPassword = '비밀번호가 일치하지 않습니다';
        }
      }

      return Object.keys(this.validationErrors).length === 0;
    },

    async handleSubmit() {
      if (!this.validateForm()) return;

      try {
        if (this.isLogin) {
          await this.login({
            email: this.form.email,
            password: this.form.password
          });
        } else {
          await this.register({
            username: this.form.username,
            email: this.form.email,
            password: this.form.password
          });
        }
        this.$router.push('/dashboard');
      } catch (error) {
        // Error is handled by the store
      }
    },



    toggleAuthMode() {
      this.isLogin = !this.isLogin;
      this.form = {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      };
      this.validationErrors = {};
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.card {
  border: none;
  border-radius: 15px;
}

.card-body {
  padding: 2.5rem;
}

.form-control {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #dee2e6;
  font-size: 1rem;
}

.form-control:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
}

.btn-primary {
  padding: 0.75rem;
  font-weight: 500;
  border-radius: 8px;
}

.btn-outline-secondary {
  padding: 0.75rem;
  font-weight: 500;
  border-radius: 8px;
}

.text-primary {
  text-decoration: none;
}

.text-primary:hover {
  text-decoration: underline;
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

<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <header>
      <h1>크리에이터 툴</h1>
      <p>유튜브와 숏폼 크리에이터를 위한 올인원 솔루션</p>
      <nav :class="{ 'open': isNavOpen }">
        <button class="hamburger" @click="toggleNav">
          <i :class="isNavOpen ? 'fas fa-times' : 'fas fa-bars'"></i>
        </button>
        <div class="nav-links">
          <router-link to="/home" @click="closeNav">홈</router-link>
          <router-link to="/features" @click="closeNav">기능 소개</router-link>
          <router-link to="/pricing" @click="closeNav">가격</router-link>
          <button @click="toggleDarkMode" class="mode-toggle">
            {{ isDarkMode ? '라이트 모드' : '다크 모드' }}
          </button>
          <button @click="showLoginModal" class="login-btn">로그인</button>
        </div>
      </nav>
    </header>
    <main>
      <transition name="fade">
        <router-view></router-view>
      </transition>
      <button
        class="download-btn"
        @click="showAlert"
        @mouseover="buttonText = '클릭하세요!'"
        @mouseleave="buttonText = '다운로드 (Coming Soon)'"
      >
        {{ buttonText }} (클릭: {{ clickCount }})
      </button>
      <div class="easter-egg" v-if="showEasterEgg">
        <p>축하합니다! 숨겨진 메시지를 찾았어요: "Grok과 함께라면 다 돼요!"</p>
      </div>
      <div class="modal" v-if="showLogin">
        <div class="modal-content">
          <h3>로그인</h3>
          <input v-model="username" placeholder="사용자 이름" />
          <input v-model="password" type="password" placeholder="비밀번호" />
          <button @click="fakeLogin">로그인</button>
          <button @click="closeLoginModal">닫기</button>
          <p v-if="loginMessage">{{ loginMessage }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      buttonText: '다운로드 (Coming Soon)',
      clickCount: 0,
      isDarkMode: false,
      showEasterEgg: false,
      keySequence: '',
      showLogin: false,
      username: '',
      password: '',
      loginMessage: '',
      isNavOpen: false
    };
  },
  mounted() {
    window.addEventListener('keydown', this.handleKeydown);
  },
  beforeDestroy() {
    window.removeEventListener('keydown', this.handleKeydown);
  },
  methods: {
    showAlert() {
      this.clickCount++;
      alert('곧 출시됩니다! 기대해주세요!');
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
    },
    handleKeydown(event) {
      this.keySequence += event.key;
      if (this.keySequence.includes('grok')) {
        this.showEasterEgg = true;
        setTimeout(() => {
          this.showEasterEgg = false;
          this.keySequence = '';
        }, 3000);
      }
    },
    showLoginModal() {
      this.showLogin = true;
    },
    closeLoginModal() {
      this.showLogin = false;
      this.username = '';
      this.password = '';
      this.loginMessage = '';
    },
    fakeLogin() {
      if (this.username && this.password) {
        this.loginMessage = `안녕하세요, ${this.username}! (가짜 로그인 성공)`;
        setTimeout(() => this.closeLoginModal(), 2000);
      } else {
        this.loginMessage = '사용자 이름과 비밀번호를 입력해주세요!';
      }
    },
    toggleNav() {
      this.isNavOpen = !this.isNavOpen;
    },
    closeNav() {
      this.isNavOpen = false;
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  color: #333;
  transition: background-color 0.3s, color 0.3s;
}
header {
  background-color: #f8f9fa;
  padding: 30px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
h1 {
  margin: 0;
  font-size: 2.5em;
  color: #007bff;
}
p {
  margin: 10px 0;
  font-size: 1.2em;
  color: #666;
}
nav {
  background: linear-gradient(90deg, #007bff, #00d4ff);
  padding: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  position: relative;
}
.hamburger {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5em;
  cursor: pointer;
}
.nav-links {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
nav a, nav button {
  color: white;
  padding: 12px 24px;
  text-decoration: none;
  border-radius: 5px;
  transition: background 0.3s;
  margin: 5px;
}
nav a:hover, nav button:hover {
  background: rgba(255, 255, 255, 0.2);
}
nav a.router-link-active {
  background: #0056b3;
}
.download-btn {
  padding: 12px 30px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.2em;
  cursor: pointer;
  transition: background-color 0.3s;
  margin: 20px;
}
.download-btn:hover {
  background-color: #0056b3;
}
.mode-toggle, .login-btn {
  background: #fff;
  color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.dark-mode {
  background-color: #333;
  color: #fff;
}
.dark-mode header {
  background-color: #444;
}
.dark-mode h1 {
  color: #00d4ff;
}
.dark-mode p {
  color: #ccc;
}
.dark-mode nav {
  background: linear-gradient(90deg, #0056b3, #007bff);
}
.dark-mode .download-btn {
  background-color: #00d4ff;
  color: #333;
}
.dark-mode .download-btn:hover {
  background-color: #007bff;
}
.easter-egg {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #007bff;
  color: white;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}
.modal-content input {
  display: block;
  margin: 10px auto;
  padding: 10px;
  width: 80%;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.modal-content button {
  margin: 10px 5px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.modal-content button:hover {
  background-color: #0056b3;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
@media (max-width: 600px) {
  .hamburger {
    display: block;
    position: absolute;
    top: 15px;
    right: 15px;
  }
  .nav-links {
    display: none;
    flex-direction: column;
    width: 100%;
  }
  nav.open .nav-links {
    display: flex;
  }
  nav a, nav button {
    width: 100%;
    text-align: center;
    margin: 5px 0;
  }
}
</style>
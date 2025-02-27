<template>
  <div id="app">
    <header>
      <h1>크리에이터 툴</h1>
      <p>유튜브와 숏폼 크리에이터를 위한 올인원 솔루션</p>
      <nav>
        <router-link to="/home">홈</router-link>
        <router-link to="/features">기능 소개</router-link>
        <router-link to="/pricing">가격</router-link>
      </nav>
    </header>
    <main>
      <router-view></router-view>
      <button
        class="download-btn"
        @click="showAlert"
        @mouseover="buttonText = '클릭하세요!'"
        @mouseleave="buttonText = '다운로드 (Coming Soon)'"
      >
        {{ buttonText }} (클릭: {{ clickCount }})
      </button>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      buttonText: '다운로드 (Coming Soon)',
      clickCount: 0
    };
  },
  methods: {
    showAlert() {
      this.clickCount++;
      alert('곧 출시됩니다! 기대해주세요!');
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  color: #333;
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
  margin-top: 20px;
}
nav a {
  margin: 0 15px;
  padding: 8px 16px;
  text-decoration: none;
  color: #007bff;
  background-color: #e9ecef;
  border-radius: 5px;
}
nav a:hover {
  background-color: #dee2e6;
}
nav a.router-link-active {
  background-color: #007bff;
  color: white;
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
</style>
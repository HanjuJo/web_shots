<template>
  <div class="home">
    <h2>환영합니다!</h2>
    <p>크리에이터 툴로 유튜브 성장을 시작하세요.</p>
    <div class="email-form">
      <input v-model="email" type="email" placeholder="이메일 입력" />
      <button @click="submitEmail">구독 신청</button>
    </div>
    <p v-if="message">{{ message }}</p>
    <h3>구독자 목록</h3>
    <ul>
      <li v-for="(email, index) in emailList" :key="index">{{ email }}</li>
    </ul>
    <div class="analyze-form">
      <h3>채널 분석</h3>
      <input v-model="channelUrl" placeholder="유튜브 영상 URL" @keyup.enter="analyzeChannel" />
      <button @click="analyzeChannel">분석</button>
      <div v-if="analysis">
        <p>키워드: {{ analysis.keywords.join(', ') }}</p>
        <p>해시태그: {{ analysis.hashtags.join(', ') }}</p>
        <p>예상 조회수: {{ analysis.predicted_views }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      email: '',
      message: '',
      emailList: [],
      channelUrl: '',
      analysis: null
    };
  },
  mounted() {
    this.fetchEmails();
  },
  methods: {
    async submitEmail() {
      if (this.email) {
        try {
          const response = await axios.post('https://creatortool-backend-123-c965e7aaa680.herokuapp.com/api/emails', { email: this.email });
          this.message = response.data.message;
          this.email = '';
          this.fetchEmails();
        } catch (error) {
          this.message = '이메일 저장 실패!';
        }
      } else {
        this.message = '이메일을 입력해주세요!';
      }
    },
    async fetchEmails() {
      try {
        const response = await axios.get('https://creatortool-backend-123-c965e7aaa680.herokuapp.com/api/emails');
        this.emailList = response.data;
      } catch (error) {
        console.error('Error fetching emails:', error);
      }
    },
    async analyzeChannel() {
      if (this.channelUrl) {
        try {
          const response = await axios.post('https://creatortool-backend-123-c965e7aaa680.herokuapp.com/api/analyze', { url: this.channelUrl });
          this.analysis = response.data;
          this.channelUrl = '';
        } catch (error) {
          console.error('Error analyzing channel:', error);
        }
      }
    }
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
}
h2 {
  color: #007bff;
}
h3 {
  margin-top: 20px;
  color: #444;
}
p {
  font-size: 1.1em;
  color: #666;
}
.email-form {
  margin-top: 20px;
}
.email-form input {
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
}
.email-form button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.email-form button:hover {
  background-color: #0056b3;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  padding: 10px;
  background: #f0f8ff;
  margin: 5px 0;
  border-radius: 5px;
}

.analyze-form {
  margin-top: 20px;
}
.analyze-form input {
  padding: 10px;
  width: 70%;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.analyze-form button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.analyze-form button:hover {
  background-color: #0056b3;
}
.analyze-form p {
  margin: 5px 0;
}
</style>
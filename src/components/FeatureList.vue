<template>
  <section class="features">
    <h2>주요 기능</h2>
    <div class="feature-list">
      <div class="feature-card" v-for="(feature, index) in features" :key="index">
        <span>{{ feature }}</span>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FeatureList',
  data() {
    return {
      features: []
    };
  },
  mounted() {
    axios.get('http://localhost:5001/api/features')
      .then(response => {
        this.features = response.data;
        console.log('Features loaded:', this.features);  // 데이터 잘 왔는지 확인
      })
      .catch(error => {
        console.error('Error fetching features:', error);  // 에러 있으면 여기서 출력
      });
  }
}
</script>

<style scoped>
.features {
  margin: 40px 0;
}
h2 {
  font-size: 1.8em;
  color: #444;
}
.feature-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}
.feature-card {
  background-color: #f0f8ff;
  padding: 20px;
  border-radius: 10px;
  width: 200px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}
.feature-card:hover {
  transform: scale(1.05);
}
</style>
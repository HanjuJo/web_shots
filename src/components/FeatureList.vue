<template>
  <section class="features">
    <h2>주요 기능</h2>
    <div class="feature-list">
      <div class="feature-card" v-for="(feature, index) in features" :key="index">
        <i :class="getIconClass(index)"></i>
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
      })
      .catch(error => {
        console.error('Error fetching features:', error);
      });
  },
  methods: {
    getIconClass(index) {
      const icons = [
        'fab fa-youtube',          // 유튜브 트렌드 분석 (브랜드 아이콘)
        'fas fa-video',            // AI 기반 영상 편집 (솔리드 아이콘)
        'fas fa-closed-captioning', // 자동 자막 생성 (솔리드 아이콘)
        'fas fa-image'             // 썸네일 자동 생성 (솔리드 아이콘)
      ];
      return icons[index];
    }
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
.feature-card i {
  display: block;
  font-size: 1.5em;
  margin-bottom: 10px;
  color: #007bff;
}
</style>
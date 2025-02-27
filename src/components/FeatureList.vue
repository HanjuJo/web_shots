<template>
  <section class="features">
    <h2>주요 기능</h2>
    <div class="feature-list">
      <div class="feature-card" v-for="(feature, index) in features" :key="index">
        <i :class="getIconClass(index)" :style="getIconStyle(index)"></i>
        <span>{{ feature }}</span>
      </div>
    </div>
  </section>
</template>

<script>

export default {
  name: 'FeatureList',
  data() {
    return {
      features: [
        "유튜브 트렌드 분석",
        "AI 기반 영상 편집",
        "자동 자막 생성",
        "썸네일 자동 생성"
      ]
    };
  },
  methods: {
    getIconClass(index) {
      const icons = [
        'fab fa-youtube',
        'fas fa-video',
        'fas fa-closed-captioning',
        'fas fa-image'
      ];
      return icons[index];
    },
    getIconStyle(index) {
      const colors = [
        '#ff0000',  // YouTube 빨강
        '#007bff',  // 기본 파랑
        '#007bff',
        '#007bff'
      ];
      return { color: colors[index] };
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
  animation: fadeIn 0.5s ease-in;
}
.feature-card:hover {
  transform: scale(1.05);
}
.feature-card i {
  display: block;
  font-size: 1.5em;
  margin-bottom: 10px;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
<template>
  <section class="features">
    <h2>주요 기능</h2>
    <ul>
      <li v-for="(feature, index) in features" :key="index">
        {{ feature }}
      </li>
    </ul>
  </section>
</template>

<script>
export default {
  name: 'FeatureList',  // 'Features' → 'FeatureList'
  data() {
    return {
      features: [
        '유튜브 트렌드 분석',
        'AI 기반 영상 편집',
        '자동 자막 생성',
        '썸네일 자동 생성'
      ]
    };
  }
}
</script>

<style scoped>
/* 기존 스타일 유지 */
.features {
  margin: 40px 0;
}
h2 {
  font-size: 1.8em;
  color: #444;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin: 15px 0;
  font-size: 1.1em;
  padding: 10px;
  background-color: #f0f8ff;
  border-radius: 5px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}
</style>
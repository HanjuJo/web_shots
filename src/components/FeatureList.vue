<template>
  <section class="features">
    <h2>주요 기능</h2>
    <div v-if="loading" class="spinner">
      <i class="fas fa-spinner fa-spin"></i> 로딩 중...
    </div>
    <div v-else class="feature-list">
      <div class="feature-card" v-for="(feature, index) in features" :key="index" @click="showModal(index)">
        <i :class="getIconClass(index)" :style="getIconStyle(index)"></i>
        <span>{{ feature }}</span>
      </div>
    </div>
    <div class="trends">
      <h3>최신 트렌드</h3>
      <div v-if="trendsLoading" class="spinner">
        <i class="fas fa-spinner fa-spin"></i> 트렌드 로딩 중...
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>제목</th>
            <th>조회수</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(trend, index) in trends" :key="index">
            <td>{{ trend.title }}</td>
            <td>{{ trend.views }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="modal" v-if="showModalFlag">
      <div class="modal-content">
        <h3>{{ selectedFeature }}</h3>
        <p>{{ getFeatureDescription(selectedIndex) }}</p>
        <button @click="closeModal">닫기</button>
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
      features: [],
      loading: true,
      showModalFlag: false,
      selectedFeature: '',
      selectedIndex: null,
      trends: [],
      trendsLoading: true
    };
  },
  mounted() {
    this.fetchFeatures();
    this.fetchTrends();
  },
  methods: {
    async fetchFeatures() {
      try {
        const response = await axios.get('https://creatortool-backend-123-c965e7aaa680.herokuapp.com/api/features');
        this.features = response.data;
        this.loading = false;
      } catch (error) {
        console.error('Error fetching features:', error);
        this.loading = false;
      }
    },
    async fetchTrends() {
      try {
        const response = await axios.get('https://creatortool-backend-123-c965e7aaa680.herokuapp.com/api/trends');
        this.trends = response.data;
        this.trendsLoading = false;
      } catch (error) {
        console.error('Error fetching trends:', error);
        this.trendsLoading = false;
      }
    },
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
        '#ff0000',
        '#007bff',
        '#007bff',
        '#007bff'
      ];
      return { color: colors[index] };
    },
    showModal(index) {
      this.selectedFeature = this.features[index];
      this.selectedIndex = index;
      this.showModalFlag = true;
    },
    closeModal() {
      this.showModalFlag = false;
    },
    getFeatureDescription(index) {
      const descriptions = [
        '최신 유튜브 트렌드를 분석해줍니다.',
        'AI로 영상을 빠르게 편집합니다.',
        '자동으로 자막을 생성해줍니다.',
        '썸네일을 자동으로 만들어줍니다.'
      ];
      return descriptions[index];
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
.spinner {
  text-align: center;
  font-size: 1.2em;
  color: #007bff;
}
.spinner i {
  font-size: 2em;
  margin-right: 10px;
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
  cursor: pointer;
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
.modal-content button {
  margin-top: 10px;
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
.trends {
  margin-top: 40px;
}
.trends h3 {
  color: #444;
}
table {
  width: 80%;
  margin: 20px auto;
  border-collapse: collapse;
  background: #f0f8ff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
th, td {
  padding: 10px;
  border: 1px solid #ccc;
}
th {
  background: #007bff;
  color: white;
}
</style>
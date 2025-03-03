&lt;template>
  &lt;div class="dashboard">
    &lt;div class="stats-grid">
      &lt;div class="stat-card">
        &lt;h3>총 구독자&lt;/h3>
        &lt;div class="stat-value">{{ formatNumber(subscribers) }}&lt;/div>
        &lt;div class="stat-change" :class="{ 'positive': subscriberChange > 0 }">
          &lt;i :class="subscriberChange > 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'">&lt;/i>
          {{ Math.abs(subscriberChange) }}%
        &lt;/div>
      &lt;/div>

      &lt;div class="stat-card">
        &lt;h3>총 조회수&lt;/h3>
        &lt;div class="stat-value">{{ formatNumber(views) }}&lt;/div>
        &lt;div class="stat-change" :class="{ 'positive': viewChange > 0 }">
          &lt;i :class="viewChange > 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'">&lt;/i>
          {{ Math.abs(viewChange) }}%
        &lt;/div>
      &lt;/div>

      &lt;div class="stat-card">
        &lt;h3>평균 시청 시간&lt;/h3>
        &lt;div class="stat-value">{{ watchTime }}&lt;/div>
        &lt;div class="stat-change" :class="{ 'positive': watchTimeChange > 0 }">
          &lt;i :class="watchTimeChange > 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'">&lt;/i>
          {{ Math.abs(watchTimeChange) }}%
        &lt;/div>
      &lt;/div>

      &lt;div class="stat-card">
        &lt;h3>수익&lt;/h3>
        &lt;div class="stat-value">₩{{ formatNumber(revenue) }}&lt;/div>
        &lt;div class="stat-change" :class="{ 'positive': revenueChange > 0 }">
          &lt;i :class="revenueChange > 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'">&lt;/i>
          {{ Math.abs(revenueChange) }}%
        &lt;/div>
      &lt;/div>
    &lt;/div>

    &lt;div class="charts-grid">
      &lt;div class="chart-card">
        &lt;h3>시청자 연령대&lt;/h3>
        &lt;div class="chart-placeholder">
          &lt;i class="fas fa-chart-pie">&lt;/i>
          &lt;p>차트 데이터 준비 중...&lt;/p>
        &lt;/div>
      &lt;/div>

      &lt;div class="chart-card">
        &lt;h3>인기 동영상&lt;/h3>
        &lt;div class="chart-placeholder">
          &lt;i class="fas fa-chart-bar">&lt;/i>
          &lt;p>차트 데이터 준비 중...&lt;/p>
        &lt;/div>
      &lt;/div>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script>
export default {
  name: 'DashboardView',
  data() {
    return {
      subscribers: 15420,
      subscriberChange: 5.2,
      views: 1250000,
      viewChange: 3.8,
      watchTime: '4:32',
      watchTimeChange: -1.5,
      revenue: 2850000,
      revenueChange: 7.2
    }
  },
  methods: {
    formatNumber(num) {
      return new Intl.NumberFormat('ko-KR').format(num)
    }
  }
}
&lt;/script>

&lt;style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

.stat-card h3 {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: #ef4444;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change i {
  font-size: 0.75rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.chart-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

.chart-card h3 {
  color: #1f2937;
  font-size: 1.125rem;
  margin-bottom: 1rem;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
}

.chart-placeholder i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.chart-placeholder p {
  font-size: 0.875rem;
}
&lt;/style>

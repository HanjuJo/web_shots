<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>크리에이터 대시보드</h1>
      <div class="period-selector">
        <button 
          v-for="period in periods" 
          :key="period.value"
          :class="['period-button', { active: selectedPeriod === period.value }]"
          @click="selectedPeriod = period.value"
        >
          {{ period.label }}
        </button>
      </div>
    </header>

    <div class="dashboard-grid">
      <!-- 주요 지표 카드 -->
      <div class="metric-cards">
        <div class="metric-card">
          <div class="metric-icon">
            <i class="fas fa-eye"></i>
          </div>
          <div class="metric-content">
            <h3>총 조회수</h3>
            <p class="metric-value">{{ formatNumber(metrics.totalViews) }}</p>
            <p class="metric-trend" :class="{ positive: metrics.viewsTrend > 0 }">
              <i :class="['fas', metrics.viewsTrend > 0 ? 'fa-arrow-up' : 'fa-arrow-down']"></i>
              {{ Math.abs(metrics.viewsTrend) }}%
            </p>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">
            <i class="fas fa-heart"></i>
          </div>
          <div class="metric-content">
            <h3>총 좋아요</h3>
            <p class="metric-value">{{ formatNumber(metrics.totalLikes) }}</p>
            <p class="metric-trend" :class="{ positive: metrics.likesTrend > 0 }">
              <i :class="['fas', metrics.likesTrend > 0 ? 'fa-arrow-up' : 'fa-arrow-down']"></i>
              {{ Math.abs(metrics.likesTrend) }}%
            </p>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="metric-content">
            <h3>팔로워</h3>
            <p class="metric-value">{{ formatNumber(metrics.followers) }}</p>
            <p class="metric-trend" :class="{ positive: metrics.followersTrend > 0 }">
              <i :class="['fas', metrics.followersTrend > 0 ? 'fa-arrow-up' : 'fa-arrow-down']"></i>
              {{ Math.abs(metrics.followersTrend) }}%
            </p>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">
            <i class="fas fa-comment-dots"></i>
          </div>
          <div class="metric-content">
            <h3>댓글</h3>
            <p class="metric-value">{{ formatNumber(metrics.totalComments) }}</p>
            <p class="metric-trend" :class="{ positive: metrics.commentsTrend > 0 }">
              <i :class="['fas', metrics.commentsTrend > 0 ? 'fa-arrow-up' : 'fa-arrow-down']"></i>
              {{ Math.abs(metrics.commentsTrend) }}%
            </p>
          </div>
        </div>
      </div>

      <!-- 차트 섹션 -->
      <div class="charts-section">
        <div class="chart-card views-chart">
          <h3>조회수 추이</h3>
          <div class="chart-container">
            <!-- 실제 차트 컴포넌트 구현 필요 -->
            <div class="placeholder-chart">
              <div v-for="(value, index) in viewsData" 
                   :key="index" 
                   class="chart-bar"
                   :style="{ height: `${value}%` }"
              ></div>
            </div>
          </div>
        </div>

        <div class="chart-card engagement-chart">
          <h3>참여도 분석</h3>
          <div class="chart-container">
            <!-- 실제 차트 컴포넌트 구현 필요 -->
            <div class="placeholder-pie-chart">
              <div class="pie-segment" style="--percentage: 45%; --color: var(--primary-color);">
                <span class="pie-label">좋아요</span>
              </div>
              <div class="pie-segment" style="--percentage: 30%; --color: var(--secondary-color);">
                <span class="pie-label">댓글</span>
              </div>
              <div class="pie-segment" style="--percentage: 25%; --color: var(--accent-color);">
                <span class="pie-label">공유</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 최근 활동 -->
      <div class="recent-activity">
        <h3>최근 활동</h3>
        <div class="activity-list">
          <div v-for="activity in recentActivities" 
               :key="activity.id" 
               class="activity-item"
          >
            <div class="activity-icon">
              <i :class="activity.icon"></i>
            </div>
            <div class="activity-content">
              <p class="activity-text">{{ activity.text }}</p>
              <p class="activity-time">{{ formatDate(activity.time) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 인기 콘텐츠 -->
      <div class="popular-content">
        <h3>인기 콘텐츠</h3>
        <div class="content-list">
          <div v-for="content in popularContent" 
               :key="content.id" 
               class="content-item"
          >
            <img :src="content.thumbnail" :alt="content.title">
            <div class="content-info">
              <h4>{{ content.title }}</h4>
              <p class="content-stats">
                <span><i class="fas fa-eye"></i> {{ formatNumber(content.views) }}</span>
                <span><i class="fas fa-heart"></i> {{ formatNumber(content.likes) }}</span>
                <span><i class="fas fa-comment"></i> {{ formatNumber(content.comments) }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardPage',
  data() {
    return {
      selectedPeriod: 'week',
      periods: [
        { value: 'day', label: '오늘' },
        { value: 'week', label: '이번 주' },
        { value: 'month', label: '이번 달' },
        { value: 'year', label: '올해' }
      ],
      metrics: {
        totalViews: 152890,
        viewsTrend: 12.5,
        totalLikes: 8456,
        likesTrend: 8.2,
        followers: 2150,
        followersTrend: 15.3,
        totalComments: 1234,
        commentsTrend: -2.1
      },
      viewsData: [30, 45, 60, 35, 50, 70, 55],
      recentActivities: [
        {
          id: 1,
          icon: 'fas fa-heart',
          text: '새로운 팔로워 50명이 추가되었습니다',
          time: new Date(2025, 2, 4, 15, 30)
        },
        {
          id: 2,
          icon: 'fas fa-comment',
          text: '\'AI 작업 자동화 가이드\'에 새로운 댓글이 달렸습니다',
          time: new Date(2025, 2, 4, 14, 20)
        },
        {
          id: 3,
          icon: 'fas fa-share',
          text: '\'AI 크리에이터 수익화 전략\'이 50회 공유되었습니다',
          time: new Date(2025, 2, 4, 13, 15)
        }
      ],
      popularContent: [
        {
          id: 1,
          title: 'AI 작업 자동화 가이드',
          thumbnail: require('@/assets/images/default-cover.svg'),
          views: 12500,
          likes: 890,
          comments: 145
        },
        {
          id: 2,
          title: 'AI 크리에이터 수익화 전략',
          thumbnail: require('@/assets/images/default-cover.svg'),
          views: 8900,
          likes: 670,
          comments: 98
        },
        {
          id: 3,
          title: 'AI 도구 비교 분석',
          thumbnail: require('@/assets/images/default-cover.svg'),
          views: 7600,
          likes: 520,
          comments: 76
        }
      ]
    }
  },
  methods: {
    formatNumber(num) {
      return new Intl.NumberFormat('ko-KR').format(num)
    },
    formatDate(date) {
      const now = new Date()
      const diff = now - date
      const minutes = Math.floor(diff / 1000 / 60)
      const hours = Math.floor(minutes / 60)
      const days = Math.floor(hours / 24)

      if (days > 0) return `${days}일 전`
      if (hours > 0) return `${hours}시간 전`
      if (minutes > 0) return `${minutes}분 전`
      return '방금 전'
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.period-selector {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.period-button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.period-button.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.dashboard-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(12, 1fr);
}

.metric-cards {
  grid-column: span 12;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.metric-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: var(--primary-light-color);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.metric-content h3 {
  color: #666;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.metric-trend {
  font-size: 0.875rem;
  color: #dc3545;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.metric-trend.positive {
  color: #28a745;
}

.charts-section {
  grid-column: span 12;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  margin-bottom: 1rem;
  color: #333;
}

.chart-container {
  height: 300px;
  position: relative;
}

.placeholder-chart {
  height: 100%;
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  padding: 1rem 0;
}

.chart-bar {
  flex: 1;
  background: var(--primary-color);
  border-radius: 4px 4px 0 0;
  transition: height 0.3s ease;
}

.placeholder-pie-chart {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto;
  border-radius: 50%;
  background: #f5f5f5;
}

.pie-segment {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  clip-path: polygon(50% 50%, 100% 0, 100% 100%);
  transform: rotate(calc(360deg * var(--percentage)));
  background: var(--color);
}

.pie-label {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.875rem;
}

.recent-activity {
  grid-column: span 6;
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.activity-list {
  margin-top: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--primary-light-color);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-text {
  margin-bottom: 0.25rem;
}

.activity-time {
  font-size: 0.875rem;
  color: #666;
}

.popular-content {
  grid-column: span 6;
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.content-list {
  margin-top: 1rem;
}

.content-item {
  display: flex;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.content-item:last-child {
  border-bottom: none;
}

.content-item img {
  width: 120px;
  height: 68px;
  object-fit: cover;
  border-radius: 8px;
}

.content-info {
  flex: 1;
}

.content-info h4 {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.content-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #666;
}

.content-stats span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

@media (max-width: 1200px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .recent-activity,
  .popular-content {
    grid-column: span 12;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }

  .metric-cards {
    grid-template-columns: 1fr;
  }

  .content-item img {
    width: 80px;
    height: 45px;
  }
}
</style>

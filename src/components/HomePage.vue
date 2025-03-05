<template>
  <div class="home">
    <section class="hero">
      <h1>AI 크리에이터 허브</h1>
      <p>AI 도구를 활용한 컨텐츠 제작의 모든 것</p>
    </section>

    <!-- 사용자 레벨별 가이드 -->
    <section class="level-guides">
      <h2>나에게 맞는 AI 도구 찾기</h2>
      <div class="guide-container">
        <div class="guide-card beginner">
          <h3>입문자를 위한 가이드</h3>
          <ul>
            <li>기초 AI 도구 소개</li>
            <li>단계별 학습 로드맵</li>
            <li>초보자 친화적 튜토리얼</li>
          </ul>
          <router-link to="/beginner-guide" class="guide-link">시작하기</router-link>
        </div>
        <div class="guide-card intermediate">
          <h3>중급자를 위한 가이드</h3>
          <ul>
            <li>고급 AI 도구 활용법</li>
            <li>워크플로우 최적화</li>
            <li>수익화 전략</li>
          </ul>
          <router-link to="/intermediate-guide" class="guide-link">더 알아보기</router-link>
        </div>
        <div class="guide-card advanced">
          <h3>전문가를 위한 가이드</h3>
          <ul>
            <li>AI 도구 커스터마이징</li>
            <li>자동화 워크플로우</li>
            <li>브랜드 최적화</li>
          </ul>
          <router-link to="/advanced-guide" class="guide-link">심화 학습</router-link>
        </div>
      </div>
    </section>

    <!-- 커뮤니티 섹션 -->
    <section class="community">
      <h2>크리에이터 커뮤니티</h2>
      <div class="community-features">
        <div class="feature">
          <h3>노하우 공유</h3>
          <p>성공한 크리에이터들의 실전 경험과 팁</p>
        </div>
        <div class="feature">
          <h3>실시간 토론</h3>
          <p>최신 AI 트렌드와 도구에 대한 토론</p>
        </div>
        <div class="feature">
          <h3>멘토링</h3>
          <p>경험 많은 크리에이터의 1:1 조언</p>
        </div>
      </div>
    </section>

    <!-- 트렌드 분석 -->
    <section class="trends">
      <h2>AI 도구 트렌드</h2>
      <div class="trend-container">
        <div class="trend-card">
          <img src="@/assets/trend-1.jpg" alt="AI 영상 편집">
          <h3>인기 AI 도구 TOP 10</h3>
        </div>
        <div class="trend-card">
          <img src="@/assets/trend-2.jpg" alt="AI 썸네일">
          <h3>이번 주 트렌딩 컨텐츠</h3>
        </div>
        <div class="trend-card">
          <img src="@/assets/trend-3.jpg" alt="AI 스크립트">
          <h3>새로운 AI 도구 리뷰</h3>
        </div>
      </div>
    </section>

    <!-- 광고 섹션 -->
    <section class="ad-section">
      <div class="ad-space">
        <!-- Google AdSense 광고 공간 -->
        <div class="adsense-placeholder">
          <p>스폰서 광고</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.hero {
  text-align: center;
  padding: 60px 0;
  background: linear-gradient(135deg, #6e8efb, #a777e3);
  color: white;
  border-radius: 15px;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 3em;
  margin-bottom: 20px;
}

.level-guides {
  margin: 40px 0;
}

.guide-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.guide-card {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.guide-card:hover {
  transform: translateY(-5px);
}

.guide-link {
  display: inline-block;
  padding: 10px 20px;
  background: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  margin-top: 15px;
}

.community-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.feature {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.trend-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.trend-card {
  position: relative;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.trend-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.trend-card h3 {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 15px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  margin: 0;
}

.ad-section {
  margin: 40px 0;
}

.adsense-placeholder {
  background: #f8f9fa;
  padding: 20px;
  text-align: center;
  border-radius: 10px;
}

@media (max-width: 768px) {
  .guide-container,
  .community-features,
  .trend-container {
    grid-template-columns: 1fr;
  }
}
</style>
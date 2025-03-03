<template>
  <div class="home">
    <h2>환영합니다!</h2>
    <p>크리에이터 툴로 유튜브 성장을 시작하세요.</p>

    <!-- 기술적 안내 카드 -->
    <div class="tech-cards">
      <h3>기술적 지원</h3>
      <div class="card-container">
        <div class="card">
          <i class="fas fa-chart-line"></i>
          <h4>트렌드 분석</h4>
          <p>AI 기반으로 유튜브 인기 트렌드와 키워드를 분석하여 최적의 콘텐츠 전략을 제안합니다.</p>
        </div>
        <div class="card">
          <i class="fas fa-video"></i>
          <h4>AI 영상 편집</h4>
          <p>텍스트 입력만으로 자동 편집된 영상을 생성, 초보자도 쉽게 활용 가능합니다.</p>
        </div>
        <div class="card">
          <i class="fas fa-closed-captioning"></i>
          <h4>자동 자막</h4>
          <p>음성 텍스트를 인식해 실시간으로 자막을 생성하여 접근성을 높입니다.</p>
        </div>
        <div class="card">
          <i class="fas fa-image"></i>
          <h4>썸네일 생성</h4>
          <p>AI가 클릭률 높은 썸네일과 제목을 추천, 시각적 매력 증대.</p>
        </div>
      </div>
    </div>

    <!-- 홍보적 안내 카드 -->
    <div class="promo-cards">
      <h3>왜 크리에이터 툴을 선택해야 하나요?</h3>
      <div class="card-container">
        <div class="card">
          <i class="fas fa-clock"></i>
          <h4>시간 절약</h4>
          <p>복잡한 편집 과정을 자동화해 하루 몇 시간 이상 절약 가능!</p>
        </div>
        <div class="card">
          <i class="fas fa-chart-pie"></i>
          <h4>수익 증대</h4>
          <p>트렌드 분석과 AI 추천으로 조회수와 구독자 증가를 도모합니다.</p>
        </div>
        <div class="card">
          <i class="fas fa-users"></i>
          <h4>초보자 친화적</h4>
          <p>어떤 경험 수준에서도 쉽게 사용할 수 있는 직관적 인터페이스 제공.</p>
        </div>
        <div class="card">
          <i class="fas fa-globe"></i>
          <h4>글로벌 지원</h4>
          <p>국내외 크리에이터를 위한 다국어 지원과 확장성.</p>
        </div>
      </div>
    </div>

    <div class="hero-image">
      <img src="@/assets/hero-image.svg" alt="AI Creator Tool Interface">
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.home {
  padding: 20px;
  text-align: center;
}
h2 {
  color: #007bff;
  font-size: 2.5em;
}
p {
  font-size: 1.2em;
  color: #666;
}
.tech-cards, .promo-cards {
  margin-top: 40px;
}
h3 {
  font-size: 1.8em;
  color: #444;
  margin-bottom: 20px;
}
.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}
.card {
  background-color: #f0f8ff;
  padding: 20px;
  border-radius: 10px;
  width: 250px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}
.card:hover {
  transform: scale(1.05);
}
.card i {
  font-size: 2em;
  color: #007bff;
  margin-bottom: 10px;
}
.card h4 {
  margin: 0 0 10px;
  color: #333;
}
.card p {
  font-size: 1em;
  color: #666;
}
@media (max-width: 600px) {
  .card {
    width: 100%;
    max-width: 300px;
  }
}
</style>
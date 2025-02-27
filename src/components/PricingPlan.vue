<template>
  <section class="pricing">
    <h2>가격 플랜</h2>
    <div class="plans">
      <div class="plan">
        <h3>무료 체험</h3>
        <p>0원 / 7일</p>
        <ul>
          <li>기본 기능 제공</li>
          <li>제한된 AI 편집</li>
        </ul>
      </div>
      <div class="plan">
        <h3>Pro 플랜</h3>
        <p>9,900원 / 월</p>
        <ul>
          <li>모든 기능 무제한</li>
          <li>AI 썸네일 생성</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'PricingPlan'  // 'Pricing' → 'PricingPlan'
}
</script>

<style scoped>
/* 기존 스타일 유지 */
.pricing {
  margin: 40px 0;
}
h2 {
  font-size: 1.8em;
  color: #444;
}
.plans {
  display: flex;
  justify-content: center;
  gap: 20px;
}
.plan {
  background-color: #f0f8ff;
  padding: 20px;
  border-radius: 10px;
  width: 200px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.plan h3 {
  margin: 0;
  color: #007bff;
}
.plan p {
  font-size: 1.1em;
  color: #666;
}
.plan ul {
  list-style: none;
  padding: 0;
}
.plan li {
  margin: 10px 0;
}
</style>
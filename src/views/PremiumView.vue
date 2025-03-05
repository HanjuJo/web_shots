<template>
  <div class="premium">
    <div class="premium-header">
      <h1>프리미엄 멤버십</h1>
      <p>더 많은 기능과 혜택을 누려보세요</p>
    </div>

    <div class="pricing-toggle">
      <span :class="{ active: !isAnnual }">월간</span>
      <label class="switch">
        <input type="checkbox" v-model="isAnnual">
        <span class="slider"></span>
      </label>
      <span :class="{ active: isAnnual }">연간</span>
      <div class="savings" v-if="isAnnual">20% 할인</div>
    </div>

    <div class="pricing-plans">
      <div class="plan-card basic">
        <div class="plan-header">
          <h3>베이직</h3>
          <p>AI 도구를 처음 시작하는 분들을 위한 플랜</p>
          <div class="price">
            <span class="amount">무료</span>
          </div>
        </div>
        <ul class="features">
          <li>
            <i class="fas fa-check"></i>
            기본 AI 도구 사용
          </li>
          <li>
            <i class="fas fa-check"></i>
            커뮤니티 접근
          </li>
          <li>
            <i class="fas fa-check"></i>
            기본 분석 리포트
          </li>
        </ul>
        <button class="btn-secondary">현재 플랜</button>
      </div>

      <div class="plan-card pro">
        <div class="popular-badge">인기</div>
        <div class="plan-header">
          <h3>프로</h3>
          <p>전문 크리에이터를 위한 고급 기능</p>
          <div class="price">
            <span class="currency">₩</span>
            <span class="amount">{{ isAnnual ? '29,900' : '39,900' }}</span>
            <span class="period">/월</span>
          </div>
          <div class="price-note" v-if="isAnnual">연간 결제 시</div>
        </div>
        <ul class="features">
          <li>
            <i class="fas fa-check"></i>
            베이직의 모든 기능 포함
          </li>
          <li>
            <i class="fas fa-check"></i>
            고급 AI 도구 무제한 사용
          </li>
          <li>
            <i class="fas fa-check"></i>
            우선순위 처리
          </li>
          <li>
            <i class="fas fa-check"></i>
            상세 분석 리포트
          </li>
          <li>
            <i class="fas fa-check"></i>
            이메일 지원
          </li>
        </ul>
        <button class="btn-primary">시작하기</button>
      </div>

      <div class="plan-card enterprise">
        <div class="plan-header">
          <h3>엔터프라이즈</h3>
          <p>대규모 팀과 기업을 위한 맞춤형 솔루션</p>
          <div class="price">
            <span class="amount">문의</span>
          </div>
        </div>
        <ul class="features">
          <li>
            <i class="fas fa-check"></i>
            프로의 모든 기능 포함
          </li>
          <li>
            <i class="fas fa-check"></i>
            맞춤형 AI 모델 학습
          </li>
          <li>
            <i class="fas fa-check"></i>
            API 액세스
          </li>
          <li>
            <i class="fas fa-check"></i>
            전담 매니저
          </li>
          <li>
            <i class="fas fa-check"></i>
            SLA 보장
          </li>
        </ul>
        <button class="btn-outline">문의하기</button>
      </div>
    </div>

    <div class="faq-section">
      <h2>자주 묻는 질문</h2>
      <div class="faq-grid">
        <div 
          v-for="(faq, index) in faqs" 
          :key="index"
          class="faq-item"
          :class="{ active: faq.isOpen }"
          @click="toggleFaq(index)"
        >
          <div class="faq-header">
            <h3>{{ faq.question }}</h3>
            <i class="fas" :class="faq.isOpen ? 'fa-minus' : 'fa-plus'"></i>
          </div>
          <div class="faq-content" v-show="faq.isOpen">
            <p>{{ faq.answer }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PremiumView',
  data() {
    return {
      isAnnual: false,
      faqs: [
        {
          question: '프리미엄 멤버십은 어떤 혜택이 있나요?',
          answer: '프리미엄 멤버십은 고급 AI 도구 무제한 사용, 우선순위 처리, 상세 분석 리포트 등 다양한 혜택을 제공합니다. 또한 전문 지원 팀의 도움을 받을 수 있습니다.',
          isOpen: false
        },
        {
          question: '멤버십은 언제든 해지할 수 있나요?',
          answer: '네, 멤버십은 언제든지 해지가 가능합니다. 해지 시 현재 결제 주기가 끝날 때까지 서비스를 이용하실 수 있습니다.',
          isOpen: false
        },
        {
          question: '결제는 어떤 방식으로 이루어지나요?',
          answer: '신용카드, 체크카드, 계좌이체 등 다양한 결제 수단을 지원합니다. 결제는 선택하신 주기(월간/연간)에 따라 자동으로 이루어집니다.',
          isOpen: false
        },
        {
          question: '환불 정책은 어떻게 되나요?',
          answer: '첫 결제 후 14일 이내에 해지하시면 전액 환불이 가능합니다. 그 이후에는 남은 기간에 대한 부분 환불은 불가능합니다.',
          isOpen: false
        }
      ]
    }
  },
  methods: {
    toggleFaq(index) {
      this.faqs[index].isOpen = !this.faqs[index].isOpen
    }
  }
}
</script>

<style scoped>
.premium {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.premium-header {
  text-align: center;
  margin-bottom: 3rem;
}

.premium-header h1 {
  font-size: 2.5rem;
  color: #1f2937;
  margin-bottom: 1rem;
}

.premium-header p {
  color: #6b7280;
  font-size: 1.1rem;
}

.pricing-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 3rem;
}

.pricing-toggle span {
  color: #6b7280;
  font-weight: 500;
}

.pricing-toggle span.active {
  color: #1f2937;
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e5e7eb;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #6366f1;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.savings {
  background: #dcfce7;
  color: #15803d;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.pricing-plans {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.plan-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  position: relative;
}

.plan-card.pro {
  border: 2px solid #6366f1;
  transform: scale(1.05);
}

.popular-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #fee2e2;
  color: #dc2626;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.plan-header {
  text-align: center;
  margin-bottom: 2rem;
}

.plan-header h3 {
  color: #1f2937;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.plan-header p {
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.price {
  font-size: 2.5rem;
  color: #1f2937;
  font-weight: 700;
}

.price .currency {
  font-size: 1.5rem;
  vertical-align: top;
  margin-right: 0.25rem;
}

.price .period {
  font-size: 1rem;
  color: #6b7280;
  font-weight: normal;
}

.price-note {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.features {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem;
}

.features li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  color: #4b5563;
}

.features li i {
  color: #6366f1;
  font-size: 0.875rem;
}

button {
  width: 100%;
  padding: 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #6366f1;
  color: white;
  border: none;
}

.btn-primary:hover {
  background: #4f46e5;
}

.btn-secondary {
  background: #e5e7eb;
  color: #4b5563;
  border: none;
}

.btn-outline {
  background: transparent;
  border: 2px solid #6366f1;
  color: #6366f1;
}

.btn-outline:hover {
  background: #6366f1;
  color: white;
}

.faq-section {
  margin-top: 4rem;
}

.faq-section h2 {
  text-align: center;
  color: #1f2937;
  font-size: 2rem;
  margin-bottom: 2rem;
}

.faq-grid {
  display: grid;
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  cursor: pointer;
}

.faq-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: #f9fafb;
}

.faq-header h3 {
  color: #1f2937;
  font-size: 1.1rem;
  margin: 0;
}

.faq-header i {
  color: #6b7280;
  transition: all 0.2s;
}

.faq-content {
  padding: 1.5rem;
  color: #6b7280;
  line-height: 1.6;
}

.faq-item.active .faq-header {
  background: #f3f4f6;
}

@media (max-width: 1024px) {
  .plan-card.pro {
    transform: none;
  }
}

@media (max-width: 768px) {
  .premium-header h1 {
    font-size: 2rem;
  }

  .pricing-plans {
    gap: 1rem;
  }

  .plan-card {
    padding: 1.5rem;
  }
}
</style>

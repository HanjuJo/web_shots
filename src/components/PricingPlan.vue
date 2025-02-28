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
        <button @click="subscribe('무료 체험')">구독하기</button>
      </div>
      <div class="plan">
        <h3>Pro 플랜</h3>
        <p>9,900원 / 월</p>
        <ul>
          <li>모든 기능 무제한</li>
          <li>AI 썸네일 생성</li>
        </ul>
        <button @click="subscribe('Pro 플랜')">구독하기</button>
      </div>
    </div>
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <h3>{{ selectedPlan }} 구독</h3>
        <p>가짜 결제 완료! {{ selectedPlan }}을 즐겨보세요!</p>
        <button @click="closeModal">확인</button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'PricingPlan',
  data() {
    return {
      showModal: false,
      selectedPlan: ''
    };
  },
  methods: {
    subscribe(plan) {
      this.selectedPlan = plan;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    }
  }
}
</script>

<style scoped>
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
.plan button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.plan button:hover {
  background-color: #0056b3;
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
</style>
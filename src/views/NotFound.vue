<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>페이지를 찾을 수 없습니다</h2>
      <p>요청하신 페이지가 존재하지 않거나 이동되었을 수 있습니다.</p>
      <router-link to="/" class="home-button">
        <i class="fas fa-home"></i>
        홈으로 돌아가기
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundPage'
}
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  text-align: center;
}

.not-found-content {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 6rem;
  color: var(--primary-color);
  margin: 0;
  line-height: 1;
}

h2 {
  font-size: 2rem;
  color: #333;
  margin: 1rem 0;
}

p {
  color: #666;
  margin-bottom: 2rem;
}

.home-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.home-button:hover {
  background: var(--primary-dark-color);
}

@media (max-width: 480px) {
  .not-found-content {
    padding: 2rem;
  }

  h1 {
    font-size: 4rem;
  }

  h2 {
    font-size: 1.5rem;
  }
}
</style>

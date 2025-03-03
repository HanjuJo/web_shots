<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero bg-primary text-white py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h1 class="display-4 mb-4">AI 크리에이터 도구</h1>
            <p class="lead mb-4">
              최신 AI 도구들을 활용하여 더 나은 콘텐츠를 제작하세요.
              유튜브 채널 분석, 트렌드 파악, 커뮤니티 참여까지 한 곳에서!
            </p>
            <router-link to="/tools" class="btn btn-light btn-lg me-3">
              AI 도구 살펴보기
            </router-link>
            <router-link to="/youtube-analytics" class="btn btn-outline-light btn-lg">
              채널 분석하기
            </router-link>
          </div>
          <div class="col-lg-6">
            <img src="@/assets/hero-image.png" alt="AI Creator Tool" class="img-fluid">
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features py-5">
      <div class="container">
        <h2 class="text-center mb-5">주요 기능</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="card h-100">
              <div class="card-body text-center">
                <i class="fas fa-tools fa-3x text-primary mb-3"></i>
                <h3 class="card-title">AI 도구</h3>
                <p class="card-text">
                  Midjourney, ChatGPT, Runway 등 다양한 AI 도구들을 
                  한눈에 비교하고 선택하세요.
                </p>
                <router-link to="/tools" class="btn btn-outline-primary mt-3">
                  더 알아보기
                </router-link>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100">
              <div class="card-body text-center">
                <i class="fas fa-chart-line fa-3x text-primary mb-3"></i>
                <h3 class="card-title">채널 분석</h3>
                <p class="card-text">
                  유튜브 채널을 분석하여 성장 전략을 제시하고
                  트렌드를 파악하세요.
                </p>
                <router-link to="/youtube-analytics" class="btn btn-outline-primary mt-3">
                  분석하기
                </router-link>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100">
              <div class="card-body text-center">
                <i class="fas fa-users fa-3x text-primary mb-3"></i>
                <h3 class="card-title">커뮤니티</h3>
                <p class="card-text">
                  다른 크리에이터들과 경험을 공유하고
                  함께 성장하세요.
                </p>
                <router-link to="/community" class="btn btn-outline-primary mt-3">
                  참여하기
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Tutorial Section -->
    <section class="tutorials bg-light py-5">
      <div class="container">
        <h2 class="text-center mb-5">인기 튜토리얼</h2>
        <div class="row g-4">
          <div class="col-md-4" v-for="tutorial in tutorials" :key="tutorial.id">
            <div class="card h-100">
              <img :src="tutorial.thumbnail" class="card-img-top" :alt="tutorial.title">
              <div class="card-body">
                <h5 class="card-title">{{ tutorial.title }}</h5>
                <p class="card-text">{{ tutorial.description }}</p>
                <router-link :to="'/tutorials/' + tutorial.id" class="btn btn-primary">
                  보러가기
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      tutorials: [
        {
          id: 1,
          title: 'Midjourney 마스터하기',
          description: 'Midjourney로 전문가급 이미지 생성하는 방법',
          thumbnail: require('@/assets/tool-1.jpg')
        },
        {
          id: 2,
          title: 'ChatGPT 프롬프트 최적화',
          description: '더 나은 결과를 위한 프롬프트 작성법',
          thumbnail: require('@/assets/tool-2.jpg')
        },
        {
          id: 3,
          title: 'Runway 영상 편집 기초',
          description: 'AI로 영상 편집 시작하기',
          thumbnail: require('@/assets/tool-3.jpg')
        }
      ]
    }
  }
}
</script>

<style scoped>
.hero {
  background: linear-gradient(45deg, #4a90e2, #63b3ed);
}

.features .card {
  transition: transform 0.2s;
}

.features .card:hover {
  transform: translateY(-5px);
}

.tutorials .card {
  transition: transform 0.2s;
}

.tutorials .card:hover {
  transform: translateY(-5px);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}
</style>

<template>
  <div class="home">
    <div class="background-pattern"></div>
    
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <h1>AI로 시작하는 새로운 창작</h1>
        <p>무료로 사용할 수 있는 최고의 AI 도구들을 만나보세요</p>
      </div>
    </section>

    <!-- AI Tools Section -->
    <section class="ai-tools">
      <div class="container">
        <h2 class="text-center mb-4">무료로 시작하는 AI 도구</h2>
        <p class="text-center text-muted mb-5">인기 있는 무료 AI 도구들을 바로 사용해보세요!</p>
        
        <div class="row g-4">
          <div v-for="tool in aiTools" :key="tool.id" class="col-md-4">
            <div class="card h-100">
              <div class="card-body position-relative">
                <div class="tool-icon">
                  <i :class="tool.icon"></i>
                </div>
                <div class="decorative-circle"></div>
                <div class="decorative-dots"></div>
                <h5 class="card-title">{{ tool.title }}</h5>
                <p class="card-text">{{ tool.description }}</p>
                <a :href="tool.url" target="_blank" class="btn btn-primary stretched-link">
                  도구 사용하기
                  <i class="fas fa-arrow-right ms-2"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 더보기 버튼 -->
        <div class="text-center mt-5">
          <router-link to="/tools" class="btn btn-outline-primary btn-lg px-5">
            더 많은 AI 도구 보기
            <i class="fas fa-arrow-right ms-2"></i>
          </router-link>
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
      aiTools: [
        {
          id: 1,
          title: 'ChatGPT',
          description: '자연어 처리 AI로 대화하고 텍스트를 생성하세요',
          url: 'https://chat.openai.com',
          icon: 'fas fa-comments'
        },
        {
          id: 2,
          title: 'Midjourney',
          description: 'AI로 놀라운 이미지와 아트워크를 생성하세요',
          url: 'https://www.midjourney.com',
          icon: 'fas fa-paint-brush'
        },
        {
          id: 3,
          title: 'Claude',
          description: '지능형 AI 어시스턴트로 작업을 자동화하세요',
          url: 'https://claude.ai',
          icon: 'fas fa-robot'
        },
        {
          id: 4,
          title: 'Leonardo.ai',
          description: 'AI로 게임 아트와 캐릭터를 디자인하세요',
          url: 'https://leonardo.ai',
          icon: 'fas fa-gamepad'
        },
        {
          id: 5,
          title: 'Runway',
          description: 'AI로 비디오 편집과 특수효과를 만드세요',
          url: 'https://runway.ml',
          icon: 'fas fa-film'
        },
        {
          id: 6,
          title: 'Stable Diffusion',
          description: '오픈소스 AI로 이미지를 생성하고 편집하세요',
          url: 'https://stability.ai',
          icon: 'fas fa-image'
        },
        {
          id: 7,
          title: 'Gamma',
          description: 'AI로 전문적인 프레젠테이션을 만드세요',
          url: 'https://gamma.app',
          icon: 'fas fa-presentation'
        },
        {
          id: 8,
          title: 'Firefly',
          description: 'Adobe의 AI로 창의적인 작업을 하세요',
          url: 'https://firefly.adobe.com',
          icon: 'fas fa-wand-magic-sparkles'
        },
        {
          id: 9,
          title: 'Synthesia',
          description: 'AI로 전문적인 비디오를 제작하세요',
          url: 'https://www.synthesia.io',
          icon: 'fas fa-video'
        }
      ]
    }
  }
}
</script>

<style scoped>
.home {
  position: relative;
  min-height: 100vh;
  background-color: #f8f9fa;
  overflow: hidden;
}

.background-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.05;
  background-image: 
    radial-gradient(circle at 25px 25px, #000 2%, transparent 2%),
    radial-gradient(circle at 75px 75px, #000 2%, transparent 2%);
  background-size: 100px 100px;
  pointer-events: none;
}

.card {
  transition: all 0.3s ease;
  border: none;
  background: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 2rem;
  z-index: 1;
}

.tool-icon {
  position: absolute;
  top: -15px;
  right: -15px;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 20px;
  transform: rotate(45deg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-icon i {
  transform: rotate(-45deg);
  font-size: 1.8rem;
  color: white;
}

.decorative-circle {
  position: absolute;
  bottom: -50px;
  left: -50px;
  width: 150px;
  height: 150px;
  background: linear-gradient(45deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
  border-radius: 50%;
  z-index: -1;
}

.decorative-dots {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 60px;
  height: 60px;
  background-image: 
    radial-gradient(circle at 6px 6px, #6366f1 3px, transparent 3px);
  background-size: 15px 15px;
  opacity: 0.2;
  z-index: -1;
}

.card-title {
  margin-bottom: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.card-text {
  color: #6b7280;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

/* Hero Section */
.hero {
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 1rem;
  margin-bottom: 4rem;
  color: white;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.hero p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  line-height: 1.6;
  opacity: 0.9;
}

/* Sections */
section {
  margin-bottom: 4rem;
}

h2 {
  font-size: 2.25rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 1rem;
  color: #1f2937;
}

.section-desc {
  text-align: center;
  color: #6b7280;
  font-size: 1.125rem;
  margin-bottom: 3rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .home {
    padding: 1rem;
  }

  .hero {
    padding: 3rem 1rem;
  }

  .hero h1 {
    font-size: 2.5rem;
  }

  .hero p {
    font-size: 1.125rem;
  }

  h2 {
    font-size: 2rem;
  }
}
</style>

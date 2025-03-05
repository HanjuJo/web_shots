<template>
  <div class="beginner-guide">
    <h1>입문자를 위한 AI 도구 가이드</h1>
    
    <section class="getting-started">
      <h2>시작하기</h2>
      <div class="guide-steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3>기본 AI 도구 이해하기</h3>
          <ul>
            <li>ChatGPT - 스크립트 작성 도우미</li>
            <li>Midjourney - 썸네일 이미지 생성</li>
            <li>Descript - 기본적인 영상 편집</li>
          </ul>
        </div>
        
        <div class="step">
          <div class="step-number">2</div>
          <h3>첫 영상 만들기</h3>
          <ul>
            <li>주제 선정하기</li>
            <li>스크립트 작성하기</li>
            <li>간단한 편집 배우기</li>
          </ul>
        </div>
        
        <div class="step">
          <div class="step-number">3</div>
          <h3>채널 최적화</h3>
          <ul>
            <li>기본적인 SEO 이해하기</li>
            <li>썸네일 디자인 기초</li>
            <li>태그 설정하기</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="recommended-tools">
      <h2>추천 AI 도구</h2>
      <div class="tool-cards">
        <div class="tool-card" v-for="tool in recommendedTools" :key="tool.name">
          <img :src="tool.icon" :alt="tool.name">
          <h3>{{ tool.name }}</h3>
          <p>{{ tool.description }}</p>
          <a :href="tool.link" class="try-button" target="_blank">사용해보기</a>
        </div>
      </div>
    </section>

    <section class="tutorials">
      <h2>초보자 튜토리얼</h2>
      <div class="tutorial-list">
        <div class="tutorial-card" v-for="tutorial in tutorials" :key="tutorial.title">
          <img :src="tutorial.thumbnail" :alt="tutorial.title">
          <div class="tutorial-info">
            <h3>{{ tutorial.title }}</h3>
            <p>{{ tutorial.description }}</p>
            <span class="duration">{{ tutorial.duration }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'BeginnerGuide',
  data() {
    return {
      recommendedTools: [
        {
          name: 'ChatGPT',
          icon: require('@/assets/chatgpt-logo.png'),
          description: '스크립트 작성과 아이디어 발상을 도와주는 AI 어시스턴트',
          link: 'https://chat.openai.com'
        },
        {
          name: 'Midjourney',
          icon: require('@/assets/midjourney-logo.png'),
          description: '고품질 이미지를 생성하는 AI 도구',
          link: 'https://www.midjourney.com'
        }
      ],
      tutorials: [
        {
          title: 'ChatGPT로 스크립트 작성하기',
          thumbnail: require('@/assets/tutorial-1.jpg'),
          description: '효과적인 스크립트 작성을 위한 프롬프트 가이드',
          duration: '15분'
        },
        {
          title: '썸네일 제작 기초',
          thumbnail: require('@/assets/tutorial-2.jpg'),
          description: 'Midjourney를 활용한 매력적인 썸네일 만들기',
          duration: '20분'
        }
      ]
    }
  }
}
</script>

<style scoped>
.beginner-guide {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 40px;
}

.guide-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin: 40px 0;
}

.step {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.step-number {
  position: absolute;
  top: -15px;
  left: -15px;
  width: 40px;
  height: 40px;
  background: #007bff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2em;
  font-weight: bold;
}

.tool-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.tool-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.tool-card img {
  width: 80px;
  height: 80px;
  object-fit: contain;
  margin-bottom: 15px;
}

.try-button {
  display: inline-block;
  padding: 10px 20px;
  background: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  margin-top: 15px;
  transition: background 0.3s ease;
}

.try-button:hover {
  background: #0056b3;
}

.tutorial-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.tutorial-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.tutorial-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.tutorial-info {
  padding: 20px;
}

.duration {
  display: inline-block;
  padding: 5px 10px;
  background: #e9ecef;
  border-radius: 15px;
  font-size: 0.9em;
  color: #666;
}

@media (max-width: 768px) {
  .guide-steps,
  .tool-cards,
  .tutorial-list {
    grid-template-columns: 1fr;
  }
}
</style>

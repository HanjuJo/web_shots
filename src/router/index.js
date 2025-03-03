import { createRouter, createWebHistory } from 'vue-router'
import YoutubeAnalytics from '../views/YoutubeAnalytics.vue'
import HomeView from '../views/HomeView.vue'
import AiTrendsView from '../views/AiTrendsView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/tools',
    name: 'Tools',
    component: () => import('@/views/Tools.vue')
  },
  {
    path: '/trends',
    name: 'Trends',
    component: AiTrendsView
  },
  {
    path: '/youtube-analytics',
    name: 'YoutubeAnalytics',
    component: YoutubeAnalytics
  },
  {
    path: '/community',
    name: 'Community',
    component: () => import('@/views/Community.vue')
  },
  {
    path: '/try-ai',
    name: 'TryAI',
    component: () => import('@/views/TryAI.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

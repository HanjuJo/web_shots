import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'
import Tools from './views/Tools.vue'
import ToolDetail from './views/ToolDetail.vue'
import Trends from './views/Trends.vue'
import Guides from './views/Guides.vue'
import Community from './views/Community.vue'
import CommunityPost from './views/CommunityPost.vue'
import PremiumView from './views/PremiumView.vue'
import TryAiView from './views/TryAiView.vue'
import DashboardView from './views/DashboardView.vue'
import ChannelView from './views/ChannelView.vue'
import SettingsView from './views/SettingsView.vue'
import YoutubeAnalyzerView from './views/YoutubeAnalyzerView.vue'
import YoutubeAnalyticsView from './views/YoutubeAnalyticsView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/tools',
    name: 'tools',
    component: Tools
  },
  {
    path: '/tools/:id',
    name: 'tool-detail',
    component: ToolDetail
  },
  {
    path: '/trends',
    name: 'trends',
    component: Trends
  },
  {
    path: '/guides',
    name: 'guides',
    component: Guides
  },
  {
    path: '/community',
    name: 'community',
    component: Community
  },
  {
    path: '/community/post/:id',
    name: 'community-post',
    component: CommunityPost
  },
  {
    path: '/premium',
    name: 'premium',
    component: PremiumView
  },
  {
    path: '/try-ai',
    name: 'try-ai',
    component: TryAiView
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView
  },
  {
    path: '/channel',
    name: 'channel',
    component: ChannelView
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView
  },
  {
    path: '/youtube-analyzer',
    name: 'youtube-analyzer',
    component: YoutubeAnalyzerView
  },
  {
    path: '/youtube-analytics',
    name: 'youtube-analytics',
    component: YoutubeAnalyticsView
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
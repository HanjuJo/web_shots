import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/tools',
    name: 'Tools',
    component: () => import('@/views/tools/Tools.vue')
  },
  {
    path: '/tools/:id',
    name: 'ToolDetail',
    component: () => import('@/views/tools/ToolDetail.vue'),
    props: true
  },
  {
    path: '/tools/combinations',
    name: 'ToolCombinations',
    component: () => import('@/views/tools/ToolCombinations.vue')
  },
  {
    path: '/tools/my-combinations',
    name: 'MyToolCombinations',
    component: () => import('@/views/tools/MyToolCombinations.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tools/combinations/:id',
    name: 'ToolCombinationDetail',
    component: () => import('@/views/tools/ToolCombinationDetail.vue'),
    props: true
  },
  {
    path: '/tools/combinations/create',
    name: 'CreateToolCombination',
    component: () => import('@/views/tools/CreateToolCombination.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tools/combinations/edit/:id',
    name: 'EditToolCombination',
    component: () => import('@/views/tools/CreateToolCombination.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/guides',
    name: 'Guides',
    component: () => import('@/views/guides/Guides.vue')
  },
  {
    path: '/guides/:id',
    name: 'GuideDetail',
    component: () => import('@/views/guides/GuideDetail.vue'),
    props: true
  },
  {
    path: '/community',
    name: 'Community',
    component: () => import('@/views/community/Community.vue')
  },
  {
    path: '/community/post/:id',
    name: 'CommunityPost',
    component: () => import('@/views/community/CommunityPost.vue'),
    props: true
  },
  {
    path: '/community/create',
    name: 'CreatePost',
    component: () => import('@/views/community/CreatePost.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/profile/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('@/views/auth/Auth.vue'),
    meta: { guest: true }
  },
  {
    path: '/try-ai',
    name: 'TryAI',
    component: () => import('@/views/TryAiView.vue')
  },
  {
    path: '/youtube-analytics',
    name: 'YoutubeAnalytics',
    component: () => import('@/views/YoutubeAnalytics.vue')
  },
  {
    path: '/trends',
    name: 'Trends',
    component: () => import('@/views/AiTrendsView.vue')
  },
  {
    path: '/tutorials',
    name: 'Tutorials',
    component: () => import('@/views/Tutorials.vue')
  },
  {
    path: '/channel',
    name: 'Channel',
    component: () => import('@/views/ChannelView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/SettingsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/premium',
    name: 'Premium',
    component: () => import('@/views/PremiumView.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { x: 0, y: 0 }
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')

  // Auth required pages
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({
        path: '/auth',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  }

  // Guest only pages (login, signup, etc)
  else if (to.matched.some(record => record.meta.guest)) {
    if (isAuthenticated) {
      next('/')
    } else {
      next()
    }
  }

  else {
    next()
  }
})

export default router

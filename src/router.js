import Vue from 'vue';
import VueRouter from 'vue-router';
import HomePage from './components/HomePage.vue';
import FeatureList from './components/FeatureList.vue';
import PricingPlan from './components/PricingPlan.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/home', component: HomePage },
  { path: '/features', component: FeatureList },
  { path: '/pricing', component: PricingPlan },
  { path: '/', redirect: '/home' } // 기본 경로를 /home으로 리다이렉트
];

const router = new VueRouter({
  routes
});

export default router;
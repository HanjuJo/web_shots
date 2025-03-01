import Vue from 'vue';
import VueRouter from 'vue-router';
import HomePage from './components/HomePage.vue';
import FeatureList from './components/FeatureList.vue';
import PricingPlan from './components/PricingPlan.vue';
import VideoEditor from './components/VideoEditor.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/home', component: HomePage, meta: { transition: 'fade' } },
  { path: '/features', component: FeatureList, meta: { transition: 'fade' } },
  { path: '/pricing', component: PricingPlan, meta: { transition: 'fade' } },
  { path: '/', redirect: '/home' },
  { path: '/editor', component: VideoEditor }
];

const router = new VueRouter({
  routes
});

export default router;
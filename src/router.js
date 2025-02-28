import Vue from 'vue';
import VueRouter from 'vue-router';
import HomePage from './components/HomePage.vue';
import FeatureList from './components/FeatureList.vue';
import PricingPlan from './components/PricingPlan.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/home', component: HomePage, meta: { transition: 'fade' } },
  { path: '/features', component: FeatureList, meta: { transition: 'fade' } },
  { path: '/pricing', component: PricingPlan, meta: { transition: 'fade' } },
  { path: '/', redirect: '/home' }
];

const router = new VueRouter({
  routes
});

export default router;
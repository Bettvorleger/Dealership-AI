import { createRouter, createWebHistory } from 'vue-router'

import store from '@/store';

import HomeView from '@/views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import ProfileView from '@/views/ProfileView.vue'
import EditCar from '@/views/EditCar.vue'
import StatusView from '@/views/StatusView.vue'
import NotFound from '@/views/NotFound.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true },
  },
  {
    path: '/car/:id',
    name: 'editCar',
    component: EditCar,
    meta: { requiresAuth: true },
    props: true,
  },
  {
    path: '/status/:pCode?',
    name: 'status',
    component: StatusView,
    props: true,
  },
  {
    path:  '/:catchAll(.*)',
    name: '404',
    component: NotFound
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isAuthenticated) {
      next();
      return;
    }
    next({name: 'login'});
  } else {
    next();
  }
});

export default router

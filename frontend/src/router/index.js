// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

// Import views
import Dashboard from '../views/Dashboard.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import PregnancyTracker from '../views/PregnancyTracker.vue'
import ChildrenManager from '../views/ChildrenManager.vue'
import HealthRecords from '../views/HealthRecords.vue'
import Profile from '../views/Profile.vue'
import Chatbot from '../views/Chatbot.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true, title: 'Dashboard' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: 'Login' }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: 'Register' }
  },
  {
    path: '/pregnancy',
    name: 'Pregnancy',
    component: PregnancyTracker,
    meta: { requiresAuth: true, title: 'Pregnancy Tracker' }
  },
  {
    path: '/children',
    name: 'Children',
    component: ChildrenManager,
    meta: { requiresAuth: true, title: 'Children' }
  },
  {
    path: '/health',
    name: 'HealthRecords',
    component: HealthRecords,
    meta: { requiresAuth: true, title: 'Health Records' }
  },
  {
    path: '/chat',
    name: 'Chatbot',
    component: Chatbot,
    meta: { requiresAuth: true, title: 'Health Assistant' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true, title: 'Profile' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // Set page title
  document.title = to.meta.title ? `${to.meta.title} - Mamatoto` : 'Mamatoto'
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/login')
  } else if ((to.name === 'Login' || to.name === 'Register') && userStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router













































































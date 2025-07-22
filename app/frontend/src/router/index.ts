import { createRouter, createWebHistory } from 'vue-router'
import VotingView from '@/views/VotingView.vue'
import LoginView from '@/views/LoginView.vue'
import { useUserStore } from '@/stores/useUserStore'

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/vote', name: 'Vote', component: VotingView },
  { path: '/', redirect: '/vote' },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = userStore.token !== null
  if (to.name !== 'Login' && !isAuthenticated) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router

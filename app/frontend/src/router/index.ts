import { createRouter, createWebHistory } from 'vue-router'
import VotingView from '@/views/VotingView.vue'
import VotedNamesView from '@/views/VotedNamesView.vue'
import LoginView from '@/views/LoginView.vue'
import GamingView from '@/views/GamingView.vue'
import AccountView from '@/views/AccountView.vue'
import PreferencesView from '@/views/PreferencesView.vue'
import { useUserStore } from '@/stores/useUserStore'

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/vote', name: 'Vote', component: VotingView },
  { path: '/voted', name: 'VotedNames', component: VotedNamesView },
  { path: '/games', name: 'Gaming', component: GamingView },
  { path: '/account', name: 'Account', component: AccountView },
  { path: '/preferences', name: 'Preferences', component: PreferencesView },
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

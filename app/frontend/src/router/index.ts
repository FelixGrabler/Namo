import { createRouter, createWebHistory } from 'vue-router'
import VotingView from '@/views/VotingView.vue'
import VotedNamesView from '@/views/VotedNamesView.vue'
import LoginView from '@/views/LoginView.vue'
import GamingView from '@/views/GamingView.vue'
import HigherLowerGameView from '@/views/HigherLowerGameView.vue'
import WordleView from '@/views/WordleView.vue'
import AccountView from '@/views/AccountView.vue'
import PreferencesView from '@/views/PreferencesView.vue'
import NameSearchView from '@/views/NameSearchView.vue'
import CompareVotesView from '@/views/CompareVotesView.vue'
import { useUserStore } from '@/stores/useUserStore'

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/vote', name: 'Vote', component: VotingView },
  { path: '/voted', name: 'VotedNames', component: VotedNamesView },
  { path: '/games', name: 'Gaming', component: GamingView },
  { path: '/games/higher-lower', name: 'HigherLower', component: HigherLowerGameView },
  { path: '/games/wordle', name: 'Wordle', component: WordleView },
  { path: '/names', name: 'NameSearch', component: NameSearchView },
  { path: '/compare', name: 'CompareVotes', component: CompareVotesView },
  { path: '/account', name: 'Account', component: AccountView },
  { path: '/preferences', name: 'Preferences', component: PreferencesView },
  { path: '/', redirect: '/vote' },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()
  const publicRoutes = new Set(['Login', 'Vote', 'Account', 'NameSearch', 'Gaming', 'HigherLower', 'Wordle', 'Preferences'])

  if (!publicRoutes.has(String(to.name)) && !userStore.isAuthenticated) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref<string | null>(localStorage.getItem('username'))

  const isAuthenticated = computed(() => !!token.value)

  const setToken = (newToken: string, user: string) => {
    token.value = newToken
    username.value = user
    localStorage.setItem('token', newToken)
    localStorage.setItem('username', user)
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
  }

  const logout = () => {
    token.value = ''
    username.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    delete axios.defaults.headers.common['Authorization']
  }

  // If already logged in, set axios header
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  return { token, username, isAuthenticated, setToken, logout }
})

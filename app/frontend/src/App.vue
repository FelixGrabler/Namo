<template>
  <div id="app">
    <header v-if="showHeader" class="app-header">
      <div class="header-content">
        <h1 class="app-title">Namo</h1>
        <nav class="nav-menu">
          <router-link
            v-if="isAuthenticated"
            to="/vote"
            class="nav-link"
            :class="{ active: $route.name === 'Vote' }"
          >
            Vote
          </router-link>
          <router-link
            v-if="isAuthenticated"
            to="/voted"
            class="nav-link"
            :class="{ active: $route.name === 'VotedNames' }"
          >
            Auswertung
          </router-link>
          <button
            v-if="isAuthenticated"
            @click="logout"
            class="nav-link logout-btn"
          >
            Logout
          </button>
        </nav>
      </div>
    </header>

    <main class="main-content" :class="mainContentClasses">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isAuthenticated = computed(() => userStore.token !== null)
const showHeader = computed(() => route.name !== 'Login')
const mainContentClasses = computed(() => ({
  'no-padding': route.name === 'Vote'
}))

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  font-family: Arial, sans-serif;
}

.app-header {
  background: #f8f9fa;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.nav-menu {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  color: #007bff;
  text-decoration: none;
  padding: 0.5rem;
}

.nav-link:hover {
  text-decoration: underline;
}

.nav-link.active {
  font-weight: bold;
}

.logout-btn {
  background: none;
  border: 1px solid #007bff;
  color: #007bff;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
}

.logout-btn:hover {
  background: #007bff;
  color: white;
}

.main-content {
  padding: 2rem;
}

.main-content.no-padding {
  padding: 0;
}
</style>

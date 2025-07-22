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

    <main class="main-content">
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

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.nav-menu {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.nav-link.active {
  background: rgba(255, 255, 255, 0.2);
}

.logout-btn {
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  font-size: 1rem;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.main-content {
  flex: 1;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: calc(100vh - 80px);
  padding: 0;
}
</style>

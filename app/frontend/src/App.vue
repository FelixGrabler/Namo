<template>
  <div id="app">
    <!-- Desktop Navigation -->
    <DesktopNavigation v-if="isAuthenticated && showNavigation" />

    <!-- New Top Bar -->
    <TopBar v-if="isAuthenticated && showNavigation" :is-mobile="isMobile" />

    <main class="main-content" :class="mainContentClasses">
      <router-view />
    </main>

    <!-- Mobile Navigation -->
    <MobileNavigation v-if="isAuthenticated && showNavigation && isMobile" />
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import MobileNavigation from '@/components/MobileNavigation.vue'
import DesktopNavigation from '@/components/DesktopNavigation.vue'
import TopBar from '@/components/TopBar.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isMobile = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

const isAuthenticated = computed(() => userStore.token !== null)
const showNavigation = computed(() => route.name !== 'Login')
const mainContentClasses = computed(() => ({
  'no-padding': route.name === 'Vote',
  'mobile-padding': isMobile.value && isAuthenticated.value,
  'with-topbar': isAuthenticated.value && showNavigation.value
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

.main-content {
  padding: 2rem;
}

.main-content.no-padding {
  padding: 0;
}

.main-content.mobile-padding {
  padding-bottom: 5rem; /* Space for mobile navigation */
}

.main-content.with-topbar {
  padding-top: 1rem; /* Space for top bar */
}

/* Mobile styles */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }

  .main-content.no-padding {
    padding: 0;
  }

  .main-content.with-topbar {
    padding-top: 0.5rem;
  }
}
</style>

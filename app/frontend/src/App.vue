<template>
  <div id="app">
    <DesktopNavigation v-if="showNavigation" />

    <TopBar v-if="showNavigation" :is-mobile="isMobile" />

    <main class="main-content" :class="mainContentClasses">
      <router-view />
    </main>

    <MobileNavigation v-if="showNavigation && isMobile" />
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import MobileNavigation from '@/components/MobileNavigation.vue'
import DesktopNavigation from '@/components/DesktopNavigation.vue'
import TopBar from '@/components/TopBar.vue'

const route = useRoute()
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

const showNavigation = computed(() => route.name !== 'Login')
const mainContentClasses = computed(() => ({
  'no-padding': route.name === 'Vote',
  'mobile-padding': isMobile.value && showNavigation.value,
  'with-topbar': showNavigation.value
}))
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
  padding-bottom: 5rem;
}

.main-content.with-topbar {
  padding-top: 1rem;
}

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

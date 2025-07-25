<template>
  <header class="top-bar" :class="{ mobile: isMobile }">
    <div class="top-bar-content">
      <!-- Left side (mobile) / Right side (desktop) -->
      <div class="flag-gender-section" :class="{ 'mobile-left': isMobile, 'desktop-right': !isMobile }">
        <!-- Austrian Flag -->
        <button @click="goToPreferences" class="flag-button">
          <div class="austrian-flag">
            <div class="flag-stripe red"></div>
            <div class="flag-stripe white"></div>
            <div class="flag-stripe red"></div>
          </div>
        </button>

        <!-- Gender Icons -->
        <div class="gender-icons" @click="goToPreferences">
          <svg
            v-if="preferencesStore.selectedGenders.includes('male')"
            class="gender-icon male"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M9,9C10.29,9 11.5,9.41 12.47,10.11L17.58,5H13V3H21V11H19V6.41L13.89,11.5C14.59,12.5 15,13.7 15,15A6,6 0 0,1 9,21A6,6 0 0,1 3,15A6,6 0 0,1 9,9M9,11A4,4 0 0,0 5,15A4,4 0 0,0 9,19A4,4 0 0,0 13,15A4,4 0 0,0 9,11Z"/>
          </svg>
          <svg
            v-if="preferencesStore.selectedGenders.includes('female')"
            class="gender-icon female"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M12,4A6,6 0 0,1 18,10C18,12.97 15.84,15.44 13,15.92V18H15V20H13V22H11V20H9V18H11V15.92C8.16,15.44 6,12.97 6,10A6,6 0 0,1 12,4M12,6A4,4 0 0,0 8,10A4,4 0 0,0 12,14A4,4 0 0,0 16,10A4,4 0 0,0 12,6Z"/>
          </svg>
        </div>
      </div>

      <!-- Center (desktop only) - App Title -->
      <div v-if="!isMobile" class="app-title-section">
        <h1 class="app-title">Namo</h1>
      </div>

      <!-- Right side (mobile) / Left side (desktop) -->
      <div class="preferences-section" :class="{ 'mobile-right': isMobile, 'desktop-left': !isMobile }">
        <button @click="goToPreferences" class="preferences-button">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { usePreferencesStore } from '@/stores/usePreferencesStore'
import { useRouter } from 'vue-router'

const props = defineProps({
  isMobile: {
    type: Boolean,
    default: false
  }
})

const preferencesStore = usePreferencesStore()
const router = useRouter()

const goToPreferences = () => {
  router.push('/preferences')
}
</script>

<style scoped>
.top-bar {
  background: linear-gradient(135deg, #6a1b9a 0%, #8e24aa 100%);
  color: white;
  padding: 0.75rem 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: relative;
  z-index: 100;
}

.top-bar-content {
  display: flex;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  height: 40px;
}

/* Mobile Layout */
.top-bar.mobile .top-bar-content {
  justify-content: space-between;
}

.mobile-left {
  order: 1;
}

.mobile-right {
  order: 3;
}

/* Desktop Layout */
.top-bar:not(.mobile) .top-bar-content {
  justify-content: space-between;
}

.desktop-left {
  order: 1;
}

.app-title-section {
  order: 2;
  flex: 1;
  text-align: center;
}

.desktop-right {
  order: 3;
}

.flag-gender-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.flag-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.austrian-flag {
  width: 32px;
  height: 24px;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 2px;
  overflow: hidden;
}

.flag-stripe {
  height: 33.33%;
  width: 100%;
}

.flag-stripe.red {
  background: #ED2939;
}

.flag-stripe.white {
  background: #FFFFFF;
}

.gender-icons {
  display: flex;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.gender-icons:hover {
  background: rgba(255,255,255,0.1);
}

.gender-icon {
  width: 20px;
  height: 20px;
  color: white;
}

.gender-icon.male {
  color: #87CEEB;
}

.gender-icon.female {
  color: #FFB6C1;
}

.app-title {
  font-size: 1.5rem;
  margin: 0;
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

.preferences-section {
  display: flex;
  align-items: center;
}

.preferences-button {
  background: rgba(255,255,255,0.1);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.preferences-button:hover {
  background: rgba(255,255,255,0.2);
}

.preferences-button svg {
  width: 20px;
  height: 20px;
  color: white;
}

@media (max-width: 768px) {
  .top-bar {
    padding: 0.5rem 1rem;
  }

  .top-bar-content {
    height: 36px;
  }

  .austrian-flag {
    width: 28px;
    height: 20px;
  }

  .gender-icon {
    width: 18px;
    height: 18px;
  }

  .preferences-button {
    width: 32px;
    height: 32px;
  }

  .preferences-button svg {
    width: 18px;
    height: 18px;
  }
}
</style>

<template>
  <div class="preferences-view">
    <div class="container">
      <h1 class="title">Einstellungen</h1>

      <div class="preference-section">
        <h3 class="section-title">Sortierung</h3>
        <div class="radio-group">
          <label class="radio-option">
            <input
              type="radio"
              value="random"
              v-model="preferencesStore.sortOrder"
              @change="updateSortOrder"
            />
            <span class="radio-text">Zufällig</span>
          </label>
          <label class="radio-option">
            <input
              type="radio"
              value="most_popular"
              v-model="preferencesStore.sortOrder"
              @change="updateSortOrder"
            />
            <span class="radio-text">Beliebteste zuerst</span>
          </label>
          <label class="radio-option">
            <input
              type="radio"
              value="least_popular"
              v-model="preferencesStore.sortOrder"
              @change="updateSortOrder"
            />
            <span class="radio-text">Seltenste zuerst</span>
          </label>
        </div>
      </div>

      <div class="preference-section">
        <h3 class="section-title">Geschlecht</h3>
        <div class="checkbox-group">
          <label class="checkbox-option">
            <input
              type="checkbox"
              value="male"
              :checked="preferencesStore.selectedGenders.includes('male')"
              @change="toggleGender('male')"
            />
            <span class="checkbox-text">
              <svg class="gender-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9,9C10.29,9 11.5,9.41 12.47,10.11L17.58,5H13V3H21V11H19V6.41L13.89,11.5C14.59,12.5 15,13.7 15,15A6,6 0 0,1 9,21A6,6 0 0,1 3,15A6,6 0 0,1 9,9M9,11A4,4 0 0,0 5,15A4,4 0 0,0 9,19A4,4 0 0,0 13,15A4,4 0 0,0 9,11Z"/>
              </svg>
              Jungen
            </span>
          </label>
          <label class="checkbox-option">
            <input
              type="checkbox"
              value="female"
              :checked="preferencesStore.selectedGenders.includes('female')"
              @change="toggleGender('female')"
            />
            <span class="checkbox-text">
              <svg class="gender-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,4A6,6 0 0,1 18,10C18,12.97 15.84,15.44 13,15.92V18H15V20H13V22H11V20H9V18H11V15.92C8.16,15.44 6,12.97 6,10A6,6 0 0,1 12,4M12,6A4,4 0 0,0 8,10A4,4 0 0,0 12,14A4,4 0 0,0 16,10A4,4 0 0,0 12,6Z"/>
              </svg>
              Mädchen
            </span>
          </label>
        </div>
      </div>

      <div class="save-section">
        <button @click="goBack" class="save-button">
          Zurück
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { usePreferencesStore } from '@/stores/usePreferencesStore'
import { useNameBuffer } from '@/stores/useNameBuffer'
import { useRouter } from 'vue-router'

const preferencesStore = usePreferencesStore()
const nameBuffer = useNameBuffer()
const router = useRouter()

const updateSortOrder = () => {
  // The v-model already updates the store, but we trigger save here
  preferencesStore.setSortOrder(preferencesStore.sortOrder)
  // Clear the buffer so new names are fetched with updated preferences
  nameBuffer.clearBuffer()
}

const toggleGender = (gender) => {
  preferencesStore.toggleGender(gender)
  // Clear the buffer so new names are fetched with updated preferences
  nameBuffer.clearBuffer()
}

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.preferences-view {
  padding: 2rem;
  min-height: 100vh;
  background: #f8f9fa;
}

.container {
  max-width: 600px;
  margin: 0 auto;
}

.title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.preference-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 1rem;
  font-weight: 600;
}

.radio-group, .checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.radio-option, .checkbox-option {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.radio-option:hover, .checkbox-option:hover {
  background: #f8f9fa;
}

.radio-option input, .checkbox-option input {
  margin-right: 0.75rem;
  width: 16px;
  height: 16px;
}

.radio-text, .checkbox-text {
  font-size: 1rem;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.gender-icon {
  width: 20px;
  height: 20px;
  color: #007bff;
}

.save-section {
  text-align: center;
  padding: 1rem 0;
}

.save-button {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-button:hover {
  background: #0056b3;
}

@media (max-width: 768px) {
  .preferences-view {
    padding: 1rem;
  }

  .title {
    font-size: 1.5rem;
  }

  .preference-section {
    padding: 1rem;
  }
}
</style>

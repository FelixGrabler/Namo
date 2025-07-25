import { defineStore } from 'pinia'
import { ref } from 'vue'

export type SortOrder = 'random' | 'most_popular' | 'least_popular'
export type Gender = 'male' | 'female'

export const usePreferencesStore = defineStore('preferences', () => {
  // Default preferences
  const sortOrder = ref<SortOrder>('random')
  const selectedGenders = ref<Gender[]>(['male', 'female'])

  // Load from localStorage on initialization
  const loadPreferences = () => {
    const savedSortOrder = localStorage.getItem('sortOrder')
    const savedGenders = localStorage.getItem('selectedGenders')

    if (savedSortOrder && ['random', 'most_popular', 'least_popular'].includes(savedSortOrder)) {
      sortOrder.value = savedSortOrder as SortOrder
    }

    if (savedGenders) {
      try {
        const parsed = JSON.parse(savedGenders)
        if (Array.isArray(parsed) && parsed.every(g => ['male', 'female'].includes(g))) {
          selectedGenders.value = parsed
        }
      } catch (e) {
        console.warn('Failed to parse saved gender preferences')
      }
    }
  }

  // Save preferences to localStorage
  const savePreferences = () => {
    localStorage.setItem('sortOrder', sortOrder.value)
    localStorage.setItem('selectedGenders', JSON.stringify(selectedGenders.value))
  }

  // Update sort order
  const setSortOrder = (newSortOrder: SortOrder) => {
    sortOrder.value = newSortOrder
    savePreferences()
  }

  // Update selected genders
  const setGenders = (genders: Gender[]) => {
    selectedGenders.value = genders
    savePreferences()
  }

  // Toggle gender selection
  const toggleGender = (gender: Gender) => {
    if (selectedGenders.value.includes(gender)) {
      selectedGenders.value = selectedGenders.value.filter(g => g !== gender)
    } else {
      selectedGenders.value = [...selectedGenders.value, gender]
    }
    savePreferences()
  }

  // Get preferences for API requests
  const getApiParams = () => {
    return {
      sort_order: sortOrder.value,
      genders: selectedGenders.value
    }
  }

  // Load preferences on store creation
  loadPreferences()

  return {
    sortOrder,
    selectedGenders,
    setSortOrder,
    setGenders,
    toggleGender,
    getApiParams,
    loadPreferences
  }
})

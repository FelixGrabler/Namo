import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useNameService } from '@/api/nameService'
import { usePreferencesStore } from '@/stores/usePreferencesStore'
import type { NameResponse } from '@/types'

export const useNameBuffer = defineStore('nameBuffer', () => {
  const buffer = ref<NameResponse[]>([])
  const previousName = ref<NameResponse | null>(null)
  const BUFFER_MIN = 5
  const BUFFER_TARGET = 10

  const ensureBuffer = async () => {
    if (buffer.value.length >= BUFFER_MIN) return

    const existingIds = new Set(buffer.value.map(n => n.id))
    const preferencesStore = usePreferencesStore()

    try {
      const names = await useNameService().getRandomNames(BUFFER_TARGET, {
        sortOrder: preferencesStore.sortOrder,
        genders: preferencesStore.selectedGenders
      })
      for (const name of names) {
        if (!existingIds.has(name.id)) {
          buffer.value.push(name)
          existingIds.add(name.id)
        }
      }
    } catch (e) {
      console.warn('Buffer refill failed', e)
    }
  }

  const removeCurrentName = () => {
    const currentName = buffer.value[0]
    if (currentName) {
      previousName.value = currentName
      buffer.value.shift()
    }
  }

  const undoLastRemoval = () => {
    if (previousName.value) {
      buffer.value.unshift(previousName.value)
      previousName.value = null
    }
  }

  const canUndo = () => {
    return previousName.value !== null
  }

  // Clear buffer when preferences change
  const clearBuffer = () => {
    buffer.value = []
    previousName.value = null
  }

  return {
    buffer,
    previousName,
    ensureBuffer,
    removeCurrentName,
    undoLastRemoval,
    canUndo,
    clearBuffer,
  }
})

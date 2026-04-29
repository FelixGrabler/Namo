import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useNameService } from '@/api/nameService'
import { usePreferencesStore } from '@/stores/usePreferencesStore'
import { useLocalVotesStore } from '@/stores/useLocalVotesStore'
import type { NameResponse } from '@/types'

export const useNameBuffer = defineStore('nameBuffer', () => {
  const buffer = ref<NameResponse[]>([])
  const previousName = ref<NameResponse | null>(null)
  const locallyExcludedNameIds = ref<number[]>([])
  const BUFFER_MIN = 5
  const BUFFER_TARGET = 10
  let refillPromise: Promise<void> | null = null

  const getExcludedNameIds = () => {
    const localVotesStore = useLocalVotesStore()
    return Array.from(new Set([
      ...buffer.value.map(name => name.id),
      ...locallyExcludedNameIds.value,
      ...localVotesStore.votedNameIds
    ]))
  }

  const refillBuffer = async () => {
    if (buffer.value.length >= BUFFER_MIN) return

    const preferencesStore = usePreferencesStore()

    try {
      const names = await useNameService().getRandomNames(BUFFER_TARGET, {
        sortOrder: preferencesStore.sortOrder,
        genders: preferencesStore.selectedGenders,
        excludedNameIds: getExcludedNameIds()
      })

      for (const name of names) {
        const existingIds = new Set(buffer.value.map(n => n.id))
        const excludedIds = new Set(getExcludedNameIds())

        if (!existingIds.has(name.id)) {
          if (excludedIds.has(name.id)) continue
          buffer.value.push(name)
        }
      }
    } catch (e) {
      console.warn('Buffer refill failed', e)
    }
  }

  const ensureBuffer = async () => {
    if (buffer.value.length >= BUFFER_MIN) return
    if (refillPromise) return refillPromise

    refillPromise = refillBuffer()
      .finally(() => {
        refillPromise = null
      })

    return refillPromise
  }

  const recordVotedName = (nameId: number) => {
    if (!locallyExcludedNameIds.value.includes(nameId)) {
      locallyExcludedNameIds.value = [...locallyExcludedNameIds.value, nameId]
    }
  }

  const forgetVotedName = (nameId: number) => {
    locallyExcludedNameIds.value = locallyExcludedNameIds.value.filter(id => id !== nameId)
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
    refillPromise = null
  }

  return {
    buffer,
    previousName,
    ensureBuffer,
    recordVotedName,
    forgetVotedName,
    removeCurrentName,
    undoLastRemoval,
    canUndo,
    clearBuffer,
  }
})

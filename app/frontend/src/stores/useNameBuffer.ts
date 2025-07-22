import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useNameService } from '@/services/nameService'
import type { NameResponse } from '@/types'

export const useNameBuffer = defineStore('nameBuffer', () => {
  const buffer = ref<NameResponse[]>([])
  const BUFFER_MIN = 5
  const BUFFER_TARGET = 10

  const ensureBuffer = async () => {
    if (buffer.value.length >= BUFFER_MIN) return

    const existingIds = new Set(buffer.value.map(n => n.id))

    try {
      const names = await useNameService().getRandomNames(BUFFER_TARGET)
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
    buffer.value.shift()
  }

  return {
    buffer,
    ensureBuffer,
    removeCurrentName,
  }
})

<template>
  <div
    class="flex flex-col items-center justify-center rounded-2xl shadow p-6 w-full max-w-md bg-white"
    :class="genderClass"
  >
    <h1 class="text-4xl font-bold tracking-wide mb-2">{{ name.name }}</h1>
    <p class="text-sm text-gray-700">{{ name.source }} &middot; Rang {{ name.rank }} &middot; {{ name.count }} Nennungen</p>
  </div>
</template>

<script setup lang="ts">
import type { NameResponse } from '@/types'
import { computed } from 'vue'

interface Props {
  name: NameResponse
}

defineProps<Props>()

const genderClass = computed(() => {
  if (name.gender === 'm') return 'bg-blue-100'
  if (name.gender === 'f') return 'bg-pink-100'
  return 'bg-gray-100'
})
</script>

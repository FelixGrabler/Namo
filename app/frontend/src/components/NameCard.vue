<template>
  <div
    class="flex flex-col items-center justify-center rounded-2xl shadow p-6 w-full max-w-md"
    :class="cardClasses"
  >
    <div v-if="loading" class="flex flex-col items-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mb-4"></div>
      <p class="text-gray-500">Loading next name...</p>
    </div>
    <div v-else class="flex flex-col items-center">
      <h1 class="text-4xl font-bold tracking-wide mb-2">{{ name.name }}</h1>
      <p class="text-sm text-gray-700">{{ name.source }} &middot; Rang {{ name.rank }} &middot; {{ name.count }} Nennungen</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { NameResponse } from '@/types'

interface Props {
  name: NameResponse
  loading?: boolean
}

const props = defineProps<Props>()

const cardClasses = computed(() => ({
  'bg-blue-100': props.name?.gender === 'm',
  'bg-pink-100': props.name?.gender === 'f',
  'bg-white': !props.name?.gender || (props.name?.gender !== 'm' && props.name?.gender !== 'f'),
  'opacity-50': props.loading
}))
</script>

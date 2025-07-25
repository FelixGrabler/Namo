<template>
  <div
    class="min-h-screen w-full flex flex-col"
    :class="backgroundClasses"
  >
    <!-- Main content area with scroll -->
    <div class="flex-1 overflow-y-auto px-6 pt-12 pb-32" ref="scrollContainer">
      <div v-if="loading" class="flex flex-col items-center justify-center min-h-[50vh]">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mb-4"></div>
        <p class="text-gray-600">Loading next name...</p>
      </div>

      <div v-else class="flex flex-col items-center text-center space-y-6">
        <!-- Name -->
        <h1 class="text-5xl font-bold tracking-wide text-gray-900">{{ name.name }}</h1>

        <!-- IPA and Sound -->
        <div v-if="name.info?.ipa || name.info?.sound" class="flex items-center gap-3">
          <SpeakerWaveIcon
            v-if="name.info?.sound"
            class="h-6 w-6 text-gray-700 cursor-pointer hover:text-gray-900"
            @click="playSound"
          />
          <span v-if="name.info?.ipa" class="text-lg text-gray-700 font-mono">[ {{ name.info.ipa }} ]</span>
        </div>

        <!-- Count and Rank -->
        <div class="flex flex-col gap-2">
          <div v-if="name.rank" class="flex items-center justify-center gap-2">
            <!-- Podium icon -->
            <svg class="h-5 w-5 text-amber-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M5 16v2a1 1 0 001 1h3v-6H5v3zm5-6v8a1 1 0 001 1h3a1 1 0 001-1v-8h-5zm7 4v4a1 1 0 001 1h3v-5h-4z"/>
              <path d="M5 13h4V9H5v4zm5-6h5V5H10v2zm7 2h4v-2h-4v2z"/>
            </svg>
            <span class="text-gray-700">Rang {{ name.rank }}</span>
          </div>
          <div v-if="name.count" class="flex items-center justify-center gap-2">
            <UsersIcon class="h-5 w-5 text-blue-600" />
            <span class="text-gray-700">{{ name.count }} Nennungen</span>
          </div>
        </div>

        <!-- Source -->
        <p class="text-sm text-gray-600">{{ name.source }}</p>

        <!-- Herkunft -->
        <div v-if="name.info?.Herkunft" class="max-w-2xl">
          <p class="text-gray-800 leading-relaxed">{{ name.info.Herkunft }}</p>
        </div>

        <!-- Show more indicator -->
        <div
          v-if="hasMoreInfo && !showingMore"
          class="flex items-center gap-2 text-blue-600 cursor-pointer hover:text-blue-800"
          @click="scrollToMore"
        >
          <DocumentTextIcon class="h-5 w-5" />
          <span class="text-sm">Erfahre mehr</span>
        </div>

        <!-- Additional info fields (shown when scrolled or clicked) -->
        <div
          v-if="additionalInfoFields.length > 0 && showingMore"
          class="max-w-2xl space-y-6 mt-8"
          ref="moreInfoSection"
        >
          <div v-for="(field, index) in additionalInfoFields" :key="index" class="text-left">
            <h3 class="font-semibold text-gray-900 mb-2">{{ field.label }}</h3>
            <p class="text-gray-700 leading-relaxed">{{ field.value }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { SpeakerWaveIcon, UsersIcon, DocumentTextIcon } from '@heroicons/vue/24/outline'
import type { NameResponse } from '@/types'

interface Props {
  name: NameResponse
  loading?: boolean
}

const props = defineProps<Props>()

const scrollContainer = ref<HTMLElement>()
const moreInfoSection = ref<HTMLElement>()
const showingMore = ref(false)

const backgroundClasses = computed(() => ({
  'bg-blue-100': props.name?.gender === 'm',
  'bg-pink-100': props.name?.gender === 'f',
  'bg-gray-50': !props.name?.gender || (props.name?.gender !== 'm' && props.name?.gender !== 'f'),
  'opacity-50': props.loading
}))

const hasMoreInfo = computed(() => {
  if (!props.name?.info) return false
  const excludeFields = ['Herkunft', 'source_url', 'ipa', 'sound', 'aussprache_link']
  return Object.keys(props.name.info).some(key => !excludeFields.includes(key))
})

const additionalInfoFields = computed(() => {
  if (!props.name?.info) return []

  const excludeFields = ['Herkunft', 'source_url', 'ipa', 'sound', 'aussprache_link']
  const fieldLabels: { [key: string]: string } = {
    'Koseformen': 'Koseformen',
    'Abkürzungen': 'Abkürzungen',
    'Bedeutung': 'Bedeutung',
    'Varianten': 'Varianten',
    'Namenstag': 'Namenstag',
    'Bekannte_Namensträger': 'Bekannte Namensträger'
  }

  return Object.entries(props.name.info)
    .filter(([key]) => !excludeFields.includes(key))
    .map(([key, value]) => ({
      label: fieldLabels[key] || key,
      value: typeof value === 'string' ? value : JSON.stringify(value)
    }))
})

const scrollToMore = () => {
  showingMore.value = true
  // Wait for DOM update then scroll
  setTimeout(() => {
    if (moreInfoSection.value) {
      moreInfoSection.value.scrollIntoView({ behavior: 'smooth' })
    }
  }, 100)
}

const playSound = () => {
  if (props.name?.info?.sound) {
    // If it's a URL, play it
    if (typeof props.name.info.sound === 'string' && props.name.info.sound.startsWith('http')) {
      const audio = new Audio(props.name.info.sound)
      audio.play().catch(console.warn)
    }
  }
}
</script>

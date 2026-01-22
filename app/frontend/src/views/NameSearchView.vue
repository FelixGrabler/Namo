<template>
  <div class="min-h-screen bg-slate-50">
    <div class="max-w-5xl mx-auto px-6 py-10">
      <div class="flex flex-col gap-6">
        <header class="flex flex-col gap-2">
          <h1 class="text-3xl font-bold text-slate-900">Namensinfo</h1>
          <p class="text-slate-600">Finde Namen und sieh dir Statistiken und Herkunft an.</p>
        </header>

        <div class="relative">
          <input
            v-model="query"
            type="text"
            class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-800 shadow-sm focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-100"
            placeholder="Name suchen (z.B. Anna)"
          />
          <div v-if="loading" class="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-slate-400">
            Lädt...
          </div>
        </div>

        <section class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-slate-800">Treffer</h2>
            <span class="text-sm text-slate-500">{{ names.length }} Namen</span>
          </div>

          <div v-if="!names.length && !loading" class="text-sm text-slate-500">
            Keine Namen gefunden.
          </div>

          <ul class="divide-y divide-slate-100">
            <li
              v-for="name in names"
              :key="name.id"
              class="py-3 flex items-center justify-between gap-4 cursor-pointer hover:bg-slate-50 px-2 rounded-lg"
              @click="selectName(name)"
            >
              <div>
                <p class="text-slate-800 font-medium">{{ name.name }}</p>
                <p class="text-xs text-slate-500">{{ name.source }}</p>
              </div>
              <div class="text-xs text-slate-500">
                <span v-if="name.count">{{ name.count }} Nennungen</span>
                <span v-else>Keine Daten</span>
              </div>
            </li>
          </ul>

          <div class="mt-4 flex justify-center">
            <button
              v-if="hasMore"
              class="rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
              @click="loadMore"
              :disabled="loading"
            >
              Mehr laden
            </button>
          </div>
        </section>
      </div>
    </div>

    <div
      v-if="selectedName"
      class="fixed inset-0 z-50 flex flex-col bg-slate-900/60 backdrop-blur-sm"
    >
      <button
        class="self-end m-6 rounded-full bg-white/90 px-4 py-2 text-sm font-semibold text-slate-700 shadow"
        @click="closeDetails"
      >
        Schliessen
      </button>
      <NameCard :name="selectedName" :loading="infoLoading" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { NameResponse } from '@/types'
import { useNameService } from '@/api/nameService'
import NameCard from '@/components/NameCard.vue'

const nameService = useNameService()

const query = ref('')
const names = ref<NameResponse[]>([])
const loading = ref(false)
const hasMore = ref(true)
const selectedName = ref<NameResponse | null>(null)
const infoLoading = ref(false)

let searchTimeout: number | undefined

const fetchNames = async (reset = false) => {
  if (loading.value) return

  if (reset) {
    names.value = []
    hasMore.value = true
  }

  if (!hasMore.value) return

  loading.value = true
  const last = names.value[names.value.length - 1]

  try {
    const results = await nameService.searchNames(query.value, {
      limit: 20,
      afterName: last?.name ?? null,
      afterId: last?.id ?? null
    })

    if (reset) {
      names.value = results
    } else {
      names.value = [...names.value, ...results]
    }

    if (results.length < 20) {
      hasMore.value = false
    }
  } finally {
    loading.value = false
  }
}

const loadMore = () => fetchNames(false)

const selectName = async (name: NameResponse) => {
  selectedName.value = { ...name }
  infoLoading.value = true

  try {
    const info = await nameService.getNameInfo(name.name)
    selectedName.value = { ...name, info: info.info }
  } catch (error) {
    selectedName.value = { ...name }
  } finally {
    infoLoading.value = false
  }
}

const closeDetails = () => {
  selectedName.value = null
}

watch(
  query,
  () => {
    if (searchTimeout) {
      window.clearTimeout(searchTimeout)
    }
    searchTimeout = window.setTimeout(() => {
      fetchNames(true)
    }, 300)
  },
  { immediate: true }
)
</script>

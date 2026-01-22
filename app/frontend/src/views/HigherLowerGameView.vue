<template>
  <div class="min-h-screen bg-slate-50">
    <div class="max-w-5xl mx-auto px-6 py-10">
      <header class="flex flex-col gap-2 mb-6">
        <h1 class="text-3xl font-bold text-slate-900">Higher or Lower</h1>
        <p class="text-slate-600">Welcher Name wurde 2023 in Österreich häufiger vergeben?</p>
        <div class="flex items-center gap-3 text-sm">
          <span class="rounded-full bg-slate-900 text-white px-3 py-1">Streak: {{ streak }}</span>
          <span v-if="statusMessage" class="text-slate-500">{{ statusMessage }}</span>
        </div>
      </header>

      <div v-if="loading" class="rounded-2xl border border-slate-200 bg-white p-6 text-center text-slate-500">
        Lade Namen...
      </div>

      <div
        v-else-if="!leftName || !rightName"
        class="rounded-2xl border border-slate-200 bg-white p-6 text-center text-slate-500"
      >
        Keine Namen verfugbar. Bitte spater erneut versuchen.
        <div class="mt-4">
          <button
            class="rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
            @click="restartGame"
          >
            Neu laden
          </button>
        </div>
      </div>

      <div v-else class="space-y-6">
        <div class="grid gap-6 lg:grid-cols-2">
          <div class="rounded-3xl p-6 text-center shadow-sm border" :class="leftCardClasses">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-600">Links</p>
            <h2 class="text-3xl font-bold text-slate-900 mt-2">{{ leftName?.name }}</h2>
            <p class="text-xs text-slate-500 mt-1">{{ leftName?.source }}</p>
            <div class="mt-6 text-2xl font-semibold">
              <span v-if="revealLeft">{{ displayCounts.left }} Nennungen</span>
              <span v-else class="text-slate-500">?</span>
            </div>
          </div>

          <div class="rounded-3xl p-6 text-center shadow-sm border" :class="rightCardClasses">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-600">Rechts</p>
            <h2 class="text-3xl font-bold text-slate-900 mt-2">{{ rightName?.name }}</h2>
            <p class="text-xs text-slate-500 mt-1">{{ rightName?.source }}</p>
            <div class="mt-6 text-2xl font-semibold">
              <span v-if="revealRight">{{ displayCounts.right }} Nennungen</span>
              <span v-else class="text-slate-500">?</span>
            </div>
          </div>
        </div>

        <div class="rounded-2xl border border-slate-200 bg-white p-6 text-center">
          <p class="text-slate-700 mb-4">Ist der rechte Name höher oder niedriger als links?</p>
          <div class="flex flex-wrap justify-center gap-4">
            <button
              class="rounded-full bg-emerald-500 px-6 py-3 text-white font-semibold shadow hover:bg-emerald-600 disabled:opacity-50"
              @click="makeGuess('higher')"
              :disabled="isLocked"
            >
              Higher
            </button>
            <button
              class="rounded-full bg-amber-500 px-6 py-3 text-white font-semibold shadow hover:bg-amber-600 disabled:opacity-50"
              @click="makeGuess('lower')"
              :disabled="isLocked"
            >
              Lower
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="gameOver" class="fixed inset-0 z-50 bg-slate-900/70 flex items-center justify-center p-6">
      <div class="rounded-3xl bg-white p-8 text-center shadow-xl max-w-sm w-full">
        <h2 class="text-2xl font-bold text-slate-900 mb-2">Game Over</h2>
        <p class="text-slate-600 mb-6">Deine Streak</p>
        <div class="text-5xl font-bold text-slate-900 mb-6">{{ streak }}</div>
        <button
          class="rounded-full bg-slate-900 px-6 py-3 text-white font-semibold hover:bg-slate-800"
          @click="restartGame"
        >
          Nochmals spielen
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import type { NameResponse } from '@/types'
import { useNameService } from '@/api/nameService'

const nameService = useNameService()

const leftName = ref<NameResponse | null>(null)
const rightName = ref<NameResponse | null>(null)
const loading = ref(true)
const revealLeft = ref(false)
const revealRight = ref(false)
const isLocked = ref(false)
const gameOver = ref(false)
const streak = ref(0)
const statusMessage = ref('')

const displayCounts = reactive({ left: 0, right: 0 })

const leftCardClasses = computed(() => ({
  'bg-blue-100 border-blue-200': leftName.value?.gender === 'm',
  'bg-pink-100 border-pink-200': leftName.value?.gender === 'f',
  'bg-white border-slate-200': !leftName.value?.gender
}))

const rightCardClasses = computed(() => ({
  'bg-blue-100 border-blue-200': rightName.value?.gender === 'm',
  'bg-pink-100 border-pink-200': rightName.value?.gender === 'f',
  'bg-white border-slate-200': !rightName.value?.gender
}))

const animateCount = (side: 'left' | 'right', target: number) => {
  const startTime = performance.now()
  const duration = 700

  const tick = (now: number) => {
    const progress = Math.min((now - startTime) / duration, 1)
    displayCounts[side] = Math.floor(progress * target)
    if (progress < 1) {
      requestAnimationFrame(tick)
    }
  }
  requestAnimationFrame(tick)
}

const fetchRandomName = async (excludeId?: number) => {
  const results = await nameService.getRandomNames(1, {
    source: 'Österreich',
    requireCount: true,
    excludeVoted: false,
    topNByCount: 200
  })
  const candidate = results[0]
  if (candidate && candidate.id === excludeId) {
    return fetchRandomName(excludeId)
  }
  return candidate
}

const loadInitial = async () => {
  loading.value = true
  try {
    const results = await nameService.getRandomNames(2, {
      source: 'Österreich',
      requireCount: true,
      excludeVoted: false,
      topNByCount: 200
    })
    leftName.value = results[0] ?? null
    rightName.value = results[1] ?? null
    revealLeft.value = false
    revealRight.value = false
    displayCounts.left = 0
    displayCounts.right = 0
  } finally {
    loading.value = false
  }
}

const makeGuess = async (choice: 'higher' | 'lower') => {
  if (!leftName.value || !rightName.value) return

  isLocked.value = true
  revealLeft.value = true
  revealRight.value = true

  const leftCount = leftName.value.count ?? 0
  const rightCount = rightName.value.count ?? 0

  animateCount('left', leftCount)
  animateCount('right', rightCount)

  const isHigher = rightCount > leftCount
  const correct = (choice === 'higher' && isHigher) || (choice === 'lower' && !isHigher)

  if (!correct) {
    statusMessage.value = 'Leider falsch!'
    gameOver.value = true
    isLocked.value = false
    return
  }

  streak.value += 1
  statusMessage.value = 'Richtig!'

  setTimeout(async () => {
    leftName.value = rightName.value
    revealLeft.value = true
    displayCounts.left = rightCount

    const next = await fetchRandomName(rightName.value?.id)
    rightName.value = next ?? null
    revealRight.value = false
    displayCounts.right = 0
    statusMessage.value = ''
    isLocked.value = false
  }, 900)
}

const restartGame = async () => {
  gameOver.value = false
  streak.value = 0
  statusMessage.value = ''
  await loadInitial()
}

void loadInitial()
</script>

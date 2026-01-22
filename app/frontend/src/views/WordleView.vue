<template>
  <div class="min-h-screen bg-slate-50">
    <div class="max-w-4xl mx-auto px-6 py-10">
      <header class="text-center mb-8">
        <h1 class="text-3xl font-bold text-slate-900">Name Wordle</h1>
        <p class="text-slate-600 mt-2">Errate den 5-Buchstaben-Namen.</p>
      </header>

      <div class="flex flex-col items-center gap-6">
        <div class="grid gap-2">
          <div v-for="row in maxRows" :key="row" class="grid grid-cols-5 gap-2">
            <div
              v-for="col in 5"
              :key="col"
              class="h-12 w-12 rounded-lg border border-slate-200 text-lg font-bold flex items-center justify-center uppercase transition"
              :class="cellClass(row - 1, col - 1)"
            >
              {{ cellLetter(row - 1, col - 1) }}
            </div>
          </div>
        </div>

        <div class="w-full max-w-sm space-y-3">
          <input
            v-model="currentGuess"
            type="text"
            maxlength="5"
            class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-center text-lg font-semibold uppercase tracking-[0.3em] focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-100 disabled:bg-slate-100"
            placeholder="ABCDE"
            :disabled="gameStatus !== 'playing'"
            @keydown.enter.prevent="submitGuess"
          />
          <button
            class="w-full rounded-full bg-slate-900 px-6 py-3 text-white font-semibold hover:bg-slate-800 disabled:opacity-50"
            @click="submitGuess"
            :disabled="gameStatus !== 'playing'"
          >
            Tipp abgeben
          </button>
          <p v-if="message" class="text-sm text-slate-600 text-center">{{ message }}</p>
        </div>

        <div v-if="gameStatus === 'won'" class="rounded-2xl bg-emerald-100 px-6 py-4 text-emerald-700 font-semibold">
          Treffer! Du hast den Namen erraten.
        </div>
        <div v-if="gameStatus === 'lost'" class="rounded-2xl bg-rose-100 px-6 py-4 text-rose-700 font-semibold">
          Schade! Der Name war {{ targetDisplay }}.
        </div>

        <button
          v-if="gameStatus !== 'playing'"
          class="rounded-full border border-slate-200 px-6 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-100"
          @click="restartGame"
        >
          Neues Spiel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useNameService } from '@/api/nameService'

type CellStatus = 'correct' | 'present' | 'absent' | 'empty'

const nameService = useNameService()

const maxRows = 6
const guesses = ref<{ word: string; statuses: CellStatus[] }[]>([])
const currentGuess = ref('')
const targetName = ref('')
const gameStatus = ref<'playing' | 'won' | 'lost'>('playing')
const message = ref('')

const targetDisplay = computed(() => targetName.value.toUpperCase())

const fetchTarget = async () => {
  const response = await nameService.getWordleTarget()
  targetName.value = response.name.toLowerCase()
}

const resetState = async () => {
  guesses.value = []
  currentGuess.value = ''
  message.value = ''
  gameStatus.value = 'playing'
  await fetchTarget()
}

const evaluateGuess = (guess: string, target: string): CellStatus[] => {
  const statuses: CellStatus[] = Array(5).fill('absent')
  const targetLetters = target.split('')
  const remaining: Record<string, number> = {}

  for (let i = 0; i < 5; i += 1) {
    if (guess[i] === targetLetters[i]) {
      statuses[i] = 'correct'
      targetLetters[i] = '*'
    } else {
      remaining[targetLetters[i]] = (remaining[targetLetters[i]] || 0) + 1
    }
  }

  for (let i = 0; i < 5; i += 1) {
    if (statuses[i] === 'correct') continue
    const letter = guess[i]
    if (remaining[letter]) {
      statuses[i] = 'present'
      remaining[letter] -= 1
    } else {
      statuses[i] = 'absent'
    }
  }

  return statuses
}

const submitGuess = async () => {
  if (gameStatus.value !== 'playing') return

  const guess = currentGuess.value.trim().toLowerCase()
  message.value = ''

  if (!/^[a-zA-Z]{5}$/.test(guess)) {
    message.value = 'Bitte genau 5 Buchstaben eingeben.'
    return
  }

  const validation = await nameService.validateWordle(guess)
  if (!validation.valid) {
    message.value = 'Name nicht in der Liste.'
    return
  }

  const statuses = evaluateGuess(guess, targetName.value)
  guesses.value = [...guesses.value, { word: guess, statuses }]
  currentGuess.value = ''

  if (guess === targetName.value) {
    gameStatus.value = 'won'
    return
  }

  if (guesses.value.length >= maxRows) {
    gameStatus.value = 'lost'
  }
}

const cellLetter = (row: number, col: number) => {
  if (row < guesses.value.length) {
    return guesses.value[row].word[col]?.toUpperCase() ?? ''
  }
  if (row === guesses.value.length) {
    return currentGuess.value[col]?.toUpperCase() ?? ''
  }
  return ''
}

const cellClass = (row: number, col: number) => {
  if (row < guesses.value.length) {
    const status = guesses.value[row].statuses[col]
    return {
      'bg-emerald-500 text-white border-emerald-500': status === 'correct',
      'bg-amber-400 text-white border-amber-400': status === 'present',
      'bg-slate-400 text-white border-slate-400': status === 'absent'
    }
  }
  return 'bg-white'
}

const restartGame = async () => {
  await resetState()
}

void resetState()
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <div class="max-w-6xl mx-auto px-6 py-10">
      <div class="grid gap-8 lg:grid-cols-[1.1fr_1.4fr]">
        <section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 class="text-2xl font-bold text-slate-900 mb-2">Vergleich</h1>
          <p class="text-sm text-slate-600 mb-4">
            Wähle eine Person aus, um gemeinsame Likes zu sehen.
          </p>

          <div class="relative mb-4">
            <input
              v-model="query"
              type="text"
              class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-800 shadow-sm focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-100"
              placeholder="Username suchen"
            />
            <div v-if="loadingUsers" class="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-400">
              Lädt...
            </div>
          </div>

          <div v-if="!users.length && !loadingUsers" class="text-sm text-slate-500">
            Keine Benutzer gefunden.
          </div>

          <ul class="divide-y divide-slate-100">
            <li
              v-for="user in users"
              :key="user.id"
              class="py-3 px-2 rounded-lg cursor-pointer hover:bg-slate-50"
              :class="{ 'bg-blue-50': selectedUser?.id === user.id }"
              @click="selectUser(user)"
            >
              <p class="font-medium text-slate-800">{{ user.username }}</p>
              <p class="text-xs text-slate-500">ID {{ user.id }}</p>
            </li>
          </ul>

          <div class="mt-4 flex justify-center">
            <button
              v-if="hasMoreUsers"
              class="rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
              @click="loadMoreUsers"
              :disabled="loadingUsers"
            >
              Mehr laden
            </button>
          </div>
        </section>

        <section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 class="text-xl font-semibold text-slate-900 mb-2">Gemeinsame Votes</h2>
          <p class="text-sm text-slate-600 mb-6">
            {{ resultText }}
          </p>

          <div v-if="loadingCompare" class="text-sm text-slate-500">
            Vergleich läuft...
          </div>

          <div v-else-if="compareResult">
            <div v-if="compareResult.both.length === 0" class="text-sm text-slate-500">
              Noch keine gemeinsamen Likes.
            </div>

            <div v-else class="flex flex-wrap gap-2">
              <span
                v-for="name in compareResult.both"
                :key="name.id"
                class="rounded-full bg-emerald-100 px-3 py-1 text-sm font-medium text-emerald-700"
              >
                {{ name.name }}
              </span>
            </div>
          </div>

          <div v-else class="text-sm text-slate-500">
            Bitte wähle eine Person links aus.
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { UserResponse, VoteCompareResponse } from '@/types'
import { useUserService } from '@/api/userService'
import { useVoteService } from '@/api/voteService'

const userService = useUserService()
const voteService = useVoteService()

const query = ref('')
const users = ref<UserResponse[]>([])
const loadingUsers = ref(false)
const hasMoreUsers = ref(true)
const selectedUser = ref<UserResponse | null>(null)

const compareResult = ref<VoteCompareResponse | null>(null)
const loadingCompare = ref(false)

let searchTimeout: number | undefined

const fetchUsers = async (reset = false) => {
  if (loadingUsers.value) return

  if (reset) {
    users.value = []
    hasMoreUsers.value = true
  }

  if (!hasMoreUsers.value) return

  loadingUsers.value = true
  const last = users.value[users.value.length - 1]

  try {
    const results = await userService.searchUsers(query.value, {
      limit: 20,
      afterUsername: last?.username ?? null,
      afterId: last?.id ?? null
    })

    if (reset) {
      users.value = results
    } else {
      users.value = [...users.value, ...results]
    }

    if (results.length < 20) {
      hasMoreUsers.value = false
    }
  } finally {
    loadingUsers.value = false
  }
}

const loadMoreUsers = () => fetchUsers(false)

const selectUser = async (user: UserResponse) => {
  selectedUser.value = user
  loadingCompare.value = true
  compareResult.value = null

  try {
    compareResult.value = await voteService.compareVotes(user.username)
  } finally {
    loadingCompare.value = false
  }
}

const resultText = computed(() => {
  if (!selectedUser.value) {
    return 'Noch keine Auswahl.'
  }

  if (!compareResult.value) {
    return `Vergleiche mit ${selectedUser.value.username}...`
  }

  return `Ihr habt ${compareResult.value.both.length} Übereinstimmungen`
})

watch(
  query,
  () => {
    if (searchTimeout) {
      window.clearTimeout(searchTimeout)
    }
    searchTimeout = window.setTimeout(() => {
      fetchUsers(true)
    }, 300)
  },
  { immediate: true }
)
</script>

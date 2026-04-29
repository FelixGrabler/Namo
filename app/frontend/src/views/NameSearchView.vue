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
      class="name-detail-overlay"
    >
      <div class="name-detail-header">
        <div>
          <p class="name-detail-kicker">Namensinfo</p>
          <h2 class="name-detail-title">{{ selectedName.name }}</h2>
        </div>
        <button
          class="name-detail-close"
          @click="closeDetails"
          aria-label="Schliessen"
        >
          ×
        </button>
      </div>

      <div class="name-detail-card">
        <NameCard :name="selectedName" :loading="infoLoading" />
      </div>

      <div class="search-vote-buttons">
        <VoteButtons
          :canUndo="false"
          :activeVote="selectedNameVote"
          @like="voteForSelectedName(true)"
          @dislike="voteForSelectedName(false)"
        />
        <p v-if="selectedNameVote !== null" class="mt-3 text-center text-sm font-semibold text-white drop-shadow">
          {{ selectedNameVote ? 'Als Like gespeichert' : 'Als Dislike gespeichert' }}
        </p>
      </div>

      <div v-if="showAccountPrompt" class="account-prompt-overlay" @click="ignoreAccountPrompt">
        <div class="account-prompt" @click.stop>
          <h2>Votes im Konto speichern?</h2>
          <p>Mit einem Login bleiben deine Bewertungen dauerhaft erhalten.</p>
          <div class="account-prompt-actions">
            <button class="login-action" @click="goToLogin">Login</button>
            <button class="ignore-action" @click="ignoreAccountPrompt">Ignorieren</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import type { NameResponse, VoteCreate } from '@/types'
import { useNameService } from '@/api/nameService'
import { useVoteService } from '@/api/voteService'
import { useUserStore } from '@/stores/useUserStore'
import { useLocalVotesStore } from '@/stores/useLocalVotesStore'
import NameCard from '@/components/NameCard.vue'
import VoteButtons from '@/components/VoteButtons.vue'

const router = useRouter()
const nameService = useNameService()
const voteService = useVoteService()
const userStore = useUserStore()
const localVotesStore = useLocalVotesStore()

const query = ref('')
const names = ref<NameResponse[]>([])
const loading = ref(false)
const hasMore = ref(true)
const selectedName = ref<NameResponse | null>(null)
const infoLoading = ref(false)
const submittedSelectedVotes = ref<Record<number, boolean>>({})

let searchTimeout: number | undefined

const selectedNameVote = computed(() => {
  if (!selectedName.value) return null

  const submittedVote = submittedSelectedVotes.value[selectedName.value.id]
  if (submittedVote !== undefined) return submittedVote

  if (!userStore.isAuthenticated) {
    const localVote = localVotesStore.votes.find(vote => vote.name_id === selectedName.value?.id)
    if (localVote) return localVote.vote
  }

  return null
})

const showAccountPrompt = computed(() => {
  return !userStore.isAuthenticated && localVotesStore.shouldPromptForAccount
})

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

const voteForSelectedName = async (vote: boolean) => {
  if (!selectedName.value) return

  const votePayload: VoteCreate = {
    name_id: selectedName.value.id,
    vote
  }

  if (!userStore.isAuthenticated) {
    localVotesStore.addVote(votePayload)
    submittedSelectedVotes.value = {
      ...submittedSelectedVotes.value,
      [selectedName.value.id]: vote
    }
    return
  }

  try {
    await voteService.submitVote(votePayload)
    submittedSelectedVotes.value = {
      ...submittedSelectedVotes.value,
      [selectedName.value.id]: vote
    }
  } catch (err: any) {
    if (err?.response?.status === 401) {
      userStore.logout()
      router.push('/login')
    }
  }
}

const goToLogin = () => {
  router.push('/login')
}

const ignoreAccountPrompt = () => {
  localVotesStore.dismissAccountPrompt()
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

<style scoped>
.name-detail-overlay {
  position: fixed;
  inset: 0;
  z-index: 2100;
  display: flex;
  flex-direction: column;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
}

.name-detail-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 2120;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 4.75rem;
  padding: 0.85rem 1.25rem;
  background: rgba(255, 255, 255, 0.96);
  border-bottom: 1px solid rgba(148, 163, 184, 0.35);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
}

.name-detail-kicker {
  margin: 0 0 0.15rem;
  color: #64748b;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.name-detail-title {
  margin: 0;
  color: #0f172a;
  font-size: 1.35rem;
  font-weight: 800;
}

.name-detail-close {
  width: 2.75rem;
  height: 2.75rem;
  border: 1px solid rgba(148, 163, 184, 0.5);
  border-radius: 999px;
  background: white;
  color: #334155;
  font-size: 1.8rem;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.1);
}

.name-detail-card {
  height: 100%;
  padding-top: 4.75rem;
}

.search-vote-buttons {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 2rem;
  z-index: 2130;
}

.account-prompt-overlay {
  position: fixed;
  inset: 0;
  z-index: 2140;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.5);
}

.account-prompt {
  width: min(24rem, 100%);
  border-radius: 8px;
  background: white;
  padding: 1.5rem;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.25);
}

.account-prompt h2 {
  margin: 0 0 0.5rem;
  color: #111827;
  font-size: 1.35rem;
  font-weight: 700;
}

.account-prompt p {
  margin: 0;
  color: #4b5563;
  line-height: 1.5;
}

.account-prompt-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.25rem;
}

.account-prompt-actions button {
  border: none;
  border-radius: 6px;
  padding: 0.7rem 1rem;
  font-weight: 600;
  cursor: pointer;
}

.login-action {
  background: #007bff;
  color: white;
}

.ignore-action {
  background: #f3f4f6;
  color: #374151;
}
</style>

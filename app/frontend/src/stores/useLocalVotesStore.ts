import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type { VoteCreate } from '@/types'

const STORAGE_KEY = 'anonymous_votes'
const PROMPT_DISMISSED_KEY = 'anonymous_vote_prompt_dismissed'

export interface StoredLocalVote extends VoteCreate {
  voted_at: string
}

const readVotes = (): StoredLocalVote[] => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return []
    const parsed = JSON.parse(stored)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export const useLocalVotesStore = defineStore('localVotes', () => {
  const votes = ref<StoredLocalVote[]>(readVotes())
  const accountPromptDismissed = ref(localStorage.getItem(PROMPT_DISMISSED_KEY) === 'true')

  const persist = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(votes.value))
  }

  const votedNameIds = computed(() => votes.value.map(vote => vote.name_id))
  const likeCount = computed(() => votes.value.filter(vote => vote.vote).length)
  const dislikeCount = computed(() => votes.value.filter(vote => !vote.vote).length)
  const shouldPromptForAccount = computed(() => {
    return !accountPromptDismissed.value && (likeCount.value >= 1 || dislikeCount.value >= 10)
  })

  const addVote = (vote: VoteCreate) => {
    const existingIndex = votes.value.findIndex(existing => existing.name_id === vote.name_id)
    const storedVote = {
      ...vote,
      voted_at: new Date().toISOString()
    }

    if (existingIndex >= 0) {
      votes.value[existingIndex] = storedVote
    } else {
      votes.value.push(storedVote)
    }

    persist()
  }

  const removeVote = (nameId: number) => {
    votes.value = votes.value.filter(vote => vote.name_id !== nameId)
    persist()
  }

  const clearVotes = () => {
    votes.value = []
    localStorage.removeItem(STORAGE_KEY)
  }

  const dismissAccountPrompt = () => {
    accountPromptDismissed.value = true
    localStorage.setItem(PROMPT_DISMISSED_KEY, 'true')
  }

  return {
    votes,
    votedNameIds,
    shouldPromptForAccount,
    addVote,
    removeVote,
    clearVotes,
    dismissAccountPrompt,
  }
})

<template>
  <div class="relative min-h-screen w-full overflow-hidden">
    <NameCard v-if="currentName" :name="currentName" />

    <!-- Vote buttons positioned at bottom -->
    <div class="vote-buttons-container">
      <VoteButtons
        v-if="currentName"
        @like="handleVote(true)"
        @dislike="handleVote(false)"
        @undo="handleUndo"
        :canUndo="nameBuffer.canUndo()"
        class="py-6"
      />
    </div>

    <div v-if="!currentName" class="flex items-center justify-center min-h-screen text-center text-gray-500 bg-gray-50">
      Loading...
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
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import { useNameBuffer } from '@/stores/useNameBuffer'
import { useLocalVotesStore } from '@/stores/useLocalVotesStore'
import { useVoteService } from '@/api/voteService'
import type { VoteCreate } from '@/types'

import NameCard from '@/components/NameCard.vue'
import VoteButtons from '@/components/VoteButtons.vue'

const router = useRouter()
const userStore = useUserStore()
const nameBuffer = useNameBuffer()
const localVotesStore = useLocalVotesStore()

const currentName = computed(() => nameBuffer.buffer[0] || null)
const showAccountPrompt = computed(() => {
  return !userStore.isAuthenticated && localVotesStore.shouldPromptForAccount
})

onMounted(async () => {
  await nameBuffer.ensureBuffer()

  // Add global keyboard listener
  document.addEventListener('keydown', handleGlobalKeydown)
})

onUnmounted(() => {
  // Clean up keyboard listener
  document.removeEventListener('keydown', handleGlobalKeydown)
})

const handleVote = (vote: boolean) => {
  console.log('handleVote', vote)
  if (!currentName.value) return

  const selectedName = currentName.value
  nameBuffer.removeCurrentName()
  nameBuffer.ensureBuffer()
  const votePayload = { name_id: selectedName.id, vote }

  if (userStore.isAuthenticated) {
    void sendVote(votePayload)
  } else {
    localVotesStore.addVote(votePayload)
  }
}

const handleUndo = () => {
  console.log('handleUndo')
  if (!userStore.isAuthenticated && nameBuffer.previousName) {
    localVotesStore.removeVote(nameBuffer.previousName.id)
  }
  nameBuffer.undoLastRemoval()
}

const handleGlobalKeydown = (event: KeyboardEvent) => {
  if (!currentName.value) return

  switch (event.key) {
    case 'ArrowLeft':
      event.preventDefault()
      handleVote(false) // dislike
      break
    case 'ArrowRight':
      event.preventDefault()
      handleVote(true) // like
      break
    case 'ArrowUp':
    case 'Backspace':
      event.preventDefault()
      if (nameBuffer.canUndo()) {
        handleUndo()
      }
      break
  }
}

const sendVote = async (vote: VoteCreate) => {
  try {
    await useVoteService().submitVote(vote)
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
</script>

<style scoped>
.vote-buttons-container {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 2rem;
  z-index: 10;
}

/* Mobile adjustments - position above the mobile navigation */
@media (max-width: 768px) {
  .vote-buttons-container {
    bottom: 4.5rem; /* Closer to mobile nav bar */
  }
}

/* Desktop adjustments - closer to bottom but with some spacing */
@media (min-width: 769px) {
  .vote-buttons-container {
    bottom: 0.75rem; /* Much closer to bottom */
  }
}

.account-prompt-overlay {
  position: fixed;
  inset: 0;
  z-index: 50;
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

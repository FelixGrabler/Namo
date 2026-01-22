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
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import { useNameBuffer } from '@/stores/useNameBuffer'
import { useVoteService } from '@/api/voteService'
import type { VoteCreate } from '@/types'

import NameCard from '@/components/NameCard.vue'
import VoteButtons from '@/components/VoteButtons.vue'

const router = useRouter()
const userStore = useUserStore()
const nameBuffer = useNameBuffer()

const currentName = computed(() => nameBuffer.buffer[0] || null)

onMounted(async () => {
  if (!userStore.isAuthenticated) {
    router.push('/login')
    return
  }
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
  void sendVote({ name_id: selectedName.id, vote })
}

const handleUndo = () => {
  console.log('handleUndo')
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
</style>

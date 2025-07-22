<template>
  <div class="flex flex-col items-center justify-center h-full p-4">
    <NameCard v-if="currentName" :name="currentName" />

    <VoteButtons
      v-if="currentName"
      @like="handleVote(true)"
      @dislike="handleVote(false)"
    />

    <div v-else class="text-center text-gray-500">Loading...</div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import { useNameBuffer } from '@/stores/useNameBuffer'
import { useVoteService } from '@/api/voteService'

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
})

const handleVote = async (vote: boolean) => {
  console.log('handleVote', vote)
  if (!currentName.value) return

  try {
    await useVoteService().submitVote({ name_id: currentName.value.id, vote })
    nameBuffer.removeCurrentName()
    await nameBuffer.ensureBuffer()
  } catch (err: any) {
    if (err?.response?.status === 401) {
      userStore.logout()
      router.push('/login')
    }
  }
}
</script>

<style scoped>
/* TODO */
</style>

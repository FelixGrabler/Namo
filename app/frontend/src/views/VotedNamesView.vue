<template>
  <div class="voted-names-view">
    <!-- Toggle Buttons -->
    <div class="toggle-container">
      <div class="toggle-buttons">
        <button
          :class="['toggle-btn', 'likes-btn', { active: showLikes }]"
          @click="setFilter(true)"
        >
          <span class="icon">❤️</span>
          <span>Likes</span>
        </button>
        <button
          :class="['toggle-btn', 'dislikes-btn', { active: !showLikes }]"
          @click="setFilter(false)"
        >
          <span class="icon">✕</span>
          <span>Dislikes</span>
        </button>
      </div>
    </div>

    <!-- Vote List -->
    <div class="vote-list">
      <div v-if="loading" class="loading">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        <p>Loading votes...</p>
      </div>

      <div v-else-if="votes.length === 0" class="empty-state">
        <p>{{ showLikes ? 'No liked names yet' : 'No disliked names yet' }}</p>
      </div>

      <div v-else class="votes-container">
        <div
          v-for="vote in votes"
          :key="vote.id"
          :class="[
            'vote-item',
            {
              'male': vote.name.gender === 'm',
              'female': vote.name.gender === 'f'
            }
          ]"
        >
          <div class="name-info">
            <span class="name-text">{{ vote.name.name }}</span>
          </div>
          <button
            :class="['action-btn', showLikes ? 'dislike-action' : 'like-action']"
            @click="showToggleConfirmation(vote)"
            :title="showLikes ? 'Dislike this name' : 'Like this name'"
          >
            {{ showLikes ? '✕' : '❤️' }}
          </button>
        </div>
      </div>

      <!-- Load More Button -->
      <div v-if="hasMore && !loading" class="load-more-container">
        <button @click="loadMore" class="load-more-btn" :disabled="loadingMore">
          {{ loadingMore ? 'Loading...' : 'Load More' }}
        </button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">Vote ändern</h3>
        <p class="modal-message">
          Möchtest du <strong>{{ voteToDelete?.name.name }}</strong> wirklich {{ showLikes ? 'disliken' : 'liken' }}?
        </p>
        <div class="modal-actions">
          <button @click="confirmToggle" class="confirm-btn">
            Ja, {{ showLikes ? 'disliken' : 'liken' }}
          </button>
          <button @click="closeModal" class="cancel-btn">
            Abbrechen
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import { useVoteService } from '@/api/voteService'
import type { VoteWithName } from '@/types'

const router = useRouter()
const userStore = useUserStore()
const voteService = useVoteService()

const showLikes = ref(true)
const votes = ref<VoteWithName[]>([])
const loading = ref(true)
const loadingMore = ref(false)
const hasMore = ref(true)
const currentSkip = ref(0)
const limit = 20

const showModal = ref(false)
const voteToDelete = ref<VoteWithName | null>(null)

onMounted(async () => {
  if (!userStore.isAuthenticated) {
    router.push('/login')
    return
  }
  await loadVotes()
})

watch(showLikes, async () => {
  await loadVotes()
})

const setFilter = (likes: boolean) => {
  showLikes.value = likes
}

const loadVotes = async (append = false) => {
  try {
    if (!append) {
      loading.value = true
      votes.value = []
      currentSkip.value = 0
    } else {
      loadingMore.value = true
    }

    const newVotes = await voteService.getVotes(showLikes.value, currentSkip.value, limit)

    if (append) {
      votes.value = [...votes.value, ...newVotes]
    } else {
      votes.value = newVotes
    }

    hasMore.value = newVotes.length === limit
    currentSkip.value += newVotes.length

  } catch (err: any) {
    console.error('Error loading votes:', err)
    if (err?.response?.status === 401) {
      userStore.logout()
      router.push('/login')
    }
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const loadMore = async () => {
  await loadVotes(true)
}

const showToggleConfirmation = (vote: VoteWithName) => {
  voteToDelete.value = vote
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  voteToDelete.value = null
}

const confirmToggle = async () => {
  if (!voteToDelete.value) return

  try {
    // Submit the opposite vote
    await voteService.submitVote({
      name_id: voteToDelete.value.name_id,
      vote: !voteToDelete.value.vote
    })

    // Remove from current list since it now belongs to the other category
    votes.value = votes.value.filter((v: VoteWithName) => v.id !== voteToDelete.value!.id)
    closeModal()
  } catch (err: any) {
    console.error('Error toggling vote:', err)
    if (err?.response?.status === 401) {
      userStore.logout()
      router.push('/login')
    }
  }
}
</script>

<style scoped>
.voted-names-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.toggle-container {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.toggle-buttons {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.toggle-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  background: #f8f9fa;
  color: #6c757d;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  font-size: 1rem;
}

.toggle-btn:hover {
  background: #e9ecef;
}

.toggle-btn.active.likes-btn {
  background: #dcfce7;
  color: #15803d;
}

.toggle-btn.active.dislikes-btn {
  background: #fef2f2;
  color: #dc2626;
}

.toggle-btn .icon {
  font-size: 1.2rem;
}

.vote-list {
  min-height: 200px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  color: #6c757d;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.votes-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.vote-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.vote-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.vote-item.male {
  background: #dbeafe; /* blue-100 */
}

.vote-item.female {
  background: #fce7f3; /* pink-100 */
}

.name-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.name-text {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
}

.action-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.2s ease;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
}

.action-btn:hover {
  background: #e9ecef;
}

.dislike-action {
  color: #dc2626;
}

.dislike-action:hover {
  color: #b91c1c;
}

.like-action {
  color: #15803d;
}

.like-action:hover {
  color: #166534;
}

.load-more-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.load-more-btn {
  padding: 0.75rem 2rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s ease;
}

.load-more-btn:hover:not(:disabled) {
  background: #0056b3;
}

.load-more-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-title {
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
}

.modal-message {
  margin: 0 0 2rem 0;
  color: #6c757d;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.confirm-btn {
  padding: 0.75rem 1.5rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s ease;
}

.confirm-btn:hover {
  background: #c82333;
}

.cancel-btn {
  padding: 0.75rem 1.5rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s ease;
}

.cancel-btn:hover {
  background: #545b62;
}
</style>

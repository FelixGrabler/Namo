<template>
  <div class="flex justify-center items-center gap-8 px-6">
    <!-- Dislike button with X icon -->
    <button
      class="bg-red-500 hover:bg-red-600 active:bg-red-700 text-white rounded-full w-20 h-20 shadow-lg focus:outline-none focus:ring-4 focus:ring-red-300 transition-all duration-150 flex items-center justify-center"
      @click="vote(false)"
    >
      <svg class="w-8 h-8" viewBox="0 0 24 24" fill="currentColor">
        <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
      </svg>
    </button>

    <!-- Undo button with undo icon -->
    <button
      class="bg-white hover:bg-gray-100 active:bg-gray-200 text-gray-700 rounded-full w-14 h-14 shadow-lg focus:outline-none focus:ring-4 focus:ring-gray-300 transition-all duration-150 border border-gray-300 flex items-center justify-center"
      @click="undo"
      :disabled="!canUndo"
      :class="{ 'opacity-50 cursor-not-allowed': !canUndo }"
      title="Undo last vote"
    >
      <svg class="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12.5,8C9.85,8 7.45,9 5.6,10.6L2,7V16H11L7.38,12.38C8.77,11.22 10.54,10.5 12.5,10.5C16.04,10.5 19.05,12.81 20.1,16L22.47,15.22C21.08,11.03 17.15,8 12.5,8Z"/>
      </svg>
    </button>

    <!-- Like button with heart icon -->
    <button
      class="bg-green-500 hover:bg-green-600 active:bg-green-700 text-white rounded-full w-20 h-20 shadow-lg focus:outline-none focus:ring-4 focus:ring-green-300 transition-all duration-150 flex items-center justify-center"
      @click="vote(true)"
    >
      <svg class="w-8 h-8" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12,21.35L10.55,20.03C5.4,15.36 2,12.27 2,8.5C2,5.41 4.42,3 7.5,3C9.24,3 10.91,3.81 12,5.08C13.09,3.81 14.76,3 16.5,3C19.58,3 22,5.41 22,8.5C22,12.27 18.6,15.36 13.45,20.03L12,21.35Z"/>
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  canUndo?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  canUndo: false
})

const emit = defineEmits<{
  (e: 'like'): void
  (e: 'dislike'): void
  (e: 'undo'): void
}>()

const vote = (isLike: boolean) => {
  if (isLike) {
    emit('like')
  } else {
    emit('dislike')
  }
}

const undo = () => {
  emit('undo')
}
</script>

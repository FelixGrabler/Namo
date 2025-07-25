<template>
  <div class="flex justify-center items-center gap-24 px-6">
    <button
      class="bg-red-500 hover:bg-red-600 active:bg-red-700 text-white text-3xl rounded-full w-20 h-20 shadow-lg focus:outline-none focus:ring-4 focus:ring-red-300 transition-all duration-150"
      @click="vote(false)"
    >
      &#10006;
    </button>

    <!-- Undo button -->
    <button
      class="bg-white hover:bg-gray-100 active:bg-gray-200 text-gray-700 text-2xl rounded-full w-14 h-14 shadow-lg focus:outline-none focus:ring-4 focus:ring-gray-300 transition-all duration-150 border border-gray-300"
      @click="undo"
      :disabled="!canUndo"
      :class="{ 'opacity-50 cursor-not-allowed': !canUndo }"
      title="Undo last vote"
    >
      ⟲
    </button>

    <button
      class="bg-green-500 hover:bg-green-600 active:bg-green-700 text-white text-3xl rounded-full w-20 h-20 shadow-lg focus:outline-none focus:ring-4 focus:ring-green-300 transition-all duration-150"
      @click="vote(true)"
    >
      &#10084;
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

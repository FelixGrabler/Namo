<template>
  <div
    class="flex justify-center gap-6 mt-6"
    @keydown="handleKeydown"
    tabindex="0"
  >
    <button
      class="bg-red-500 hover:bg-red-600 text-white text-2xl rounded-full w-16 h-16 shadow focus:outline-none focus:ring-2 focus:ring-red-400"
      @click="vote(false)"
    >
      &#10006;
    </button>

    <button
      class="bg-green-500 hover:bg-green-600 text-white text-2xl rounded-full w-16 h-16 shadow focus:outline-none focus:ring-2 focus:ring-green-400"
      @click="vote(true)"
    >
      &#10084;
    </button>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  (e: 'like'): void
  (e: 'dislike'): void
}>()

const vote = (isLike: boolean) => {
  if (isLike) {
    emit('like')
  } else {
    emit('dislike')
  }
}

const handleKeydown = (event: KeyboardEvent) => {
  switch (event.key) {
    case 'ArrowLeft':
    case 'ArrowDown':
      event.preventDefault()
      vote(false) // dislike
      break
    case 'ArrowRight':
    case 'ArrowUp':
      event.preventDefault()
      vote(true) // like
      break
  }
}
</script>

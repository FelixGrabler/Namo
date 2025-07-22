<template>
  <div class="flex justify-center gap-6 mt-6">
    <button
      class="bg-red-500 hover:bg-red-600 text-white text-2xl rounded-full w-16 h-16 shadow"
      @click="$emit('vote', false)"
    >
      &#10006;
    </button>

    <button
      class="bg-green-500 hover:bg-green-600 text-white text-2xl rounded-full w-16 h-16 shadow"
      @click="$emit('vote', true)"
    >
      &#10084;
    </button>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  (e: 'vote', value: boolean): void
}>()
</script>

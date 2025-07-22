<template>
  <div class="auth-view p-4 max-w-md mx-auto">
    <h1 class="text-xl font-bold mb-4">{{ isLoginMode ? 'Login' : 'Register' }}</h1>
    <form @submit.prevent="handleSubmit">
      <input
        v-model="username"
        type="text"
        placeholder="Username"
        class="mb-2 w-full p-2 border rounded"
        required
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="mb-4 w-full p-2 border rounded"
        required
      />
      <button
        type="submit"
        class="w-full bg-blue-500 text-white py-2 rounded mb-2 hover:bg-blue-600"
        :disabled="isLoading"
      >
        {{ isLoading ? 'Loading...' : (isLoginMode ? 'Login' : 'Register') }}
      </button>
      <button
        type="button"
        @click="toggleMode"
        class="w-full bg-gray-500 text-white py-2 rounded hover:bg-gray-600"
      >
        {{ isLoginMode ? 'Switch to Register' : 'Switch to Login' }}
      </button>
      <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import { useAuthService } from '@/api/authService'

const username = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)
const isLoginMode = ref(true)
const router = useRouter()
const userStore = useUserStore()
const authService = useAuthService()

const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value
  error.value = ''
}

const handleSubmit = async () => {
  error.value = ''
  isLoading.value = true

  try {
    const credentials = {
      username: username.value,
      password: password.value
    }

    const response = isLoginMode.value
      ? await authService.login(credentials)
      : await authService.register(credentials)

    userStore.setToken(response.access_token, username.value)
    router.push('/vote')
  } catch (err: any) {
    const errorMessage = err?.response?.data?.detail
    if (isLoginMode.value) {
      error.value = errorMessage || 'Login failed'
    } else {
      error.value = errorMessage || 'Registration failed'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-view {
  padding-top: 4rem;
}
</style>

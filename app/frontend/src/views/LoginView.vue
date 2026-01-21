<template>
  <div class="auth-view">
    <div class="auth-card">
      <div class="auth-header">
        <span class="auth-badge">{{ isLoginMode ? 'Willkommen zurueck' : 'Neu hier?' }}</span>
        <h1 class="auth-title">{{ isLoginMode ? 'Anmelden' : 'Konto erstellen' }}</h1>
        <p class="auth-subtitle">
          {{
            isLoginMode
              ? 'Melde dich an, um weiterzumachen.'
              : 'Konto erstellen, damit Namen gespeichert werden.'
          }}
        </p>
      </div>
      <form @submit.prevent="handleSubmit" class="auth-form">
        <label class="auth-label" for="username">Benutzername</label>
        <input
          id="username"
          v-model="username"
          type="text"
          placeholder="Dein Benutzername"
          class="auth-input"
          required
        />
        <label class="auth-label" for="password">Passwort</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="Dein Passwort"
          class="auth-input"
          required
        />
        <button type="submit" class="auth-submit" :disabled="isLoading">
          {{
            isLoading
              ? 'Lädt...'
              : (isLoginMode ? 'Login' : 'Registrieren')
          }}
        </button>
        <button type="button" class="auth-toggle" @click="toggleMode">
          {{
            isLoginMode
              ? 'Noch kein Konto? Registrieren'
              : 'Hast du bereits ein Konto? Login'
          }}
        </button>
        <p v-if="error" class="auth-error">{{ error }}</p>
      </form>
    </div>
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
const isLoginMode = ref(false)
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
      error.value = errorMessage || 'Login fehlgeschlagen'
    } else {
      error.value = errorMessage || 'Registrierung fehlgeschlagen'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
  background: radial-gradient(circle at top, #e0f2ff 0%, #ffe6f2 55%, #ffffff 100%);
}

.auth-card {
  width: min(26rem, 100%);
  background: #ffffff;
  border-radius: 24px;
  padding: 2.5rem 2rem;
  box-shadow: 0 24px 60px rgba(40, 55, 120, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.15);
  position: relative;
}

.auth-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 26px;
  background: linear-gradient(120deg, rgba(59, 130, 246, 0.35), rgba(236, 72, 153, 0.35));
  z-index: -1;
}

.auth-header {
  margin-bottom: 1.5rem;
  text-align: left;
}

.auth-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 700;
  color: #2563eb;
  background: rgba(59, 130, 246, 0.12);
  padding: 0.3rem 0.6rem;
  border-radius: 999px;
}

.auth-title {
  margin-top: 0.8rem;
  font-size: 2rem;
  line-height: 1.1;
  font-weight: 700;
  color: #0f172a;
}

.auth-subtitle {
  margin-top: 0.6rem;
  color: #475569;
  font-size: 0.98rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.auth-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #334155;
}

.auth-input {
  width: 100%;
  padding: 0.8rem 0.9rem;
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.5);
  font-size: 0.95rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.auth-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

.auth-submit {
  margin-top: 0.4rem;
  border: none;
  color: #ffffff;
  font-weight: 600;
  padding: 0.85rem 1rem;
  border-radius: 14px;
  background: linear-gradient(120deg, #3b82f6, #ec4899);
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.2s ease;
}

.auth-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.auth-submit:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 24px rgba(59, 130, 246, 0.25);
}

.auth-toggle {
  background: transparent;
  border: none;
  color: #2563eb;
  font-weight: 600;
  text-align: left;
  padding: 0.2rem 0;
  cursor: pointer;
}

.auth-toggle:hover {
  color: #db2777;
}

.auth-error {
  color: #dc2626;
  font-size: 0.9rem;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 2rem 1.5rem;
  }

  .auth-title {
    font-size: 1.7rem;
  }
}
</style>

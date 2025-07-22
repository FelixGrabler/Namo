import axios from 'axios'
import { useUserStore } from '@/stores/useUserStore'
import type { LoginRequest, RegisterRequest, AuthResponse } from '@/types'

export const useAuthService = () => {
  const userStore = useUserStore()

  const login = async (credentials: LoginRequest): Promise<AuthResponse> => {
    const response = await axios.post('/api/auth/login', credentials)
    return response.data
  }

  const register = async (credentials: RegisterRequest): Promise<AuthResponse> => {
    const response = await axios.post('/api/auth/register', credentials)
    return response.data
  }

  const logout = () => {
    userStore.logout()
  }

  return {
    login,
    register,
    logout
  }
}

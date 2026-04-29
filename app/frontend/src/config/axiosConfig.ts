import axios, { type AxiosResponse, type AxiosError } from 'axios'
import { useUserStore } from '@/stores/useUserStore'
import router from '@/router'

// Response interceptor to handle 401 errors globally
export const setupAxiosInterceptors = () => {
  axios.interceptors.response.use(
    (response: AxiosResponse) => {
      // If the response is successful, just return it
      return response
    },
    (error: AxiosError) => {
      if (error.response?.status === 401) {
        const userStore = useUserStore()
        const hadSession = userStore.isAuthenticated

        userStore.logout()

        if (hadSession && router.currentRoute.value.name !== 'Login') {
          router.push('/login')
          console.warn('Session expired. Please log in again.')
        }
      }

      // Re-throw the error so it can still be handled by the calling code if needed
      return Promise.reject(error)
    }
  )
}

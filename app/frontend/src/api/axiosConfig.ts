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
      // Handle 401 Unauthorized errors
      if (error.response?.status === 401) {
        // Get the user store
        const userStore = useUserStore()

        // Logout the user (clears token and localStorage)
        userStore.logout()

        // Redirect to login page
        router.push('/login')

        // Optional: Show a notification to the user
        console.warn('Session expired. Please log in again.')
      }

      // Re-throw the error so it can still be handled by the calling code if needed
      return Promise.reject(error)
    }
  )
}

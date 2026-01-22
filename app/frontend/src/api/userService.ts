import axios from 'axios'
import type { UserResponse } from '@/types'

export const useUserService = () => {
  const searchUsers = async (
    q = '',
    options?: {
      limit?: number;
      afterUsername?: string | null;
      afterId?: number | null;
    }
  ): Promise<UserResponse[]> => {
    const params: any = {
      q,
      limit: options?.limit ?? 20
    }

    if (options?.afterUsername) {
      params.after_username = options.afterUsername
    }

    if (options?.afterId) {
      params.after_id = options.afterId
    }

    const response = await axios.get('/api/auth/users/search', { params })
    return response.data
  }

  return {
    searchUsers
  }
}

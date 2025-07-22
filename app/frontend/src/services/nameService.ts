import axios from 'axios'
import type { NameResponse } from '@/types'

export const useNameService = () => {
  const getRandomNames = async (limit = 10): Promise<NameResponse[]> => {
    const response = await axios.get('/api/names/random', {
      params: { limit }
    })
    return response.data
  }

  return {
    getRandomNames,
  }
}

import axios from 'axios'
import type { NameResponse } from '@/types'

export const useNameService = () => {
  const getRandomNames = async (n = 10): Promise<NameResponse[]> => {
    const response = await axios.get('/api/names/random', {
      params: { n }
    })
    return response.data
  }

  return {
    getRandomNames,
  }
}

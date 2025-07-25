import axios from 'axios'
import type { NameResponse } from '@/types'
import type { SortOrder, Gender } from '@/stores/usePreferencesStore'

export const useNameService = () => {
  const getRandomNames = async (
    n = 10,
    options?: {
      sortOrder?: SortOrder;
      genders?: Gender[];
    }
  ): Promise<NameResponse[]> => {
    const params: any = { n }

    if (options?.sortOrder) {
      params.sort_order = options.sortOrder
    }

    if (options?.genders && options.genders.length > 0) {
      params.genders = options.genders.join(',')
    }

    const response = await axios.get('/api/names/random', {
      params
    })
    return response.data
  }

  return {
    getRandomNames,
  }
}

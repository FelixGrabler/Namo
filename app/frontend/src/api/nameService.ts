import axios from 'axios'
import type { NameResponse } from '@/types'
import type { SortOrder, Gender } from '@/stores/usePreferencesStore'

export const useNameService = () => {
  const getRandomNames = async (
    n = 10,
    options?: {
      sortOrder?: SortOrder;
      genders?: Gender[];
      source?: string;
      requireCount?: boolean;
      excludeVoted?: boolean;
    }
  ): Promise<NameResponse[]> => {
    const params: any = { n }

    if (options?.sortOrder) {
      params.sort_order = options.sortOrder
    }

    if (options?.genders && options.genders.length > 0) {
      params.genders = options.genders.join(',')
    }

    if (options?.source) {
      params.source = options.source
    }

    if (options?.requireCount) {
      params.require_count = true
    }

    if (options?.excludeVoted === false) {
      params.exclude_voted = false
    }

    const response = await axios.get('/api/names/random', {
      params
    })
    return response.data ?? []
  }

  const searchNames = async (
    q = '',
    options?: {
      limit?: number;
      afterName?: string | null;
      afterId?: number | null;
      source?: string;
    }
  ): Promise<NameResponse[]> => {
    const params: any = {
      q,
      limit: options?.limit ?? 20
    }

    if (options?.afterName) {
      params.after_name = options.afterName
    }

    if (options?.afterId) {
      params.after_id = options.afterId
    }

    if (options?.source) {
      params.source = options.source
    }

    const response = await axios.get('/api/names/search', { params })
    return response.data
  }

  const getNameInfo = async (name: string) => {
    const response = await axios.get(`/api/names/info/${encodeURIComponent(name)}`)
    return response.data
  }

  const getWordleTarget = async () => {
    const response = await axios.get('/api/names/wordle/random')
    return response.data
  }

  const validateWordle = async (name: string) => {
    const response = await axios.get('/api/names/wordle/validate', {
      params: { name }
    })
    return response.data
  }

  return {
    getRandomNames,
    searchNames,
    getNameInfo,
    getWordleTarget,
    validateWordle,
  }
}

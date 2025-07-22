src/services/voteService.ts

import axios from 'axios'
import type { VoteCreate } from '@/types'

export const useVoteService = () => {
  const submitVote = async (vote: VoteCreate) => {
    const response = await axios.post('/api/votes/', vote)
    return response.data
  }

  return { submitVote }
}

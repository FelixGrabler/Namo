import axios from 'axios'
import type { VoteCreate, VoteWithName } from '@/types'

export const useVoteService = () => {
  const submitVote = async (vote: VoteCreate) => {
    const response = await axios.post('/api/votes/', vote)
    return response.data
  }

  const getVotes = async (vote?: boolean, skip = 0, limit = 100): Promise<VoteWithName[]> => {
    const params: any = { skip, limit }
    if (vote !== undefined) {
      params.vote = vote
    }
    const response = await axios.get('/api/votes/', { params })
    return response.data
  }

  return {
    submitVote,
    getVotes
  }
}

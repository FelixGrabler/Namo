export interface NameResponse {
  id: number
  name: string
  source: string  // Changed from country to match backend
  gender: 'm' | 'f' | null  // Changed to lowercase and allow null
  rank: number | null
  count: number | null
}

export interface VoteCreate {
  name_id: number
  vote: boolean  // True = like, False = dislike
}

export interface VoteResponse {
  id: number
  name_id: number
  vote: boolean
}

export interface VoteWithName {
  id: number
  name_id: number
  vote: boolean
  name: NameResponse
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

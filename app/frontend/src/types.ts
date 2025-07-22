export interface NameResponse {
  id: number
  name: string
  country: string
  gender: 'M' | 'F'
  year: number
  popularity: number
}

export interface VoteCreate {
  name_id: number
  vote_type: 'like' | 'dislike'
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


export interface Participant {
  id: number
  full_name: string
  email: string
  phone: string
  is_verified: boolean
  is_winner: boolean
  created_at: string
}

export interface RegisterData {
  full_name: string
  email: string
  phone: string
}

export interface SetPasswordData {
  token: string
  password: string
  password_confirm: string
}

export interface AdminLoginData {
  username: string
  password: string
}

export interface LoginResponse {
  access: string
  refresh: string
}

export interface DrawWinnerResponse {
  message: string
  winner: Participant
}

export interface ApiResponse<T = any> {
  message?: string
  data?: T
}

export interface ApiError {
  message: string
  errors?: Record<string, string[]>
}

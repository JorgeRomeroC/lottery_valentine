// Interfaces para los participantes
export interface Participant {
  id: string
  email: string
  full_name: string
  phone: string
  is_verified: boolean
  status: string
  registered_at: string
  verified_at?: string
}

// Datos para el registro
export interface RegisterData {
  email: string
  full_name: string
  phone: string
  frontend_url: string
}

// Datos para verificar email
export interface VerifyEmailData {
  token: string
}

// Datos para crear contraseña
export interface SetPasswordData {
  token: string
  password: string
  password_confirm: string
}

// Datos para login de admin
export interface AdminLoginData {
  email: string
  password: string
}

// Respuesta del login
export interface LoginResponse {
  message: string
  access: string
  refresh: string
  user: {
    id: string
    email: string
    full_name: string
    is_staff: boolean
  }
}

// Ganador
export interface Winner {
  id: string
  participant: Participant
  winner_name: string
  winner_email: string
  draw_date: string
  is_notified: boolean
  notified_at?: string
  notes?: string
}

// Respuesta del sorteo
export interface DrawWinnerResponse {
  message: string
  winner: Winner
}

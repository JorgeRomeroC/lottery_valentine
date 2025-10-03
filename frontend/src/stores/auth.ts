import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/api/axios'
import type { AdminLoginData, LoginResponse } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('admin_token'))
  const isAuthenticated = ref<boolean>(!!token.value)

  // Login del administrador
  const login = async (credentials: AdminLoginData): Promise<void> => {
    try {
      const response = await apiClient.post<LoginResponse>('/users/admin/login/', credentials)
      token.value = response.data.access
      isAuthenticated.value = true
      localStorage.setItem('admin_token', response.data.access)
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Error al iniciar sesión')
    }
  }

  const logout = (): void => {
    token.value = null
    isAuthenticated.value = false
    localStorage.removeItem('admin_token')
  }

  const checkAuth = (): boolean => {
    const storedToken = localStorage.getItem('admin_token')
    if (storedToken) {
      token.value = storedToken
      isAuthenticated.value = true
      return true
    }
    return false
  }

  return {
    token,
    isAuthenticated,
    login,
    logout,
    checkAuth
  }
})

<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow">
          <div class="card-body p-5">
            <h2 class="text-center mb-4">
               Panel Administrador
            </h2>
            <p class="text-center text-muted mb-4">
              Acceso exclusivo para personal del hotel
            </p>

            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>

            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  :class="{ 'is-invalid': errors.email }"
                  id="email"
                  v-model="credentials.email"
                  @blur="validateEmail"
                  @input="errors.email = ''"
                  required
                  :disabled="loading"
                />
                <div v-if="errors.email" class="invalid-feedback">
                  {{ errors.email }}
                </div>
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Contraseña</label>
                <input
                  type="password"
                  class="form-control"
                  :class="{ 'is-invalid': errors.password }"
                  id="password"
                  v-model="credentials.password"
                  @blur="validatePassword"
                  @input="errors.password = ''"
                  required
                  :disabled="loading"
                />
                <div v-if="errors.password" class="invalid-feedback">
                  {{ errors.password }}
                </div>
              </div>

              <button
                type="submit"
                class="btn btn-dark w-100"
                :disabled="loading || hasErrors"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
              </button>
            </form>

            <div class="text-center mt-4">
              <a href="/" class="text-decoration-none text-muted">
                ← Volver a inscripción
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { AdminLoginData } from '@/types'

const router = useRouter()
const authStore = useAuthStore()

const credentials = ref<AdminLoginData>({
  email: '',
  password: ''
})

const errors = ref({
  email: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const validateEmail = () => {
  const email = credentials.value.email.trim()

  if (!email) {
    errors.value.email = 'El email es requerido'
    return false
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    errors.value.email = 'El formato del email no es válido'
    return false
  }

  errors.value.email = ''
  return true
}

const validatePassword = () => {
  const password = credentials.value.password

  if (!password) {
    errors.value.password = 'La contraseña es requerida'
    return false
  }

  if (password.length < 4) {
    errors.value.password = 'La contraseña debe tener al menos 4 caracteres'
    return false
  }

  errors.value.password = ''
  return true
}

const hasErrors = computed(() => {
  return !!(errors.value.email || errors.value.password)
})

const validateForm = (): boolean => {
  const emailValid = validateEmail()
  const passwordValid = validatePassword()
  return emailValid && passwordValid
}

const handleLogin = async () => {
  if (!validateForm()) {
    error.value = 'Por favor corrige los errores en el formulario'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await authStore.login(credentials.value)
    router.push({ name: 'admin-participants' })
  } catch (err: any) {
    error.value = err.message || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.card {
  border: none;
  border-radius: 15px;
}

.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  display: block;
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>

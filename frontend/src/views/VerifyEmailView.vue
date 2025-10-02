<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body p-5">
            <h2 class="text-center mb-4 text-danger">
              Verificación de Cuenta
            </h2>

            <div v-if="verifying" class="text-center">
              <div class="spinner-border text-danger mb-3" role="status">
                <span class="visually-hidden">Verificando...</span>
              </div>
              <p>Verificando tu correo electrónico...</p>
            </div>

            <div v-if="verificationError" class="alert alert-danger">
              {{ verificationError }}
            </div>

            <div v-if="verified && !passwordSet">
              <div class="alert alert-success mb-4">
                 Tu correo ha sido verificado correctamente
              </div>

              <p class="text-muted mb-4">
                Ahora crea tu contraseña para completar tu registro:
              </p>

              <form @submit.prevent="handleSetPassword">
                <div class="mb-3">
                  <label for="password" class="form-label">Contraseña *</label>
                  <input
                    type="password"
                    class="form-control"
                    :class="{ 'is-invalid': errors.password }"
                    id="password"
                    v-model="passwordData.password"
                    @blur="validatePassword"
                    @input="errors.password = ''"
                    required
                    :disabled="loading"
                  />
                  <small class="text-muted">Mínimo 8 caracteres</small>
                  <div v-if="errors.password" class="invalid-feedback">
                    {{ errors.password }}
                  </div>
                </div>

                <div class="mb-3">
                  <label for="password_confirm" class="form-label">
                    Confirmar Contraseña *
                  </label>
                  <input
                    type="password"
                    class="form-control"
                    :class="{ 'is-invalid': errors.password_confirm }"
                    id="password_confirm"
                    v-model="passwordData.password_confirm"
                    @blur="validatePasswordConfirm"
                    @input="errors.password_confirm = ''"
                    required
                    :disabled="loading"
                  />
                  <div v-if="errors.password_confirm" class="invalid-feedback">
                    {{ errors.password_confirm }}
                  </div>
                </div>

                <div v-if="error" class="alert alert-danger">
                  {{ error }}
                </div>

                <button
                  type="submit"
                  class="btn btn-danger w-100"
                  :disabled="loading || hasErrors"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Guardando...' : 'Crear Contraseña' }}
                </button>
              </form>
            </div>

            <div v-if="passwordSet" class="text-center">
              <div class="alert alert-success mb-4">
                <h4 class="alert-heading">🎉 ¡Felicitaciones!</h4>
                <p class="mb-0">
                  Tu cuenta ha sido activada.<br>
                  <strong>Ya estás participando en el sorteo de San Valentín.</strong>
                </p>
              </div>
              <p class="text-muted">
                Te notificaremos por correo si resultas ganador.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/api/axios'
import type { SetPasswordData, VerifyEmailData } from '@/types'

const route = useRoute()
const token = route.params.token as string

const verifying = ref(true)
const verified = ref(false)
const verificationError = ref('')
const passwordSet = ref(false)
const loading = ref(false)
const error = ref('')

const passwordData = ref<SetPasswordData>({
  token: token,
  password: '',
  password_confirm: ''
})

const errors = ref({
  password: '',
  password_confirm: ''
})

// Validación de contraseña
const validatePassword = () => {
  const password = passwordData.value.password

  if (!password) {
    errors.value.password = 'La contraseña es requerida'
    return false
  }

  if (password.length < 8) {
    errors.value.password = 'La contraseña debe tener al menos 8 caracteres'
    return false
  }

  if (password.length > 128) {
    errors.value.password = 'La contraseña es demasiado larga'
    return false
  }

  // Validar que tenga al menos una letra y un número (opcional pero recomendado)
  const hasLetter = /[a-zA-Z]/.test(password)
  const hasNumber = /[0-9]/.test(password)

  if (!hasLetter || !hasNumber) {
    errors.value.password = 'La contraseña debe contener letras y números'
    return false
  }

  errors.value.password = ''
  return true
}

// Validación de confirmación de contraseña
const validatePasswordConfirm = () => {
  const password = passwordData.value.password
  const passwordConfirm = passwordData.value.password_confirm

  if (!passwordConfirm) {
    errors.value.password_confirm = 'Debes confirmar la contraseña'
    return false
  }

  if (password !== passwordConfirm) {
    errors.value.password_confirm = 'Las contraseñas no coinciden'
    return false
  }

  errors.value.password_confirm = ''
  return true
}

const hasErrors = computed(() => {
  return !!(errors.value.password || errors.value.password_confirm)
})

const validateForm = (): boolean => {
  const passwordValid = validatePassword()
  const confirmValid = validatePasswordConfirm()
  return passwordValid && confirmValid
}

const verifyEmail = async () => {
  try {
    const verifyData: VerifyEmailData = { token }
    await apiClient.post('/users/verify-email/', verifyData)
    verified.value = true
    verificationError.value = ''
  } catch (err: any) {
    verificationError.value = err.response?.data?.error || 'Token inválido o expirado'
    verified.value = false
  } finally {
    verifying.value = false
  }
}

const handleSetPassword = async () => {
  if (!validateForm()) {
    error.value = 'Por favor corrige los errores en el formulario'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await apiClient.post('/users/set-password/', passwordData.value)
    passwordSet.value = true
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Error al crear la contraseña'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  verifyEmail()
})
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

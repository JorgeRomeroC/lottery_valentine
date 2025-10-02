<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body p-5">
            <h2 class="text-center mb-4 text-danger">
              Verificación de Cuenta
            </h2>

            <!-- Estado: Verificando -->
            <div v-if="verifying" class="text-center">
              <div class="spinner-border text-danger mb-3" role="status">
                <span class="visually-hidden">Verificando...</span>
              </div>
              <p>Verificando tu correo electrónico...</p>
            </div>

            <!-- Estado: Error de verificación -->
            <div v-if="verificationError" class="alert alert-danger">
              {{ verificationError }}
            </div>

            <!-- Estado: Verificado - Formulario de contraseña -->
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
                    id="password"
                    v-model="passwordData.password"
                    required
                    minlength="8"
                    :disabled="loading"
                  />
                  <small class="text-muted">Mínimo 8 caracteres</small>
                </div>

                <div class="mb-3">
                  <label for="password_confirm" class="form-label">
                    Confirmar Contraseña *
                  </label>
                  <input
                    type="password"
                    class="form-control"
                    id="password_confirm"
                    v-model="passwordData.password_confirm"
                    required
                    minlength="8"
                    :disabled="loading"
                  />
                </div>

                <div v-if="error" class="alert alert-danger">
                  {{ error }}
                </div>

                <button
                  type="submit"
                  class="btn btn-danger w-100"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Guardando...' : 'Crear Contraseña' }}
                </button>
              </form>
            </div>

            <!-- Estado: Contraseña creada exitosamente -->
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/api/axios'
import type { SetPasswordData } from '@/types'

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

// Verificar el email al cargar el componente
const verifyEmail = async () => {
  try {
    await apiClient.get(`/participants/verify-email/${token}/`)
    verified.value = true
    verificationError.value = ''
  } catch (err: any) {
    verificationError.value = err.response?.data?.error || 'Token inválido o expirado'
    verified.value = false
  } finally {
    verifying.value = false
  }
}

// Crear contraseña
const handleSetPassword = async () => {
  if (passwordData.value.password !== passwordData.value.password_confirm) {
    error.value = 'Las contraseñas no coinciden'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await apiClient.post('/participants/set-password/', passwordData.value)
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
</style>

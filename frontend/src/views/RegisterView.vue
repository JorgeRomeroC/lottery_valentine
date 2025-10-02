<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body p-5">
            <h2 class="text-center mb-4 text-danger">
               Sorteo San Valentín
            </h2>
            <p class="text-center text-muted mb-4">
              ¡Gana 2 noches todo pagado para una pareja en un hotel!
            </p>

            <!-- Mensaje de éxito -->
            <div v-if="success" class="alert alert-success" role="alert">
              <strong>¡Gracias por registrarte!</strong><br>
              Revisa tu correo para verificar tu cuenta.
            </div>

            <!-- Mensaje de error -->
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>

            <!-- Formulario de inscripción -->
            <form v-if="!success" @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="full_name" class="form-label">Nombre Completo *</label>
                <input
                  type="text"
                  class="form-control"
                  id="full_name"
                  v-model="formData.full_name"
                  required
                  :disabled="loading"
                />
              </div>

              <div class="mb-3">
                <label for="email" class="form-label">Correo Electrónico *</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="formData.email"
                  required
                  :disabled="loading"
                />
              </div>

              <div class="mb-3">
                <label for="phone" class="form-label">Teléfono *</label>
                <input
                  type="tel"
                  class="form-control"
                  id="phone"
                  v-model="formData.phone"
                  required
                  placeholder="+56912345678"
                  :disabled="loading"
                />
              </div>

              <button
                type="submit"
                class="btn btn-danger w-100"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Registrando...' : 'Inscribirme al Sorteo' }}
              </button>
            </form>

            <div v-if="success" class="text-center mt-4">
              <button class="btn btn-outline-danger" @click="resetForm">
                Registrar otro participante
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import apiClient from '@/api/axios'
import type { RegisterData } from '@/types'

const formData = ref<RegisterData>({
  full_name: '',
  email: '',
  phone: ''
})

const loading = ref(false)
const success = ref(false)
const error = ref('')

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    await apiClient.post('/participants/register/', formData.value)
    success.value = true
  } catch (err: any) {
    if (err.response?.data?.error) {
      error.value = err.response.data.error
    } else if (err.response?.data?.email) {
      error.value = err.response.data.email[0]
    } else {
      error.value = 'Error al registrarse. Intenta nuevamente.'
    }
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.value = {
    full_name: '',
    email: '',
    phone: ''
  }
  success.value = false
  error.value = ''
}
</script>

<style scoped>
.card {
  border: none;
  border-radius: 15px;
}
</style>

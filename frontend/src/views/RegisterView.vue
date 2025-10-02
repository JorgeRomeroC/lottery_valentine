<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body p-5">
            <h2 class="text-center mb-4 text-danger">
              🌹 Sorteo San Valentín 🌹
            </h2>
            <p class="text-center text-muted mb-4">
              ¡Gana 2 noches todo pagado para una pareja en un hotel!
            </p>

            <div v-if="success" class="alert alert-success" role="alert">
              <strong>¡Gracias por registrarte!</strong><br>
              Revisa tu correo para verificar tu cuenta.
            </div>

            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>

            <form v-if="!success" @submit.prevent="handleSubmit">
              <!-- Nombre Completo -->
              <div class="mb-3">
                <label for="full_name" class="form-label">Nombre Completo *</label>
                <input
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': errors.full_name }"
                  id="full_name"
                  v-model="formData.full_name"
                  @blur="validateFullName"
                  @input="errors.full_name = ''"
                  required
                  :disabled="loading"
                />
                <div v-if="errors.full_name" class="invalid-feedback">
                  {{ errors.full_name }}
                </div>
              </div>

              <!-- Email -->
              <div class="mb-3">
                <label for="email" class="form-label">Correo Electrónico *</label>
                <input
                  type="email"
                  class="form-control"
                  :class="{ 'is-invalid': errors.email }"
                  id="email"
                  v-model="formData.email"
                  @blur="validateEmail"
                  @input="errors.email = ''"
                  required
                  :disabled="loading"
                />
                <div v-if="errors.email" class="invalid-feedback">
                  {{ errors.email }}
                </div>
              </div>

              <!-- Teléfono -->
              <div class="mb-3">
                <label for="phone" class="form-label">Teléfono *</label>
                <input
                  type="tel"
                  class="form-control"
                  :class="{ 'is-invalid': errors.phone }"
                  id="phone"
                  v-model="formData.phone"
                  @blur="validatePhone"
                  @input="errors.phone = ''"
                  required
                  placeholder="+56912345678"
                  :disabled="loading"
                />
                <small class="text-muted">Formato: +56912345678</small>
                <div v-if="errors.phone" class="invalid-feedback">
                  {{ errors.phone }}
                </div>
              </div>

              <button
                type="submit"
                class="btn btn-danger w-100"
                :disabled="loading || hasErrors"
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
import { ref, computed } from 'vue'
import apiClient from '@/api/axios'
import type { RegisterData } from '@/types'

const formData = ref<RegisterData>({
  full_name: '',
  email: '',
  phone: '',
  frontend_url: 'http://localhost:5173'
})

const errors = ref({
  full_name: '',
  email: '',
  phone: ''
})

const loading = ref(false)
const success = ref(false)
const error = ref('')

// Validación de nombre completo
const validateFullName = () => {
  const name = formData.value.full_name.trim()

  if (!name) {
    errors.value.full_name = 'El nombre es requerido'
    return false
  }

  if (name.length < 3) {
    errors.value.full_name = 'El nombre debe tener al menos 3 caracteres'
    return false
  }

  if (name.length > 100) {
    errors.value.full_name = 'El nombre es demasiado largo'
    return false
  }

  const nameRegex = /^[a-záéíóúñA-ZÁÉÍÓÚÑ\s]+$/
  if (!nameRegex.test(name)) {
    errors.value.full_name = 'El nombre solo puede contener letras'
    return false
  }

  errors.value.full_name = ''
  return true
}

// Validación de email
const validateEmail = () => {
  const email = formData.value.email.trim()

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

// Validación de teléfono
const validatePhone = () => {
  const phone = formData.value.phone.trim()

  if (!phone) {
    errors.value.phone = 'El teléfono es requerido'
    return false
  }

  const phoneRegex = /^\+56[2-9]\d{8}$/
  if (!phoneRegex.test(phone)) {
    errors.value.phone = 'El teléfono debe tener formato chileno: +56912345678'
    return false
  }

  errors.value.phone = ''
  return true
}

// Computed para verificar si hay errores
const hasErrors = computed(() => {
  return !!(errors.value.full_name || errors.value.email || errors.value.phone)
})

const validateForm = (): boolean => {
  const nameValid = validateFullName()
  const emailValid = validateEmail()
  const phoneValid = validatePhone()

  return nameValid && emailValid && phoneValid
}

const handleSubmit = async () => {
  // Validar antes de enviar
  if (!validateForm()) {
    error.value = 'Por favor corrige los errores en el formulario'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await apiClient.post('/users/register/', formData.value)
    success.value = true
  } catch (err: any) {
    if (err.response?.data?.error) {
      error.value = err.response.data.error
    } else if (err.response?.data?.email) {
      error.value = err.response.data.email[0]
    } else if (err.response?.data?.full_name) {
      errors.value.full_name = err.response.data.full_name[0]
    } else if (err.response?.data?.phone) {
      errors.value.phone = err.response.data.phone[0]
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
    phone: '',
    frontend_url: 'http://localhost:5173'
  }
  errors.value = {
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

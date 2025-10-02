<template>
  <div class="container-fluid py-4">
    <!-- Navbar de administrador -->
    <nav class="navbar navbar-dark bg-dark rounded mb-4">
      <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">Panel de Administración</span>
        <div class="d-flex">
          <router-link to="/admin/participants" class="btn btn-outline-light me-2">
             Ver Participantes
          </router-link>
          <button class="btn btn-outline-light" @click="handleLogout">
            Cerrar Sesión
          </button>
        </div>
      </div>
    </nav>

    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body p-5 text-center">
            <h2 class="mb-4"> Sorteo de San Valentín</h2>
            <p class="text-muted mb-4">
              Selecciona aleatoriamente un ganador entre todos los participantes verificados
            </p>

            <!-- Mensaje de error -->
            <div v-if="error" class="alert alert-danger">
              {{ error }}
            </div>

            <!-- Estado: Sin sortear -->
            <div v-if="!winner && !loading">
              <div class="alert alert-info mb-4">
                <strong>️ Información:</strong><br>
                El sorteo seleccionará automáticamente un participante verificado<br>
                y le enviará un correo de notificación.
              </div>

              <button
                class="btn btn-danger btn-lg px-5"
                @click="drawWinner"
              >
                 Realizar Sorteo
              </button>
            </div>

            <!-- Estado: Sorteando -->
            <div v-if="loading" class="py-5">
              <div class="spinner-border text-danger mb-3" style="width: 4rem; height: 4rem;" role="status">
                <span class="visually-hidden">Sorteando...</span>
              </div>
              <h4 class="text-danger">Sorteando ganador...</h4>
              <p class="text-muted">Seleccionando participante aleatorio</p>
            </div>

            <!-- Estado: Ganador seleccionado -->
            <div v-if="winner && !loading" class="py-4">
              <div class="alert alert-success mb-4">
                <h3 class="alert-heading">🎉 ¡Tenemos un ganador!</h3>
              </div>

              <div class="card bg-light border-danger border-3 mb-4">
                <div class="card-body p-4">
                  <h4 class="text-danger mb-3">🏆 Ganador:</h4>
                  <h3 class="mb-3">{{ winner.full_name }}</h3>
                  <p class="mb-2">
                    <strong>Email:</strong> {{ winner.email }}
                  </p>
                  <p class="mb-0">
                    <strong>Teléfono:</strong> {{ winner.phone }}
                  </p>
                </div>
              </div>

              <div class="alert alert-info">
                 Se ha enviado un correo de notificación al ganador
              </div>

              <button
                class="btn btn-outline-danger mt-3"
                @click="resetDraw"
              >
                Realizar otro sorteo
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api/axios'
import type { Participant } from '@/types'

const router = useRouter()
const authStore = useAuthStore()

const winner = ref<Participant | null>(null)
const loading = ref(false)
const error = ref('')

// Realizar sorteo
const drawWinner = async () => {
  loading.value = true
  error.value = ''
  winner.value = null

  try {
    const response = await apiClient.post('/admin/draw-winner/')

    // Simular efecto de "sorteando" por 2 segundos
    setTimeout(() => {
      winner.value = response.data.winner
      loading.value = false
    }, 2000)
  } catch (err: any) {
    loading.value = false
    if (err.response?.data?.error) {
      error.value = err.response.data.error
    } else {
      error.value = 'Error al realizar el sorteo'
    }
  }
}

// Resetear sorteo
const resetDraw = () => {
  winner.value = null
  error.value = ''
}

// Cerrar sesión
const handleLogout = () => {
  authStore.logout()
  router.push({ name: 'admin-login' })
}
</script>

<style scoped>
.card {
  border: none;
  border-radius: 15px;
}
</style>

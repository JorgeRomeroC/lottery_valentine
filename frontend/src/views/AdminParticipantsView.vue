<template>
  <div class="container-fluid py-4">
    <!-- Navbar de administrador -->
    <nav class="navbar navbar-dark bg-dark rounded mb-4">
      <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">Panel de Administración</span>
        <div class="d-flex">
          <router-link to="/admin/draw" class="btn btn-danger me-2">
             Sortear Ganador
          </router-link>
          <button class="btn btn-outline-light" @click="handleLogout">
            Cerrar Sesión
          </button>
        </div>
      </div>
    </nav>

    <div class="card shadow">
      <div class="card-header bg-white py-3">
        <h4 class="mb-0">Lista de Participantes</h4>
      </div>
      <div class="card-body">
        <!-- Barra de búsqueda -->
        <div class="row mb-3">
          <div class="col-md-6">
            <input
              type="text"
              class="form-control"
              placeholder="Buscar por nombre o email..."
              v-model="searchQuery"
              @input="filterParticipants"
            />
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filterStatus" @change="filterParticipants">
              <option value="all">Todos</option>
              <option value="verified">Verificados</option>
              <option value="not_verified">No verificados</option>
            </select>
          </div>
          <div class="col-md-3 text-end">
            <button class="btn btn-primary" @click="loadParticipants">
               Actualizar
            </button>
          </div>
        </div>

        <!-- Estado de carga -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
        </div>

        <!-- Mensaje de error -->
        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <!-- Tabla de participantes -->
        <div v-if="!loading && !error" class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Nombre Completo</th>
                <th>Email</th>
                <th>Teléfono</th>
                <th>Estado</th>
                <th>Ganador</th>
                <th>Fecha de Registro</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="participant in filteredParticipants" :key="participant.id">
                <td>{{ participant.id }}</td>
                <td>{{ participant.full_name }}</td>
                <td>{{ participant.email }}</td>
                <td>{{ participant.phone }}</td>
                <td>
                  <span
                    class="badge"
                    :class="participant.is_verified ? 'bg-success' : 'bg-warning text-dark'"
                  >
                    {{ participant.is_verified ? '✓ Verificado' : ' Pendiente' }}
                  </span>
                </td>
                <td>
                  <span v-if="participant.is_winner" class="badge bg-danger">
                     GANADOR
                  </span>
                  <span v-else class="text-muted">-</span>
                </td>
                <td>{{ formatDate(participant.created_at) }}</td>
              </tr>
            </tbody>
          </table>

          <!-- Sin resultados -->
          <div v-if="filteredParticipants.length === 0" class="text-center py-4 text-muted">
            No se encontraron participantes
          </div>

          <!-- Total de participantes -->
          <div class="mt-3 text-muted">
            Total: {{ filteredParticipants.length }} participante(s)
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api/axios'
import type { Participant } from '@/types'

const router = useRouter()
const authStore = useAuthStore()

const participants = ref<Participant[]>([])
const filteredParticipants = ref<Participant[]>([])
const loading = ref(false)
const error = ref('')
const searchQuery = ref('')
const filterStatus = ref('all')

// Cargar participantes
const loadParticipants = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await apiClient.get('/admin/participants/')
    participants.value = response.data
    filteredParticipants.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al cargar participantes'
  } finally {
    loading.value = false
  }
}

// Filtrar participantes
const filterParticipants = () => {
  let filtered = [...participants.value]

  // Filtrar por búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(
      (p) =>
        p.full_name.toLowerCase().includes(query) ||
        p.email.toLowerCase().includes(query)
    )
  }

  // Filtrar por estado
  if (filterStatus.value === 'verified') {
    filtered = filtered.filter((p) => p.is_verified)
  } else if (filterStatus.value === 'not_verified') {
    filtered = filtered.filter((p) => !p.is_verified)
  }

  filteredParticipants.value = filtered
}

// Formatear fecha
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleString('es-CL', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Cerrar sesión
const handleLogout = () => {
  authStore.logout()
  router.push({ name: 'admin-login' })
}

onMounted(() => {
  loadParticipants()
})
</script>

<style scoped>
.table {
  font-size: 0.9rem;
}
</style>

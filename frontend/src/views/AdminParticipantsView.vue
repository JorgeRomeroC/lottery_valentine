<template>
  <div class="container-fluid py-4">
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
              <option value="pending">Pendientes</option>
            </select>
          </div>
          <div class="col-md-3 text-end">
            <button class="btn btn-primary" @click="loadParticipants">
               Actualizar
            </button>
          </div>
        </div>

        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
        </div>

        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <div v-if="!loading && !error" class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Nombre Completo</th>
                <th>Email</th>
                <th>Teléfono</th>
                <th>Estado</th>
                <th>Fecha de Registro</th>
                <th>Fecha de Verificación</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="participant in filteredParticipants" :key="participant.id">
                <td>{{ participant.full_name }}</td>
                <td>{{ participant.email }}</td>
                <td>{{ participant.phone }}</td>
                <td>
                  <span
                    class="badge"
                    :class="participant.status === 'verified' ? 'bg-success' : 'bg-warning text-dark'"
                  >
                    {{ participant.status === 'verified' ? '✓ Verificado' : '⏳ Pendiente' }}
                  </span>
                </td>
                <td>{{ formatDate(participant.registered_at) }}</td>
                <td>{{ participant.verified_at ? formatDate(participant.verified_at) : '-' }}</td>
              </tr>
            </tbody>
          </table>

          <div v-if="filteredParticipants.length === 0" class="text-center py-4 text-muted">
            No se encontraron participantes
          </div>

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

const loadParticipants = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await apiClient.get('/contest/participants/')
    participants.value = response.data.results || response.data
    filteredParticipants.value = participants.value
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al cargar participantes'
  } finally {
    loading.value = false
  }
}

const filterParticipants = () => {
  let filtered = [...participants.value]

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(
      (p) =>
        p.full_name.toLowerCase().includes(query) ||
        p.email.toLowerCase().includes(query)
    )
  }

  if (filterStatus.value === 'verified') {
    filtered = filtered.filter((p) => p.status === 'verified')
  } else if (filterStatus.value === 'pending') {
    filtered = filtered.filter((p) => p.status === 'pending')
  }

  filteredParticipants.value = filtered
}

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

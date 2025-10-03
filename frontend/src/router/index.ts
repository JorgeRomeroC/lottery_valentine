import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { title: 'Inscripción al Sorteo' }
    },
    {
      path: '/verify-email/:token',
      name: 'verify-email',
      component: () => import('@/views/VerifyEmailView.vue'),
      meta: { title: 'Verificar Email' }
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('@/views/AdminLoginView.vue'),
      meta: { title: 'Login Administrador' }
    },
    {
      path: '/admin/participants',
      name: 'admin-participants',
      component: () => import('@/views/AdminParticipantsView.vue'),
      meta: { title: 'Lista de Participantes', requiresAuth: true }
    },
    {
      path: '/admin/draw',
      name: 'admin-draw',
      component: () => import('@/views/AdminDrawView.vue'),
      meta: { title: 'Sorteo de Ganador', requiresAuth: true }
    }
  ]
})

// Guard para rutas protegidas
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'admin-login' })
  } else {
    next()
  }
})

export default router

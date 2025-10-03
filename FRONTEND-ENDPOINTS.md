# 🎨 API Frontend - Sorteo San Valentín

## Configuración

**Backend API:** `http://127.0.0.1:8000/api`  
**Frontend:** `http://localhost:5173`

---

## Rutas y Endpoints

### 1. Página de Inscripción

**Ruta Frontend:** `/`  
**Componente:** `RegisterView.vue`  
**Acceso:** Público

**API Call:**
```typescript
POST /api/users/register/

Request Body:
{
  "full_name": "Juan Pérez",
  "email": "usuario@example.com",
  "phone": "+56912345678",
  "frontend_url": "http://localhost:5173"
}

Response (201):
{
  "message": "¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.",
  "email": "usuario@example.com"
}

Response Error (400):
{
  "email": ["Este correo electrónico ya está registrado."],
  "full_name": ["El nombre debe tener al menos 3 caracteres"],
  "phone": ["El teléfono debe tener formato chileno: +56912345678"]
}
```

---

### 2. Verificación de Email y Creación de Contraseña

**Ruta Frontend:** `/verify-email/:token`  
**Componente:** `VerifyEmailView.vue`  
**Acceso:** Público (con token válido)

**API Calls:**

**2.1 Verificar Token:**
```typescript
POST /api/users/verify-email/

Request Body:
{
  "token": "uuid-del-email"
}

Response (200):
{
  "message": "Token válido. Ahora puedes establecer tu contraseña.",
  "email": "usuario@example.com",
  "full_name": "Juan Pérez"
}

Response Error (400):
{
  "error": "Token inválido o ya fue utilizado"
}
```

**2.2 Establecer Contraseña:**
```typescript
POST /api/users/set-password/

Request Body:
{
  "token": "uuid-del-email",
  "password": "MiPassword123",
  "password_confirm": "MiPassword123"
}

Response (200):
{
  "message": "Tu cuenta ha sido activada. Ya estás participando en el sorteo."
}

Response Error (400):
{
  "error": "Las contraseñas no coinciden",
  "password": ["La contraseña debe tener al menos 8 caracteres"]
}
```

---

### 3. Login de Administrador

**Ruta Frontend:** `/admin/login`  
**Componente:** `AdminLoginView.vue`  
**Acceso:** Público

**API Call:**
```typescript
POST /api/users/admin/login/

Request Body:
{
  "email": "admin@ctsturismo.cl",
  "password": "password123"
}

Response (200):
{
  "message": "Login exitoso",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "email": "admin@ctsturismo.cl",
    "full_name": "Administrador",
    "is_staff": true
  }
}

Response Error (401):
{
  "error": "Credenciales inválidas"
}

Response Error (403):
{
  "error": "No tienes permisos de administrador"
}
```

---

### 4. Lista de Participantes

**Ruta Frontend:** `/admin/participants`  
**Componente:** `AdminParticipantsView.vue`  
**Acceso:** Protegido (requiere token JWT)

**API Call:**
```typescript
GET /api/contest/participants/

Headers:
{
  "Authorization": "Bearer <access_token>"
}

Query Params (opcionales):
- search: string (busca en nombre/email)
- status: 'verified' | 'pending' | 'all'

Response (200):
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/contest/participants/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "email": "usuario@example.com",
      "full_name": "Juan Pérez",
      "phone": "+56912345678",
      "status": "verified",
      "is_verified": true,
      "registered_at": "2025-10-02T10:00:00Z",
      "verified_at": "2025-10-02T10:05:00Z"
    }
  ]
}

Response Error (401):
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 5. Sorteo de Ganador

**Ruta Frontend:** `/admin/draw`  
**Componente:** `AdminDrawView.vue`  
**Acceso:** Protegido (requiere token JWT)

**API Call:**
```typescript
POST /api/contest/draw-winner/

Headers:
{
  "Authorization": "Bearer <access_token>"
}

Request Body: {} (vacío)

Response (201):
{
  "message": "¡Ganador seleccionado exitosamente!",
  "winner": {
    "id": "uuid",
    "winner_name": "María González",
    "winner_email": "ganador@example.com",
    "draw_date": "2025-10-02T10:20:00Z",
    "is_notified": true,
    "notified_at": "2025-10-02T10:20:01Z"
  }
}

Response Error (400):
{
  "error": "No hay participantes verificados para el sorteo"
}

Response Error (401):
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Tipos TypeScript

```typescript
interface Participant {
  id: string
  email: string
  full_name: string
  phone: string
  status: 'pending' | 'verified' | 'rejected'
  is_verified: boolean
  registered_at: string
  verified_at?: string
}

interface RegisterData {
  email: string
  full_name: string
  phone: string
  frontend_url: string
}

interface SetPasswordData {
  token: string
  password: string
  password_confirm: string
}

interface AdminLoginData {
  email: string
  password: string
}

interface LoginResponse {
  message: string
  access: string
  refresh: string
  user: {
    id: string
    email: string
    full_name: string
    is_staff: boolean
  }
}

interface Winner {
  id: string
  winner_name: string
  winner_email: string
  draw_date: string
  is_notified: boolean
  notified_at?: string
}
```

---

## Autenticación

**Token Storage:** `localStorage.getItem('admin_token')`

**Header Authorization:**
```typescript
Authorization: Bearer <access_token>
```

**Rutas Protegidas:**
- `/admin/participants` - Requiere token
- `/admin/draw` - Requiere token

**Guard de Router:**
```typescript
if (to.meta.requiresAuth && !authStore.isAuthenticated) {
  next({ name: 'admin-login' })
}
```

---

## Códigos de Estado HTTP

- `200` - Éxito (GET)
- `201` - Recurso creado (POST)
- `400` - Error de validación
- `401` - No autenticado
- `403` - Sin permisos
- `404` - No encontrado
- `500` - Error del servidor

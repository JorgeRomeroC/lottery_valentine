# 🧪 Pruebas del Backend - Sorteo San Valentín

## 📋 Configuración Inicial

**Base URL:** `http://127.0.0.1:8000`

---

## 1️⃣ ENDPOINTS PÚBLICOS (Sin autenticación)

### 1.1 Registro de Usuario

**Endpoint:** `POST /api/users/register/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "usuario1@example.com",
  "full_name": "Juan Pérez",
  "phone": "+56912345678",
  "frontend_url": "http://localhost:5173"
}
```

**Respuesta esperada (201):**
```json
{
  "message": "¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.",
  "email": "usuario1@example.com"
}
```

**⚠️ Nota:** Se enviará un email a Mailtrap con el token de verificación.

---

### 1.2 Verificar Email (Paso 1: Validar Token)

**Endpoint:** `POST /api/users/verify-email/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "token": "el-token-uuid-que-llegó-por-email"
}
```

**Respuesta esperada (200):**
```json
{
  "message": "Token válido. Ahora puedes establecer tu contraseña.",
  "email": "usuario1@example.com",
  "full_name": "Juan Pérez"
}
```

**⚠️ Obtener el token:** Ve a Mailtrap y copia el UUID del enlace de verificación.

---

### 1.3 Establecer Contraseña (Paso 2: Activar Cuenta)

**Endpoint:** `POST /api/users/set-password/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "token": "el-mismo-token-uuid-anterior",
  "password": "MiPassword123!",
  "password_confirm": "MiPassword123!"
}
```

**Respuesta esperada (200):**
```json
{
  "message": "Tu cuenta ha sido activada. Ya estás participando en el sorteo."
}
```

**✅ El usuario ya está participando oficialmente en el sorteo.**

---

### 1.4 Login de Administrador

**Endpoint:** `POST /api/users/admin/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "admin@ctsturismo.cl",
  "password": "tu-password-de-superusuario"
}
```

**Respuesta esperada (200):**
```json
{
  "message": "Login exitoso",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid-del-admin",
    "email": "admin@ctsturismo.cl",
    "full_name": "Administrador",
    "is_staff": true
  }
}
```

**⚠️ Guarda el `access` token para los siguientes requests.**

---

## 2️⃣ ENDPOINTS PROTEGIDOS (Requieren autenticación de Admin)

**⚠️ Para todos estos endpoints, agrega el header:**
```
Authorization: Bearer TU_ACCESS_TOKEN_AQUI
```

---

### 2.1 Perfil del Administrador

**Endpoint:** `GET /api/users/admin/profile/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta esperada (200):**
```json
{
  "id": "uuid",
  "email": "admin@ctsturismo.cl",
  "full_name": "Administrador",
  "phone": "+56912345678",
  "is_verified": true,
  "date_joined": "2025-10-02T10:00:00Z"
}
```

---

### 2.2 Lista de Participantes

**Endpoint:** `GET /api/contest/participants/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Query Parameters (opcionales):**
- `search=juan` - Buscar por nombre, email o teléfono
- `status=verified` - Filtrar por estado (pending, verified, rejected)
- `is_verified=true` - Filtrar por email verificado
- `page=1` - Paginación

**Ejemplo completo:**
```
GET /api/contest/participants/?search=juan&status=verified&page=1
```

**Respuesta esperada (200):**
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/contest/participants/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "email": "usuario1@example.com",
      "full_name": "Juan Pérez",
      "phone": "+56912345678",
      "status": "verified",
      "is_verified": true,
      "registered_at": "2025-10-02T10:00:00Z",
      "verified_at": "2025-10-02T10:05:00Z"
    }
  ]
}
```

---

### 2.3 Estadísticas de Participantes

**Endpoint:** `GET /api/contest/participants/stats/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta esperada (200):**
```json
{
  "total_participants": 150,
  "verified_participants": 120,
  "pending_participants": 30,
  "eligible_for_draw": 120
}
```

---

### 2.4 Realizar Sorteo (Seleccionar Ganador)

**Endpoint:** `POST /api/contest/draw-winner/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json
```

**Body:** (vacío o {})

**Respuesta esperada (201):**
```json
{
  "message": "¡Ganador seleccionado exitosamente!",
  "winner": {
    "id": "uuid-del-ganador",
    "participant": {
      "id": "uuid",
      "user": {
        "id": "uuid",
        "email": "ganador@example.com",
        "full_name": "María González",
        "phone": "+56987654321",
        "is_verified": true,
        "date_joined": "2025-10-01T15:30:00Z"
      },
      "status": "verified",
      "registered_at": "2025-10-01T15:30:00Z",
      "verified_at": "2025-10-01T15:35:00Z"
    },
    "winner_name": "María González",
    "winner_email": "ganador@example.com",
    "draw_date": "2025-10-02T10:20:00Z",
    "is_notified": true,
    "notified_at": "2025-10-02T10:20:01Z",
    "notes": null
  }
}
```

**✅ Se enviará automáticamente un email al ganador vía Celery.**

---

### 2.5 Obtener Último Ganador

**Endpoint:** `GET /api/contest/latest-winner/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta esperada (200):**
```json
{
  "id": "uuid",
  "participant": { ... },
  "winner_name": "María González",
  "winner_email": "ganador@example.com",
  "draw_date": "2025-10-02T10:20:00Z",
  "is_notified": true,
  "notified_at": "2025-10-02T10:20:01Z",
  "notes": null
}
```

---

### 2.6 Lista de Ganadores

**Endpoint:** `GET /api/contest/winners/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta esperada (200):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "participant": { ... },
      "winner_name": "María González",
      "winner_email": "ganador@example.com",
      "draw_date": "2025-10-02T10:20:00Z",
      "is_notified": true,
      "notified_at": "2025-10-02T10:20:01Z",
      "notes": null
    }
  ]
}
```

---

### 2.7 Refrescar Token JWT

**Endpoint:** `POST /api/users/admin/token/refresh/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "refresh": "tu-refresh-token-aqui"
}
```

**Respuesta esperada (200):**
```json
{
  "access": "nuevo-access-token"
}
```

---

## 🧪 Flujo de Prueba Completo

### Paso 1: Registrar un usuario
```
POST /api/users/register/
```

### Paso 2: Revisar Mailtrap
Ve a tu inbox de Mailtrap y copia el token UUID del email.

### Paso 3: Verificar email
```
POST /api/users/verify-email/
```

### Paso 4: Establecer contraseña
```
POST /api/users/set-password/
```

### Paso 5: Login como admin
```
POST /api/users/admin/login/
```

### Paso 6: Ver participantes
```
GET /api/contest/participants/
```

### Paso 7: Ver estadísticas
```
GET /api/contest/participants/stats/
```

### Paso 8: Realizar sorteo
```
POST /api/contest/draw-winner/
```

### Paso 9: Revisar email del ganador en Mailtrap

---

## 📝 Notas Importantes

1. **Crear superusuario** primero: `python manage.py createsuperuser`
2. **Mailtrap:** Todos los emails se capturan en Mailtrap (no se envían realmente)
3. **JWT Tokens:** Duran 60 minutos (configurable en .env)
4. **Celery:** Debe estar corriendo para que se envíen los emails
5. **Redis:** Debe estar corriendo para que funcione Celery

---

## ❌ Errores Comunes

**401 Unauthorized:** El token JWT expiró o es inválido
**403 Forbidden:** El usuario no tiene permisos de admin
**400 Bad Request:** Revisa el formato del JSON o campos requeridos
**404 Not Found:** La URL es incorrecta o el recurso no existe

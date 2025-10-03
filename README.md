#  Sorteo San Valentín - Sistema de Gestión de Concursos


## 👨‍💻 Desarrollado por

**Jorge Romero Contreras**  
Programador y Desarrollador Web especializado en Django, Flask y Vue.js, PHP, Laravel

🌐 **Web:** [deverom.com](https://deverom.com)  
💼 **LinkedIn:** [https://www.linkedin.com/in/jorgeromerocontreras/)  
📧 **Email:** contacto@deverom.com

---

# 📖 Documentación del Proyecto Lottery Valentine

## Índice

- [👨‍💻 Desarrollado por](#desarrollado-por)
- [📋 Descripción del Proyecto](#descripción-del-proyecto)
- [🎯 Objetivos del Sistema](#objetivos-del-sistema)
- [🎯 Decisiones técnicas](#decisiones-técnicas)
- [🏗️ Arquitectura del Sistema](#arquitectura-del-sistema)
- [✨ Funcionalidades Principales](#funcionalidades-principales)
- [🔒 Validaciones Implementadas](#validaciones-implementadas)
- [📁 Estructura del Proyecto](#estructura-del-proyecto)
- [🚀 Instalación y Configuración](#instalación-y-configuración)
- [🚀 Librerías Backend (Python/Django)](#librerías-backend-pythondjango)
- [🚀 Librerías Frontend (Node.js/Vue.js)](#librerías-frontend-nodejsvuejs)
- [📦 Instalación del Backend](#instalación-del-backend)
- [🎨 Instalación del Frontend](#instalación-del-frontend)
- [🔗 Endpoints de la API](#endpoints-de-la-api)
- [🧪 Flujo de Prueba Completo](#flujo-de-prueba-completo)
- [🛠️ Comandos Útiles](#comandos-útiles)
- [🐛 Solución de Problemas Comunes](#solución-de-problemas-comunes)
- [📊 Modelos de Datos](#modelos-de-datos)
- [🧪 Tests Unitarios](#tests-unitarios)
- [🔐 Seguridad](#seguridad)
- [📝 Notas Importantes](#notas-importantes)
- [📄 Licencia](#licencia)
- [🎉 Proyecto Completado](#proyecto-completado)
- 📎 Archivos relacionados
  - [CARTURAS-DE-PROCESOS.md](CARTURAS-DE-PROCESOS.md)
  - [LISTADO-ENDPOINTS.md](LISTADO-ENDPOINTS.md)

---

## 📋 Descripción del Proyecto


Sistema Full Stack para gestionar un sorteo de San Valentín donde los participantes pueden inscribirse para ganar una estadía de 2 noches todo pagado para una pareja en un hotel. El sistema incluye verificación de email, panel de administración y selección aleatoria de ganadores con notificaciones automáticas.

---

## 🎯 Objetivos del Sistema

1. Permitir la inscripción de usuarios al concurso
2. Validar emails únicos (sin registros duplicados)
3. Verificar correos electrónicos mediante tokens
4. Gestionar participantes verificados y pendientes
5. Sortear ganadores aleatoriamente entre participantes verificados
6. Notificar automáticamente a los ganadores por email
7. Proporcionar panel administrativo para gestionar el concurso

## 🎯 Decisiones técnicas

1. Django + DRF: se eligió por su robustez en la construcción de APIs y manejo claro de serializadores, validaciones y autenticación.
2. Vue 3 + TypeScript: permite un frontend modular, reactivo.
3. TypeScript: mejora la calidad del código y facilita la detección de errores en tiempo de compilación, añade algo de complicidad al proyecto, pero es mejor para un desarrollo en donde es necesario no perder tiempo en pequeños errores y con tiempo limtado.
3. Celery + Redis: usados para manejar tareas asíncronas como el envío de correos electrónicos de verificación y notificación de ganadores, evitando bloquear el flujo principal de la aplicación.
4. Mailtrap: elegido como servicio de correo para pruebas, ya que permite interceptar y visualizar emails sin necesidad de un servidor SMTP real.
5. Arquitectura separada (backend/frontend): facilita el escalado independiente y el despliegue en contenedores o servicios separados.


---

## 🏗️ Arquitectura del Sistema

### Backend
- **Framework:** Django 5.2 + Django Rest Framework
- **Base de datos:** PostgreSQL
- **Autenticación:** JWT (Simple JWT)
- **Tareas asíncronas:** Celery + Redis
- **Emails:** Django Email con Mailtrap (desarrollo)

### Frontend
- **Framework:** Vue.js 3 + TypeScript
- **Enrutamiento:** Vue Router
- **Estado:** Pinia
- **HTTP Client:** Axios
- **Estilos:** Bootstrap 5
- **Servidor desarrollo:** Vite

---

## ✨ Funcionalidades Principales

### Módulo Público
1. **Registro de participantes**
   - Formulario con nombre completo, email y teléfono
   - Validación de email único
   - Envío automático de email de verificación

2. **Verificación de email**
   - Link único por usuario (válido 24 horas)
   - Validación de token
   - Creación de contraseña (mínimo 8 caracteres)
   - Confirmación de participación

### Módulo Administrativo
1. **Login de administrador**
   - Autenticación mediante email y contraseña
   - Tokens JWT con expiración
   - Validación de permisos de staff

2. **Gestión de participantes**
   - Lista completa de inscritos
   - Filtros por estado (verificado/pendiente)
   - Búsqueda por nombre o email
   - Visualización de fechas de registro y verificación

3. **Sorteo de ganador**
   - Selección aleatoria entre participantes verificados
   - Visualización del ganador
   - Notificación automática por email
   - Opción de realizar múltiples sorteos

---

## 🔒 Validaciones Implementadas

### Backend
- Email único (no permite duplicados)
- Formato de email válido
- Contraseñas con mínimo 8 caracteres
- Confirmación de contraseña (ambas deben coincidir)
- Token de verificación válido y no expirado
- Solo usuarios con `is_staff=True` pueden acceder al admin
- Solo participantes verificados pueden ganar
- Tokens JWT con tiempo de expiración

### Frontend
- Campos requeridos en formularios
- Validación de tipo email
- Validación de longitud mínima de contraseña
- Confirmación de contraseña
- Protección de rutas administrativas (guards)
- Manejo de errores de API
- Estados de carga (loading)

---

## 📁 Estructura del Proyecto

```
lottery_valentine/
├── backend/                    # Django Backend
│   ├── apps/
│   │   ├── users/             # App de usuarios
│   │   │   ├── models.py      # Modelo User
│   │   │   ├── serializers.py # Serializadores
│   │   │   ├── views.py       # Endpoints de users
│   │   │   ├── tasks.py       # Tareas Celery (emails)
│   │   │   └── urls.py
│   │   └── contest/           # App del concurso
│   │       ├── models.py      # Modelos Participant y Winner
│   │       ├── serializers.py
│   │       ├── views.py       # Endpoints del concurso
│   │       ├── tasks.py       # Emails de notificación
│   │       └── urls.py
│   ├── config/                # Configuración Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── celery.py         # Configuración Celery
│   │   └── wsgi.py
│   ├── manage.py
│   ├── requirements.txt
│   └── .env                   # Variables de entorno
│
└── frontend/                  # Vue.js Frontend
    ├── src/
    │   ├── api/
    │   │   └── axios.ts       # Configuración Axios
    │   ├── components/
    │   ├── views/
    │   │   ├── RegisterView.vue
    │   │   ├── VerifyEmailView.vue
    │   │   ├── AdminLoginView.vue
    │   │   ├── AdminParticipantsView.vue
    │   │   └── AdminDrawView.vue
    │   ├── stores/
    │   │   └── auth.ts        # Store de autenticación
    │   ├── router/
    │   │   └── index.ts       # Rutas Vue Router
    │   ├── types/
    │   │   └── index.ts       # Tipos TypeScript
    │   ├── App.vue
    │   └── main.ts
    ├── package.json
    └── vite.config.ts
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python:** 3.10 o superior
- **Node.js:** 18 o superior
- **PostgreSQL:** 14 o superior
- **Redis:** 6 o superior
- **Git:** Para clonar el repositorio

---
## 🚀 Librerías Backend (Python/Django)

- **Django:** 5.1.2
- **djangorestframework:** 3.15.2
- **djangorestframework-simplejwt:** 5.3.1
- **django-cors-headers:** 4.4.0
- **celery:** 5.4.0
- **redis:** 5.0.8
- **psycopg2-binary:** 2.9.9
- **python-decouple:** 3.8

---

## 🚀 Librerías Frontend (Node.js/Vue.js)

- **vue:** 3.4.21
- **vue-router:** 4.3.0
- **pinia:** 2.1.7
- **axios:** 1.6.8
- **bootstrap:** 5.3.3
- **bootstrap-icons:** 1.11.3
- **typescript:** 5.4.0
- **vite:** 5.2.0

---

## 📦 Instalación del Backend

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd lottery_valentine
```

### 2. Crear entorno virtual de Python

```bash
python -m venv .venv

# Activar en Linux/Mac:
source .venv/bin/activate

# Activar en Windows:
.venv\Scripts\activate
```

### 3. Instalar dependencias del backend

```bash
cd backend
pip install -r requirements.txt
```

### 4. Crear base de datos PostgreSQL

```bash
# Acceder a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE lottery_valentine_db;

# Crear usuario (opcional)
CREATE USER lottery_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE lottery_valentine_db TO lottery_user;

# Salir
\q
```

### 5. Configurar variables de entorno

Crea el archivo `backend/.env`:

```env
# Django
SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=lottery_valentine_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Email (Mailtrap para desarrollo)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_mailtrap_user
EMAIL_HOST_PASSWORD=tu_mailtrap_password
DEFAULT_FROM_EMAIL=sorteo@ctsturismo.cl

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 6. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser

# Ingresar:
# - Email: admin@ctsturismo.cl
# - Nombre completo: Administrador
# - Teléfono: +56912345678
# - Password: tu_password_segura
```

### 8. Iniciar Redis

```bash
# En Linux/Mac:
redis-server

# En Windows (con Redis instalado):
redis-server.exe
```

### 9. Iniciar Celery Worker

En una nueva terminal (con el entorno virtual activado):

```bash
cd backend
celery -A config worker -l info
```

### 10. Iniciar servidor Django

En otra terminal:

```bash
cd backend
python manage.py runserver
```

El backend estará disponible en: `http://127.0.0.1:8000/`

---

## 🎨 Instalación del Frontend

### 1. Instalar dependencias

En una nueva terminal:

```bash
cd frontend
npm install
```

### 2. Iniciar servidor de desarrollo

```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:5173/`

---

## 🔗 Endpoints de la API

### Endpoints Públicos (Sin autenticación)

#### 1. Registro de Usuario
```
POST /api/users/register/
Content-Type: application/json

Body:
{
  "email": "usuario@example.com",
  "full_name": "Juan Pérez",
  "phone": "+56912345678",
  "frontend_url": "http://localhost:5173"
}

Response (201):
{
  "message": "¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.",
  "email": "usuario@example.com"
}
```

#### 2. Verificar Email
```
POST /api/users/verify-email/
Content-Type: application/json

Body:
{
  "token": "uuid-token-del-email"
}

Response (200):
{
  "message": "Token válido. Ahora puedes establecer tu contraseña.",
  "email": "usuario@example.com",
  "full_name": "Juan Pérez"
}
```

#### 3. Establecer Contraseña
```
POST /api/users/set-password/
Content-Type: application/json

Body:
{
  "token": "uuid-token-del-email",
  "password": "MiPassword123!",
  "password_confirm": "MiPassword123!"
}

Response (200):
{
  "message": "Tu cuenta ha sido activada. Ya estás participando en el sorteo."
}
```

#### 4. Login de Administrador
```
POST /api/users/admin/login/
Content-Type: application/json

Body:
{
  "email": "admin@ctsturismo.cl",
  "password": "tu_password"
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
```

### Endpoints Protegidos (Requieren autenticación)

**Header requerido:**
```
Authorization: Bearer <access_token>
```

#### 5. Lista de Participantes
```
GET /api/contest/participants/
Authorization: Bearer <token>

Query params (opcionales):
- search=nombre
- status=verified|pending
- page=1

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
```

#### 6. Estadísticas de Participantes
```
GET /api/contest/participants/stats/
Authorization: Bearer <token>

Response (200):
{
  "total_participants": 150,
  "verified_participants": 120,
  "pending_participants": 30,
  "eligible_for_draw": 120
}
```

#### 7. Realizar Sorteo
```
POST /api/contest/draw-winner/
Authorization: Bearer <token>
Content-Type: application/json

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
```

#### 8. Obtener Último Ganador
```
GET /api/contest/latest-winner/
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "winner_name": "María González",
  "winner_email": "ganador@example.com",
  "draw_date": "2025-10-02T10:20:00Z",
  "is_notified": true,
  "notified_at": "2025-10-02T10:20:01Z"
}
```

---

## 🧪 Flujo de Prueba Completo

### 1. Registrar un Usuario
- Ir a `http://localhost:5173/`
- Llenar formulario con datos válidos
- Hacer clic en "Inscribirme al Sorteo"
- Verificar mensaje de éxito

### 2. Verificar Email
- Ir a Mailtrap inbox
- Abrir email de verificación
- Hacer clic en el botón "Verificar mi correo"
- Crear contraseña (mínimo 8 caracteres)
- Confirmar contraseña
- Verificar mensaje de confirmación

### 3. Login como Administrador
- Ir a `http://localhost:5173/admin/login`
- Ingresar credenciales del superusuario
- Hacer clic en "Iniciar Sesión"

### 4. Ver Lista de Participantes
- Verificar que aparezcan todos los participantes
- Probar búsqueda por nombre
- Probar filtros por estado

### 5. Realizar Sorteo
- Hacer clic en "Sortear Ganador"
- Esperar animación de sorteo
- Verificar datos del ganador
- Revisar email del ganador en Mailtrap

---

## 🛠️ Comandos Útiles

### Backend

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

# Acceder al shell de Django
python manage.py shell

# Iniciar Celery
celery -A config worker -l info

# Ver tareas de Celery
celery -A config inspect active
```

### Frontend

```bash
# Instalar dependencias
npm install

# Iniciar servidor desarrollo
npm run dev

# Compilar para producción
npm run build

# Vista previa de producción
npm run preview

# Linter
npm run lint

# Tests
npm run test:unit
```

---

## 🐛 Solución de Problemas Comunes

### Error: "Unable to load celery application"
**Solución:** Ejecutar Celery con `celery -A config worker -l info` desde la carpeta `backend/`

### Error: "CORS policy blocked"
**Solución:** Verificar que `django-cors-headers` esté instalado y configurado en `settings.py`

### Error: "Token inválido o expirado"
**Solución:** Generar un nuevo registro para obtener un token fresco

### Error: "No tienes permisos de administrador"
**Solución:** Asegurarse de que el usuario tenga `is_staff=True`:
```python
python manage.py shell
from apps.users.models import User
user = User.objects.get(email='tu@email.com')
user.is_staff = True
user.is_superuser = True
user.save()
```

### Email no llega
**Solución:** 
- Verificar que Celery esté corriendo
- Verificar que Redis esté corriendo
- Revisar credenciales de Mailtrap en `.env`

### Error: "Connection refused" al registrar
**Solución:**
- Verificar que Django esté corriendo en `http://127.0.0.1:8000`
- Verificar configuración CORS en `settings.py`

---

## 📊 Modelos de Datos

### User (apps/users/models.py)
```python
- id: UUID (PK)
- email: EmailField (único)
- full_name: CharField
- phone: CharField
- password: CharField (hash)
- is_verified: BooleanField
- is_staff: BooleanField
- verification_token: UUIDField
- date_joined: DateTimeField
```

### Participant (apps/contest/models.py)
```python
- id: UUID (PK)
- user: ForeignKey(User)
- status: CharField (pending/verified/rejected)
- registered_at: DateTimeField
- verified_at: DateTimeField (nullable)
```

### Winner (apps/contest/models.py)
```python
- id: UUID (PK)
- participant: ForeignKey(Participant)
- winner_name: CharField
- winner_email: EmailField
- draw_date: DateTimeField
- is_notified: BooleanField
- notified_at: DateTimeField (nullable)
- notes: TextField (nullable)
```

---

## 🔐 Seguridad

- Contraseñas hasheadas con Django's PBKDF2
- Tokens JWT con expiración configurable
- Tokens de verificación únicos por usuario
- CORS configurado para orígenes específicos
- Rutas administrativas protegidas con permisos
- Validación de datos en backend y frontend
- Variables sensibles en archivo `.env`

---

---

## 🧪 Tests Unitarios

El proyecto incluye **38 tests unitarios** que cubren los módulos principales del sistema con una cobertura del **87%**.

### Cobertura de Tests

**apps/users (26 tests):**
- Tests de modelos: creación de usuarios, validación de email único, normalización
- Tests de serializers: validaciones de nombre, teléfono, email, contraseñas
- Tests de endpoints: registro, verificación, login admin, establecer contraseña
- Tests de tareas: envío de emails de verificación

**apps/contest (12 tests):**
- Tests de modelos: participantes, ganadores
- Tests de endpoints: lista de participantes, sorteo, último ganador, estadísticas
- Tests de autenticación en rutas protegidas
- Tests de tareas: emails de confirmación y notificación de ganadores

### Ejecutar Tests
```bash
# Todos los tests
python manage.py test

# Solo tests de users
python manage.py test apps.users

# Solo tests de contest
python manage.py test apps.contest

# Con más detalle
python manage.py test --verbosity=2

```

### Cobertura Actual

El proyecto tiene una cobertura de código del **87%** (787/787 statements, 101 missed).

**El reporte HTML muestra:**
- Resumen general de cobertura por módulo
- Líneas específicas cubiertas y no cubiertas
- Navegación interactiva por archivos
- Estadísticas detalladas por archivo

### Generar Reporte de Cobertura
```bash
# Ejecutar tests con cobertura
coverage run --source='apps' manage.py test

# Ver reporte en la terminal
coverage report

# Generar reporte HTML interactivo
coverage html

# Abrir el reporte en el navegador
# En macOS:
open htmlcov/index.html

# En Linux:
xdg-open htmlcov/index.html

# En Windows:
start htmlcov/index.html

# O simplemente navega a: file:///ruta/al/proyecto/backend/htmlcov/index.html

```

### Generar Reporte de Cobertura
---

## 📝 Notas Importantes

1. **Mailtrap:** En desarrollo, todos los emails se capturan en Mailtrap. Para producción, cambiar a servicio real (SendGrid, AWS SES, etc.)

2. **Tokens JWT:** Por defecto expiran en 60 minutos. Configurable en `.env`

3. **Redis:** Debe estar corriendo para que Celery funcione

4. **Celery:** Debe estar corriendo para envío asíncrono de emails

5. **PostgreSQL:** Se recomienda para producción. SQLite solo para desarrollo

6. **Frontend URL:** Al registrar usuarios, el `frontend_url` debe coincidir con donde corre el frontend

---

## 📄 Licencia

Este proyecto fue desarrollado como prueba técnica para CTS Turismo.

---

## 🎉 Proyecto Completado

El sistema está totalmente funcional con todas las características solicitadas:
- ✅ Registro e inscripción
- ✅ Verificación por email
- ✅ Test Unitario por modulo users, contest y todos ejecutados
- ✅ Panel administrativo
- ✅ Sorteo aleatorio de ganadores
- ✅ Notificaciones automáticas
- ✅ Interfaz responsive con Bootstrap 5

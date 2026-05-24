# API Escolar — Node.js + Express + MySQL

API RESTful profesional para administración de alumnos, materias e inscripciones. Incluye autenticación JWT, control de acceso por roles, auditoría completa y bajas lógicas.

---

## Estructura del proyecto

```
api-escolar/
├── database/
│   └── schema.sql              → Script SQL completo
├── src/
│   ├── config/
│   │   ├── database.js         → Pool de conexiones MySQL
│   │   └── jwt.js              → Configuración JWT
│   ├── controllers/            → Reciben req/res, llaman al service
│   │   ├── auth.controller.js
│   │   ├── carrera.controller.js
│   │   ├── inscripcion.controller.js
│   │   ├── materia.controller.js
│   │   └── usuario.controller.js
│   ├── middlewares/
│   │   ├── auth.middleware.js   → verifyToken + authorizeRoles
│   │   ├── error.middleware.js  → Manejo centralizado de errores
│   │   └── validate.middleware.js → express-validator handler
│   ├── repositories/           → Solo queries SQL (acceso a DB)
│   │   ├── carrera.repository.js
│   │   ├── inscripcion.repository.js
│   │   ├── materia.repository.js
│   │   └── usuario.repository.js
│   ├── routes/                 → Definición de endpoints + middlewares
│   │   ├── alumno.routes.js
│   │   ├── auth.routes.js
│   │   ├── carrera.routes.js
│   │   ├── inscripcion.routes.js
│   │   ├── materia.routes.js
│   │   └── usuario.routes.js
│   ├── services/               → Lógica de negocio
│   │   ├── auth.service.js
│   │   ├── carrera.service.js
│   │   ├── inscripcion.service.js
│   │   ├── materia.service.js
│   │   └── usuario.service.js
│   ├── utils/
│   │   ├── audit.js            → Helpers de auditoría
│   │   ├── response.js         → Respuestas JSON estandarizadas
│   │   └── seed.js             → Script de datos iniciales
│   ├── validators/             → Reglas express-validator por entidad
│   │   ├── auth.validator.js
│   │   ├── carrera.validator.js
│   │   ├── inscripcion.validator.js
│   │   ├── materia.validator.js
│   │   └── usuario.validator.js
│   ├── app.js                  → Configuración Express + rutas
│   └── server.js               → Entry point
├── .env.example
├── package.json
└── README.md
```

---

## Cómo ejecutar el proyecto

### 1. Clonar / descomprimir el proyecto

'''bash
cd api-escolar
```

### 2. Instalar dependencias

```bash
npm install
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus datos de MySQL
```

`.env` mínimo necesario:
```env
PORT=3000
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=api_escolar
JWT_SECRET=un_secreto_muy_largo_y_aleatorio
JWT_EXPIRES_IN=8h
BCRYPT_SALT_ROUNDS=12
NODE_ENV=development
```

### 4. Crear la base de datos

```bash
mysql -u root -p < database/schema.sql
```

O manualmente en MySQL Workbench: abrir y ejecutar `database/schema.sql`.

### 5. Cargar datos de prueba (seed)

```bash
npm run seed
```

Esto crea:
- Usuario admin: `admin` / `Admin1234!`
- Usuario alumno: `jperez` / `Alumno1234!`
- 3 carreras de ejemplo
- 4 materias de ejemplo

### 6. Iniciar el servidor

```bash
# Producción
npm start

# Desarrollo (con auto-reload)
npm run dev
```

El servidor arrancará en `http://localhost:3000`.

---

## Autenticación

Todos los endpoints (excepto `/auth/login` y `/health`) requieren un JWT.

**Header requerido:**
```
Authorization: Bearer <token>
```

**Roles disponibles:**
| Rol | Permisos |
|-----|----------|
| `Administrador` | Acceso total (CRUD completo) |
| `Coordinador` | Solo lectura de materias, carreras, alumnos |
| `Alumno` | Ver materias, ver sus propias inscripciones, inscribirse a sí mismo |

---

## Endpoints

### Auth
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Login, retorna JWT |

### Usuarios (solo Administrador)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/usuarios` | Listar usuarios activos |
| GET | `/api/v1/usuarios/:id` | Ver usuario |
| POST | `/api/v1/usuarios` | Crear usuario |
| PUT | `/api/v1/usuarios/:id` | Editar usuario |
| DELETE | `/api/v1/usuarios/:id` | Baja lógica |

### Carreras
| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/api/v1/carreras` | Listar | Admin, Coordinador |
| GET | `/api/v1/carreras/:id` | Ver | Admin, Coordinador |
| POST | `/api/v1/carreras` | Crear | Admin |
| PUT | `/api/v1/carreras/:id` | Editar | Admin |
| DELETE | `/api/v1/carreras/:id` | Baja lógica | Admin |

### Materias
| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/api/v1/materias` | Listar | Todos |
| GET | `/api/v1/materias/:id` | Ver | Todos |
| GET | `/api/v1/materias/:id/alumnos` | Alumnos inscriptos | Admin, Coordinador |
| POST | `/api/v1/materias` | Crear | Admin |
| PUT | `/api/v1/materias/:id` | Editar | Admin |
| DELETE | `/api/v1/materias/:id` | Baja lógica | Admin |

### Inscripciones
| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| POST | `/api/v1/inscripciones` | Inscribir alumno | Admin, Alumno (solo a sí mismo) |
| DELETE | `/api/v1/inscripciones/:id` | Baja lógica | Admin, Alumno dueño |

### Alumnos
| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/api/v1/alumnos/:id/materias` | Materias de un alumno | Admin, Coordinador, el propio Alumno |

---

## Ejemplos de Requests (Postman / curl)

### Login
```bash
curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"usuario": "admin", "password": "Admin1234!"}'
```

Respuesta:
```json
{
  "success": true,
  "message": "Login exitoso.",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": { "id": 1, "nombre": "Administrador Sistema", "usuario": "admin", "rol": "Administrador" }
  }
}
```

### Crear materia
```bash
curl -X POST http://localhost:3000/api/v1/materias \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"nombre": "Cálculo I", "carrera_id": 1}'
```

### Inscribir alumno (desde admin)
```bash
curl -X POST http://localhost:3000/api/v1/inscripciones \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN_ADMIN>" \
  -d '{"alumno_id": 2, "materia_id": 1}'
```

### Ver materias de un alumno (desde el propio alumno)
```bash
curl http://localhost:3000/api/v1/alumnos/2/materias \
  -H "Authorization: Bearer <TOKEN_ALUMNO>"
```

### Baja lógica de inscripción
```bash
curl -X DELETE http://localhost:3000/api/v1/inscripciones/1 \
  -H "Authorization: Bearer <TOKEN>"
```

---

## Recomendaciones de seguridad para producción

1. **JWT_SECRET**: Usar al menos 64 caracteres aleatorios. Generar con: `node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"`
2. **HTTPS**: Usar siempre HTTPS. Configura un proxy inverso (Nginx / Caddy) con certificado TLS.
3. **Rate limiting**: Agregar `express-rate-limit` para prevenir ataques de fuerza bruta en `/auth/login`.
4. **Helmet**: Agregar el paquete `helmet` para headers de seguridad HTTP.
5. **CORS**: Configurar `cors` para aceptar solo orígenes conocidos.
6. **Logs**: Usar `winston` o `pino` para logs estructurados en producción.
7. **Variables de entorno**: Nunca commitear `.env` al repositorio. Usar gestores de secretos (AWS Secrets Manager, Vault, etc.).
8. **NODE_ENV=production**: Asegurarse de setear en producción para ocultar stack traces en errores.
9. **DB usuario dedicado**: Crear un usuario MySQL con permisos mínimos (solo SELECT/INSERT/UPDATE, sin DROP/CREATE).

---

## Dependencias

| Paquete | Propósito |
|---------|-----------|
| `express` | Framework web |
| `mysql2` | Cliente MySQL con soporte async/await y pool |
| `jsonwebtoken` | Generación y verificación de JWT |
| `bcryptjs` | Hash seguro de contraseñas |
| `express-validator` | Validación de inputs |
| `dotenv` | Variables de entorno |
| `nodemon` | Auto-reload en desarrollo |

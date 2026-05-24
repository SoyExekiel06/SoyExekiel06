const express = require('express');

// Rutas
const authRoutes        = require('./routes/auth.routes');
const usuarioRoutes     = require('./routes/usuario.routes');
const carreraRoutes     = require('./routes/carrera.routes');
const materiaRoutes     = require('./routes/materia.routes');
const inscripcionRoutes = require('./routes/inscripcion.routes');
const alumnoRoutes      = require('./routes/alumno.routes');

// Middlewares globales
const { errorMiddleware, notFoundMiddleware } = require('./middlewares/error.middleware');

const app = express();

// ─── Parsers ──────────────────────────────────────────────────────────────────
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ─── Seguridad básica: deshabilitar header que revela que usamos Express ──────
app.disable('x-powered-by');

// ─── Health check (no requiere auth) ─────────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({ success: true, message: 'API funcionando.', timestamp: new Date().toISOString() });
});

// ─── Rutas de la API ──────────────────────────────────────────────────────────
app.use('/api/v1/auth',         authRoutes);
app.use('/api/v1/usuarios',     usuarioRoutes);
app.use('/api/v1/carreras',     carreraRoutes);
app.use('/api/v1/materias',     materiaRoutes);
app.use('/api/v1/inscripciones',inscripcionRoutes);
app.use('/api/v1/alumnos',      alumnoRoutes);

// ─── Ruta no encontrada (debe ir antes del error middleware) ──────────────────
app.use(notFoundMiddleware);

// ─── Manejo centralizado de errores (SIEMPRE al final) ───────────────────────
app.use(errorMiddleware);

module.exports = app;

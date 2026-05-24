/**
 * Middleware de manejo centralizado de errores.
 * Debe registrarse DESPUÉS de todas las rutas en app.js.
 * Express lo reconoce como error handler por tener 4 parámetros (err, req, res, next).
 */
const errorMiddleware = (err, req, res, next) => {
  // Log del error en servidor (en producción usar un logger como Winston)
  console.error('Error no controlado:', {
    message: err.message,
    stack: process.env.NODE_ENV !== 'production' ? err.stack : undefined,
    path: req.path,
    method: req.method,
  });

  // Error de validación de express-validator (manejado en los controllers, pero por si acaso)
  if (err.type === 'validation') {
    return res.status(422).json({
      success: false,
      message: 'Error de validación.',
      error: err.errors,
    });
  }

  // Error de JWT mal formado que escapó del middleware de auth
  if (err.name === 'JsonWebTokenError' || err.name === 'TokenExpiredError') {
    return res.status(401).json({ success: false, message: 'Token inválido o expirado.' });
  }

  // Error de MySQL: violación de clave única
  if (err.code === 'ER_DUP_ENTRY') {
    return res.status(409).json({ success: false, message: 'Ya existe un registro con esos datos únicos.' });
  }

  // Error genérico del servidor
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Error interno del servidor.';

  return res.status(statusCode).json({
    success: false,
    message,
    error: process.env.NODE_ENV !== 'production' ? err.stack : undefined,
  });
};

/**
 * Middleware para rutas no encontradas (404).
 * Registrar antes del error middleware.
 */
const notFoundMiddleware = (req, res) => {
  res.status(404).json({
    success: false,
    message: `Ruta ${req.method} ${req.originalUrl} no encontrada.`,
  });
};

module.exports = { errorMiddleware, notFoundMiddleware };

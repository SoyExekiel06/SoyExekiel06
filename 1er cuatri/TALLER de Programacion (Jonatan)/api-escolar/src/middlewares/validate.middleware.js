const { validationResult } = require('express-validator');

/**
 * Middleware que evalúa los resultados de express-validator.
 * Se encadena DESPUÉS de las reglas de validación en las rutas.
 *
 * Uso en rutas:
 *   router.post('/', [body('nombre').notEmpty(), validateRequest], controller.create)
 */
const validateRequest = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(422).json({
      success: false,
      message: 'Error de validación en los datos enviados.',
      error: errors.array().map((e) => ({ campo: e.path, mensaje: e.msg })),
    });
  }
  next();
};

module.exports = { validateRequest };

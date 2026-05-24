/**
 * Genera una respuesta de éxito estandarizada.
 * @param {object} res - Express response object
 * @param {number} statusCode - HTTP status code
 * @param {string} message - Mensaje descriptivo
 * @param {any} data - Payload de datos
 */
const successResponse = (res, statusCode = 200, message = 'OK', data = null) => {
  const response = { success: true, message };
  if (data !== null) response.data = data;
  return res.status(statusCode).json(response);
};

/**
 * Genera una respuesta de error estandarizada.
 * @param {object} res - Express response object
 * @param {number} statusCode - HTTP status code
 * @param {string} message - Mensaje de error
 * @param {any} error - Detalle del error (solo en desarrollo)
 */
const errorResponse = (res, statusCode = 500, message = 'Error interno', error = null) => {
  const response = { success: false, message };
  // Solo exponer detalles técnicos del error en desarrollo
  if (error && process.env.NODE_ENV !== 'production') {
    response.error = error;
  }
  return res.status(statusCode).json(response);
};

module.exports = { successResponse, errorResponse };

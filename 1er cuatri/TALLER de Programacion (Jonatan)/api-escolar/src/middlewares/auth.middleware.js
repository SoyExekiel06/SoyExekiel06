const jwt = require('jsonwebtoken');
const jwtConfig = require('../config/jwt');
const { errorResponse } = require('../utils/response');

/**
 * Middleware: verifica que el request incluya un JWT válido.
 * Agrega el payload del token al objeto `req.user` para uso posterior.
 */
const verifyToken = (req, res, next) => {
  // El token se espera en el header: Authorization: Bearer <token>
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // "Bearer TOKEN"

  if (!token) {
    return errorResponse(res, 401, 'Token de acceso requerido.');
  }

  try {
    const decoded = jwt.verify(token, jwtConfig.secret);
    req.user = decoded; // { id, usuario, rol, iat, exp }
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return errorResponse(res, 401, 'El token ha expirado.');
    }
    return errorResponse(res, 401, 'Token inválido.');
  }
};

/**
 * Middleware factory: verifica que el usuario tenga uno de los roles permitidos.
 * @param {...string} roles - Nombres de roles permitidos (ej: 'Administrador', 'Coordinador')
 * @returns Middleware de Express
 *
 * Uso: authorizeRoles('Administrador', 'Coordinador')
 */
const authorizeRoles = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return errorResponse(res, 401, 'No autenticado.');
    }
    if (!roles.includes(req.user.rol)) {
      return errorResponse(res, 403, 'No tenés permisos para realizar esta acción.');
    }
    next();
  };
};

module.exports = { verifyToken, authorizeRoles };

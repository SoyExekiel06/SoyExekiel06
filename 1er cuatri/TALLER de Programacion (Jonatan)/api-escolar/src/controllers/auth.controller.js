const authService = require('../services/auth.service');
const { successResponse } = require('../utils/response');

/**
 * POST /auth/login
 * Autentica un usuario y retorna un JWT.
 */
const login = async (req, res, next) => {
  try {
    const { usuario, password } = req.body;
    const result = await authService.login(usuario, password);
    return successResponse(res, 200, 'Login exitoso.', result);
  } catch (error) {
    next(error);
  }
};

module.exports = { login };

const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const jwtConfig = require('../config/jwt');
const usuarioRepo = require('../repositories/usuario.repository');

/**
 * Servicio de autenticación.
 * Contiene la lógica de login y generación de tokens.
 */

/**
 * Autentica un usuario y devuelve un JWT si las credenciales son válidas.
 * @param {string} usuario - Username
 * @param {string} password - Contraseña en texto plano
 * @returns {{ token: string, user: object }}
 * @throws {Error} Si las credenciales son inválidas o el usuario está dado de baja
 */
const login = async (usuario, password) => {
  // Buscar usuario incluyendo el hash de password
  const user = await usuarioRepo.findByUsuario(usuario);

  // Mensaje genérico para no revelar si el usuario existe (security best practice)
  const invalidCredsError = new Error('Usuario o contraseña incorrectos.');
  invalidCredsError.statusCode = 401;

  if (!user) throw invalidCredsError;

  // Verificar que el usuario esté activo
  if (user.fecha_baja !== null) {
    const err = new Error('El usuario está inactivo. Contacte al administrador.');
    err.statusCode = 403;
    throw err;
  }

  // Comparar contraseña con el hash almacenado
  const passwordMatch = await bcrypt.compare(password, user.password);
  if (!passwordMatch) throw invalidCredsError;

  // Payload del JWT: solo datos necesarios, sin información sensible
  const payload = {
    id: user.id,
    usuario: user.usuario,
    rol: user.rol,
  };

  const token = jwt.sign(payload, jwtConfig.secret, { expiresIn: jwtConfig.expiresIn });

  // Devolver token y datos del usuario (sin password)
  return {
    token,
    user: {
      id: user.id,
      nombre: user.nombre,
      mail: user.mail,
      usuario: user.usuario,
      rol: user.rol,
    },
  };
};

module.exports = { login };

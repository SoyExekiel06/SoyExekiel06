/**
 * Configuración centralizada de JWT.
 * Mantener la config en un solo lugar facilita cambios futuros.
 */
const jwtConfig = {
  secret: process.env.JWT_SECRET || 'fallback_secret_cambiar_en_produccion',
  expiresIn: process.env.JWT_EXPIRES_IN || '8h',
};

// Advertencia en desarrollo si se usa el secret de fallback
if (!process.env.JWT_SECRET) {
  console.warn(' JWT_SECRET no definido en .env. Usando valor de fallback (NO usar en producción).');
}

module.exports = jwtConfig;

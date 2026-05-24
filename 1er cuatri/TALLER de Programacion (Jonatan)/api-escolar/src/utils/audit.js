/**
 * Genera los campos de auditoría para INSERT (alta).
 * @param {string} usuario - Username del usuario que realiza la acción
 * @returns {object} Campos de auditoría para alta
 */
const auditCreate = (usuario) => ({
  fecha_alta: new Date(),
  usuario_alta: usuario,
  fecha_modificacion: null,
  usuario_modificacion: null,
  fecha_baja: null,
  usuario_baja: null,
});

/**
 * Genera los campos de auditoría para UPDATE (modificación).
 * @param {string} usuario - Username del usuario que realiza la acción
 * @returns {object} Campos de auditoría para modificación
 */
const auditUpdate = (usuario) => ({
  fecha_modificacion: new Date(),
  usuario_modificacion: usuario,
});

/**
 * Genera los campos de auditoría para DELETE lógico (baja).
 * @param {string} usuario - Username del usuario que realiza la acción
 * @returns {object} Campos de auditoría para baja lógica
 */
const auditDelete = (usuario) => ({
  fecha_baja: new Date(),
  usuario_baja: usuario,
});

module.exports = { auditCreate, auditUpdate, auditDelete };

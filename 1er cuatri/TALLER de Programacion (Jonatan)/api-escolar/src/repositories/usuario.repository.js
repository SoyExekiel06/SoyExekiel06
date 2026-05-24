const { pool } = require('../config/database');

/**
 * Capa de acceso a datos para usuarios.
 * Solo contiene queries SQL, sin lógica de negocio.
 */

const findAll = async () => {
  const [rows] = await pool.execute(
    `SELECT u.id, u.nombre, u.mail, u.usuario, r.nombre AS rol,
            u.fecha_alta, u.usuario_alta, u.fecha_modificacion, u.usuario_modificacion
     FROM usuarios u
     INNER JOIN roles r ON u.rol_id = r.id
     WHERE u.fecha_baja IS NULL
     ORDER BY u.nombre`
  );
  return rows;
};

const findById = async (id) => {
  const [rows] = await pool.execute(
    `SELECT u.id, u.nombre, u.mail, u.usuario, r.nombre AS rol, u.rol_id,
            u.fecha_alta, u.usuario_alta, u.fecha_modificacion, u.usuario_modificacion
     FROM usuarios u
     INNER JOIN roles r ON u.rol_id = r.id
     WHERE u.id = ? AND u.fecha_baja IS NULL`,
    [id]
  );
  return rows[0] || null;
};

const findByUsuario = async (usuario) => {
  // Incluye el hash de password para la autenticación
  const [rows] = await pool.execute(
    `SELECT u.id, u.nombre, u.mail, u.usuario, u.password, r.nombre AS rol,
            u.fecha_baja
     FROM usuarios u
     INNER JOIN roles r ON u.rol_id = r.id
     WHERE u.usuario = ?`,
    [usuario]
  );
  return rows[0] || null;
};

const findByMail = async (mail) => {
  const [rows] = await pool.execute(
    'SELECT id FROM usuarios WHERE mail = ? AND fecha_baja IS NULL',
    [mail]
  );
  return rows[0] || null;
};

const findByUsuarioExcluding = async (usuario, excludeId) => {
  const [rows] = await pool.execute(
    'SELECT id FROM usuarios WHERE usuario = ? AND id != ? AND fecha_baja IS NULL',
    [usuario, excludeId]
  );
  return rows[0] || null;
};

const create = async (data) => {
  const { nombre, mail, usuario, password, rol_id, fecha_alta, usuario_alta } = data;
  const [result] = await pool.execute(
    `INSERT INTO usuarios (nombre, mail, usuario, password, rol_id, fecha_alta, usuario_alta)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [nombre, mail, usuario, password, rol_id, fecha_alta, usuario_alta]
  );
  return result.insertId;
};

const update = async (id, data) => {
  const fields = [];
  const values = [];

  if (data.nombre !== undefined)  { fields.push('nombre = ?');  values.push(data.nombre); }
  if (data.mail !== undefined)    { fields.push('mail = ?');    values.push(data.mail); }
  if (data.rol_id !== undefined)  { fields.push('rol_id = ?'); values.push(data.rol_id); }
  if (data.password !== undefined){ fields.push('password = ?');values.push(data.password); }

  fields.push('fecha_modificacion = ?', 'usuario_modificacion = ?');
  values.push(data.fecha_modificacion, data.usuario_modificacion, id);

  const [result] = await pool.execute(
    `UPDATE usuarios SET ${fields.join(', ')} WHERE id = ? AND fecha_baja IS NULL`,
    values
  );
  return result.affectedRows;
};

const softDelete = async (id, fecha_baja, usuario_baja) => {
  const [result] = await pool.execute(
    'UPDATE usuarios SET fecha_baja = ?, usuario_baja = ? WHERE id = ? AND fecha_baja IS NULL',
    [fecha_baja, usuario_baja, id]
  );
  return result.affectedRows;
};

module.exports = { findAll, findById, findByUsuario, findByMail, findByUsuarioExcluding, create, update, softDelete };

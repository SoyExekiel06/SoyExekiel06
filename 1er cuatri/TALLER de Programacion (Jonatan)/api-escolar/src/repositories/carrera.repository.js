const { pool } = require('../config/database');

const findAll = async () => {
  const [rows] = await pool.execute(
    `SELECT id, nombre, fecha_alta, usuario_alta, fecha_modificacion, usuario_modificacion
     FROM carreras
     WHERE fecha_baja IS NULL
     ORDER BY nombre`
  );
  return rows;
};

const findById = async (id) => {
  const [rows] = await pool.execute(
    `SELECT id, nombre, fecha_alta, usuario_alta, fecha_modificacion, usuario_modificacion
     FROM carreras
     WHERE id = ? AND fecha_baja IS NULL`,
    [id]
  );
  return rows[0] || null;
};

const findByNombre = async (nombre) => {
  const [rows] = await pool.execute(
    'SELECT id FROM carreras WHERE nombre = ? AND fecha_baja IS NULL',
    [nombre]
  );
  return rows[0] || null;
};

const create = async (data) => {
  const { nombre, fecha_alta, usuario_alta } = data;
  const [result] = await pool.execute(
    'INSERT INTO carreras (nombre, fecha_alta, usuario_alta) VALUES (?, ?, ?)',
    [nombre, fecha_alta, usuario_alta]
  );
  return result.insertId;
};

const update = async (id, data) => {
  const [result] = await pool.execute(
    `UPDATE carreras
     SET nombre = ?, fecha_modificacion = ?, usuario_modificacion = ?
     WHERE id = ? AND fecha_baja IS NULL`,
    [data.nombre, data.fecha_modificacion, data.usuario_modificacion, id]
  );
  return result.affectedRows;
};

const softDelete = async (id, fecha_baja, usuario_baja) => {
  const [result] = await pool.execute(
    'UPDATE carreras SET fecha_baja = ?, usuario_baja = ? WHERE id = ? AND fecha_baja IS NULL',
    [fecha_baja, usuario_baja, id]
  );
  return result.affectedRows;
};

module.exports = { findAll, findById, findByNombre, create, update, softDelete };

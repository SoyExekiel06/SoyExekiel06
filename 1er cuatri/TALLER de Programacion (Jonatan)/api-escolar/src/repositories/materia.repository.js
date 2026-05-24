const { pool } = require('../config/database');

const findAll = async () => {
  const [rows] = await pool.execute(
    `SELECT m.id, m.nombre, m.carrera_id, c.nombre AS carrera,
            m.fecha_alta, m.usuario_alta, m.fecha_modificacion, m.usuario_modificacion
     FROM materias m
     INNER JOIN carreras c ON m.carrera_id = c.id
     WHERE m.fecha_baja IS NULL
     ORDER BY m.nombre`
  );
  return rows;
};

const findById = async (id) => {
  const [rows] = await pool.execute(
    `SELECT m.id, m.nombre, m.carrera_id, c.nombre AS carrera,
            m.fecha_alta, m.usuario_alta, m.fecha_modificacion, m.usuario_modificacion
     FROM materias m
     INNER JOIN carreras c ON m.carrera_id = c.id
     WHERE m.id = ? AND m.fecha_baja IS NULL`,
    [id]
  );
  return rows[0] || null;
};

const findAlumnosByMateria = async (materiaId) => {
  const [rows] = await pool.execute(
    `SELECT u.id, u.nombre, u.mail, u.usuario,
            i.id AS inscripcion_id, i.fecha_alta AS fecha_inscripcion
     FROM inscripciones i
     INNER JOIN usuarios u ON i.alumno_id = u.id
     WHERE i.materia_id = ?
       AND i.fecha_baja IS NULL
       AND u.fecha_baja IS NULL
     ORDER BY u.nombre`,
    [materiaId]
  );
  return rows;
};

const create = async (data) => {
  const { nombre, carrera_id, fecha_alta, usuario_alta } = data;
  const [result] = await pool.execute(
    'INSERT INTO materias (nombre, carrera_id, fecha_alta, usuario_alta) VALUES (?, ?, ?, ?)',
    [nombre, carrera_id, fecha_alta, usuario_alta]
  );
  return result.insertId;
};

const update = async (id, data) => {
  const fields = [];
  const values = [];

  if (data.nombre !== undefined)     { fields.push('nombre = ?');     values.push(data.nombre); }
  if (data.carrera_id !== undefined) { fields.push('carrera_id = ?'); values.push(data.carrera_id); }

  fields.push('fecha_modificacion = ?', 'usuario_modificacion = ?');
  values.push(data.fecha_modificacion, data.usuario_modificacion, id);

  const [result] = await pool.execute(
    `UPDATE materias SET ${fields.join(', ')} WHERE id = ? AND fecha_baja IS NULL`,
    values
  );
  return result.affectedRows;
};

const softDelete = async (id, fecha_baja, usuario_baja) => {
  const [result] = await pool.execute(
    'UPDATE materias SET fecha_baja = ?, usuario_baja = ? WHERE id = ? AND fecha_baja IS NULL',
    [fecha_baja, usuario_baja, id]
  );
  return result.affectedRows;
};

module.exports = { findAll, findById, findAlumnosByMateria, create, update, softDelete };

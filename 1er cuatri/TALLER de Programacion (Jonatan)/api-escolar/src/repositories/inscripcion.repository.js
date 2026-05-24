const { pool } = require('../config/database');

const findById = async (id) => {
  const [rows] = await pool.execute(
    `SELECT i.id, i.alumno_id, i.materia_id,
            u.nombre AS alumno_nombre, m.nombre AS materia_nombre,
            i.fecha_alta, i.usuario_alta, i.fecha_baja, i.usuario_baja
     FROM inscripciones i
     INNER JOIN usuarios u ON i.alumno_id = u.id
     INNER JOIN materias m ON i.materia_id = m.id
     WHERE i.id = ?`,
    [id]
  );
  return rows[0] || null;
};

const findByAlumno = async (alumnoId) => {
  const [rows] = await pool.execute(
    `SELECT i.id AS inscripcion_id, m.id AS materia_id, m.nombre AS materia,
            c.nombre AS carrera, i.fecha_alta AS fecha_inscripcion
     FROM inscripciones i
     INNER JOIN materias m ON i.materia_id = m.id
     INNER JOIN carreras c ON m.carrera_id = c.id
     WHERE i.alumno_id = ?
       AND i.fecha_baja IS NULL
       AND m.fecha_baja IS NULL
     ORDER BY m.nombre`,
    [alumnoId]
  );
  return rows;
};

/**
 * Verifica si ya existe una inscripción activa para alumno+materia.
 * Usado para evitar inscripciones duplicadas.
 */
const findDuplicate = async (alumno_id, materia_id) => {
  const [rows] = await pool.execute(
    'SELECT id FROM inscripciones WHERE alumno_id = ? AND materia_id = ? AND fecha_baja IS NULL',
    [alumno_id, materia_id]
  );
  return rows[0] || null;
};

const create = async (data) => {
  const { alumno_id, materia_id, fecha_alta, usuario_alta } = data;
  const [result] = await pool.execute(
    'INSERT INTO inscripciones (alumno_id, materia_id, fecha_alta, usuario_alta) VALUES (?, ?, ?, ?)',
    [alumno_id, materia_id, fecha_alta, usuario_alta]
  );
  return result.insertId;
};

const softDelete = async (id, fecha_baja, usuario_baja) => {
  const [result] = await pool.execute(
    'UPDATE inscripciones SET fecha_baja = ?, usuario_baja = ? WHERE id = ? AND fecha_baja IS NULL',
    [fecha_baja, usuario_baja, id]
  );
  return result.affectedRows;
};

module.exports = { findById, findByAlumno, findDuplicate, create, softDelete };

const inscripcionRepo = require('../repositories/inscripcion.repository');
const usuarioRepo = require('../repositories/usuario.repository');
const materiaRepo = require('../repositories/materia.repository');
const { auditCreate, auditDelete } = require('../utils/audit');

/**
 * Crea una nueva inscripción.
 * Verifica:
 *  - Que el alumno exista y sea rol 'Alumno'
 *  - Que la materia exista
 *  - Que no haya una inscripción activa duplicada
 */
const create = async (data, actorUsuario) => {
  const { alumno_id, materia_id } = data;

  // Verificar que el alumno exista
  const alumno = await usuarioRepo.findById(alumno_id);
  if (!alumno) {
    const err = new Error('El alumno especificado no existe o está dado de baja.');
    err.statusCode = 404;
    throw err;
  }

  // Verificar que sea rol Alumno
  if (alumno.rol !== 'Alumno') {
    const err = new Error('Solo se pueden inscribir usuarios con rol Alumno.');
    err.statusCode = 400;
    throw err;
  }

  // Verificar que la materia exista
  const materia = await materiaRepo.findById(materia_id);
  if (!materia) {
    const err = new Error('La materia especificada no existe o está dada de baja.');
    err.statusCode = 404;
    throw err;
  }

  // Verificar que no esté ya inscripto
  const duplicado = await inscripcionRepo.findDuplicate(alumno_id, materia_id);
  if (duplicado) {
    const err = new Error('El alumno ya está inscripto en esta materia.');
    err.statusCode = 409;
    throw err;
  }

  const audit = auditCreate(actorUsuario);
  const id = await inscripcionRepo.create({ alumno_id, materia_id, ...audit });
  return inscripcionRepo.findById(id);
};

const getMateriasByAlumno = async (alumnoId, requestingUser) => {
  // Verificar que el alumno exista
  const alumno = await usuarioRepo.findById(alumnoId);
  if (!alumno) {
    const err = new Error('Alumno no encontrado.');
    err.statusCode = 404;
    throw err;
  }

  // Si el solicitante es Alumno, solo puede ver sus propias inscripciones
  if (requestingUser.rol === 'Alumno' && requestingUser.id !== parseInt(alumnoId)) {
    const err = new Error('Solo podés ver tus propias materias.');
    err.statusCode = 403;
    throw err;
  }

  return inscripcionRepo.findByAlumno(alumnoId);
};

const remove = async (id, requestingUser) => {
  const inscripcion = await inscripcionRepo.findById(id);
  if (!inscripcion || inscripcion.fecha_baja !== null) {
    const err = new Error('Inscripción no encontrada o ya dada de baja.');
    err.statusCode = 404;
    throw err;
  }

  // El alumno dueño de la inscripción o el admin pueden darla de baja
  const esAdmin = requestingUser.rol === 'Administrador';
  const esDuenio = requestingUser.id === inscripcion.alumno_id;

  if (!esAdmin && !esDuenio) {
    const err = new Error('No tenés permisos para dar de baja esta inscripción.');
    err.statusCode = 403;
    throw err;
  }

  const { fecha_baja, usuario_baja } = auditDelete(requestingUser.usuario);
  await inscripcionRepo.softDelete(id, fecha_baja, usuario_baja);
};

module.exports = { create, getMateriasByAlumno, remove };

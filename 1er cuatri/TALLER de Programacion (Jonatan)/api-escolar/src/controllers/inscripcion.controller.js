const inscripcionService = require('../services/inscripcion.service');
const { successResponse } = require('../utils/response');

/**
 * POST /inscripciones
 * Permitido: admin o el propio alumno.
 * La validación de permisos finos se hace en el service.
 */
const create = async (req, res, next) => {
  try {
    // Si el usuario es Alumno, forzamos que solo pueda inscribirse a sí mismo
    if (req.user.rol === 'Alumno') {
      req.body.alumno_id = req.user.id;
    }
    const data = await inscripcionService.create(req.body, req.user.usuario);
    return successResponse(res, 201, 'Inscripción realizada exitosamente.', data);
  } catch (error) { next(error); }
};

/**
 * GET /alumnos/:id/materias
 * Permitido: admin, coordinador, o el propio alumno.
 */
const getMateriasByAlumno = async (req, res, next) => {
  try {
    const data = await inscripcionService.getMateriasByAlumno(req.params.id, req.user);
    return successResponse(res, 200, 'Materias del alumno obtenidas.', data);
  } catch (error) { next(error); }
};

/**
 * DELETE /inscripciones/:id
 * Permitido: admin o el alumno dueño.
 */
const remove = async (req, res, next) => {
  try {
    await inscripcionService.remove(req.params.id, req.user);
    return successResponse(res, 200, 'Inscripción dada de baja correctamente.');
  } catch (error) { next(error); }
};

module.exports = { create, getMateriasByAlumno, remove };

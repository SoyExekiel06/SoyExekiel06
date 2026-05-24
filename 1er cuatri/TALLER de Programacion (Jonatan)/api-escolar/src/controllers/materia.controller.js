const materiaService = require('../services/materia.service');
const { successResponse } = require('../utils/response');

const getAll = async (req, res, next) => {
  try {
    const data = await materiaService.getAll();
    return successResponse(res, 200, 'Materias obtenidas.', data);
  } catch (error) { next(error); }
};

const getById = async (req, res, next) => {
  try {
    const data = await materiaService.getById(req.params.id);
    return successResponse(res, 200, 'Materia obtenida.', data);
  } catch (error) { next(error); }
};

const getAlumnosByMateria = async (req, res, next) => {
  try {
    const data = await materiaService.getAlumnosByMateria(req.params.id);
    return successResponse(res, 200, 'Alumnos de la materia obtenidos.', data);
  } catch (error) { next(error); }
};

const create = async (req, res, next) => {
  try {
    const data = await materiaService.create(req.body, req.user.usuario);
    return successResponse(res, 201, 'Materia creada exitosamente.', data);
  } catch (error) { next(error); }
};

const update = async (req, res, next) => {
  try {
    const data = await materiaService.update(req.params.id, req.body, req.user.usuario);
    return successResponse(res, 200, 'Materia actualizada.', data);
  } catch (error) { next(error); }
};

const remove = async (req, res, next) => {
  try {
    await materiaService.remove(req.params.id, req.user.usuario);
    return successResponse(res, 200, 'Materia dada de baja correctamente.');
  } catch (error) { next(error); }
};

module.exports = { getAll, getById, getAlumnosByMateria, create, update, remove };

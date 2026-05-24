const carreraService = require('../services/carrera.service');
const { successResponse } = require('../utils/response');

const getAll = async (req, res, next) => {
  try {
    const data = await carreraService.getAll();
    return successResponse(res, 200, 'Carreras obtenidas.', data);
  } catch (error) { next(error); }
};

const getById = async (req, res, next) => {
  try {
    const data = await carreraService.getById(req.params.id);
    return successResponse(res, 200, 'Carrera obtenida.', data);
  } catch (error) { next(error); }
};

const create = async (req, res, next) => {
  try {
    const data = await carreraService.create(req.body, req.user.usuario);
    return successResponse(res, 201, 'Carrera creada exitosamente.', data);
  } catch (error) { next(error); }
};

const update = async (req, res, next) => {
  try {
    const data = await carreraService.update(req.params.id, req.body, req.user.usuario);
    return successResponse(res, 200, 'Carrera actualizada.', data);
  } catch (error) { next(error); }
};

const remove = async (req, res, next) => {
  try {
    await carreraService.remove(req.params.id, req.user.usuario);
    return successResponse(res, 200, 'Carrera dada de baja correctamente.');
  } catch (error) { next(error); }
};

module.exports = { getAll, getById, create, update, remove };

const usuarioService = require('../services/usuario.service');
const { successResponse } = require('../utils/response');

const getAll = async (req, res, next) => {
  try {
    const data = await usuarioService.getAll();
    return successResponse(res, 200, 'Usuarios obtenidos.', data);
  } catch (error) { next(error); }
};

const getById = async (req, res, next) => {
  try {
    const data = await usuarioService.getById(req.params.id);
    return successResponse(res, 200, 'Usuario obtenido.', data);
  } catch (error) { next(error); }
};

const create = async (req, res, next) => {
  try {
    const data = await usuarioService.create(req.body, req.user.usuario);
    return successResponse(res, 201, 'Usuario creado exitosamente.', data);
  } catch (error) { next(error); }
};

const update = async (req, res, next) => {
  try {
    const data = await usuarioService.update(req.params.id, req.body, req.user.usuario);
    return successResponse(res, 200, 'Usuario actualizado.', data);
  } catch (error) { next(error); }
};

const remove = async (req, res, next) => {
  try {
    await usuarioService.remove(req.params.id, req.user.usuario);
    return successResponse(res, 200, 'Usuario dado de baja correctamente.');
  } catch (error) { next(error); }
};

module.exports = { getAll, getById, create, update, remove };

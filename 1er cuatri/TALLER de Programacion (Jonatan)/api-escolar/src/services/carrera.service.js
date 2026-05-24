const carreraRepo = require('../repositories/carrera.repository');
const { auditCreate, auditUpdate, auditDelete } = require('../utils/audit');

const getAll = async () => carreraRepo.findAll();

const getById = async (id) => {
  const carrera = await carreraRepo.findById(id);
  if (!carrera) {
    const err = new Error('Carrera no encontrada.');
    err.statusCode = 404;
    throw err;
  }
  return carrera;
};

const create = async (data, actorUsuario) => {
  const existe = await carreraRepo.findByNombre(data.nombre);
  if (existe) {
    const err = new Error(`Ya existe una carrera con el nombre '${data.nombre}'.`);
    err.statusCode = 409;
    throw err;
  }

  const audit = auditCreate(actorUsuario);
  const id = await carreraRepo.create({ ...data, ...audit });
  return carreraRepo.findById(id);
};

const update = async (id, data, actorUsuario) => {
  const existente = await carreraRepo.findById(id);
  if (!existente) {
    const err = new Error('Carrera no encontrada.');
    err.statusCode = 404;
    throw err;
  }

  const audit = auditUpdate(actorUsuario);
  await carreraRepo.update(id, { ...data, ...audit });
  return carreraRepo.findById(id);
};

const remove = async (id, actorUsuario) => {
  const existente = await carreraRepo.findById(id);
  if (!existente) {
    const err = new Error('Carrera no encontrada.');
    err.statusCode = 404;
    throw err;
  }

  const { fecha_baja, usuario_baja } = auditDelete(actorUsuario);
  await carreraRepo.softDelete(id, fecha_baja, usuario_baja);
};

module.exports = { getAll, getById, create, update, remove };

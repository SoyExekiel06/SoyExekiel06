const materiaRepo = require('../repositories/materia.repository');
const carreraRepo = require('../repositories/carrera.repository');
const { auditCreate, auditUpdate, auditDelete } = require('../utils/audit');

const getAll = async () => materiaRepo.findAll();

const getById = async (id) => {
  const materia = await materiaRepo.findById(id);
  if (!materia) {
    const err = new Error('Materia no encontrada.');
    err.statusCode = 404;
    throw err;
  }
  return materia;
};

const getAlumnosByMateria = async (materiaId) => {
  await getById(materiaId); // Valida que la materia exista
  return materiaRepo.findAlumnosByMateria(materiaId);
};

const create = async (data, actorUsuario) => {
  // Verificar que la carrera exista
  const carrera = await carreraRepo.findById(data.carrera_id);
  if (!carrera) {
    const err = new Error('La carrera especificada no existe o está dada de baja.');
    err.statusCode = 404;
    throw err;
  }

  const audit = auditCreate(actorUsuario);
  const id = await materiaRepo.create({ ...data, ...audit });
  return materiaRepo.findById(id);
};

const update = async (id, data, actorUsuario) => {
  const existente = await materiaRepo.findById(id);
  if (!existente) {
    const err = new Error('Materia no encontrada.');
    err.statusCode = 404;
    throw err;
  }

  // Si se cambia la carrera, verificar que la nueva exista
  if (data.carrera_id) {
    const carrera = await carreraRepo.findById(data.carrera_id);
    if (!carrera) {
      const err = new Error('La carrera especificada no existe o está dada de baja.');
      err.statusCode = 404;
      throw err;
    }
  }

  const audit = auditUpdate(actorUsuario);
  await materiaRepo.update(id, { ...data, ...audit });
  return materiaRepo.findById(id);
};

const remove = async (id, actorUsuario) => {
  const existente = await materiaRepo.findById(id);
  if (!existente) {
    const err = new Error('Materia no encontrada.');
    err.statusCode = 404;
    throw err;
  }

  const { fecha_baja, usuario_baja } = auditDelete(actorUsuario);
  await materiaRepo.softDelete(id, fecha_baja, usuario_baja);
};

module.exports = { getAll, getById, getAlumnosByMateria, create, update, remove };

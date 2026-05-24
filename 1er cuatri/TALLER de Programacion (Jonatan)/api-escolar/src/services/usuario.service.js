const bcrypt = require('bcryptjs');
const usuarioRepo = require('../repositories/usuario.repository');
const { auditCreate, auditUpdate, auditDelete } = require('../utils/audit');

/**
 * Servicio de usuarios.
 * Contiene toda la lógica de negocio relacionada a usuarios.
 */

const getAll = async () => {
  return usuarioRepo.findAll();
};

const getById = async (id) => {
  const usuario = await usuarioRepo.findById(id);
  if (!usuario) {
    const err = new Error('Usuario no encontrado.');
    err.statusCode = 404;
    throw err;
  }
  return usuario;
};

const create = async (data, actorUsuario) => {
  // Verificar unicidad de usuario
  const existeUsuario = await usuarioRepo.findByUsuario(data.usuario);
  if (existeUsuario) {
    const err = new Error(`El nombre de usuario '${data.usuario}' ya está en uso.`);
    err.statusCode = 409;
    throw err;
  }

  // Verificar unicidad de mail
  const existeMail = await usuarioRepo.findByMail(data.mail);
  if (existeMail) {
    const err = new Error(`El mail '${data.mail}' ya está registrado.`);
    err.statusCode = 409;
    throw err;
  }

  // Encriptar contraseña
  const saltRounds = parseInt(process.env.BCRYPT_SALT_ROUNDS) || 12;
  const passwordHash = await bcrypt.hash(data.password, saltRounds);

  const audit = auditCreate(actorUsuario);
  const id = await usuarioRepo.create({ ...data, password: passwordHash, ...audit });

  return usuarioRepo.findById(id);
};

const update = async (id, data, actorUsuario) => {
  // Verificar que el usuario a actualizar existe
  const existente = await usuarioRepo.findById(id);
  if (!existente) {
    const err = new Error('Usuario no encontrado.');
    err.statusCode = 404;
    throw err;
  }

  // Si viene nuevo mail, verificar que no esté en uso por otro usuario
  if (data.mail) {
    const [rows] = await require('../config/database').pool.execute(
      'SELECT id FROM usuarios WHERE mail = ? AND id != ? AND fecha_baja IS NULL',
      [data.mail, id]
    );
    if (rows.length > 0) {
      const err = new Error(`El mail '${data.mail}' ya está en uso por otro usuario.`);
      err.statusCode = 409;
      throw err;
    }
  }

  // Si viene nueva password, encriptarla
  if (data.password) {
    const saltRounds = parseInt(process.env.BCRYPT_SALT_ROUNDS) || 12;
    data.password = await bcrypt.hash(data.password, saltRounds);
  }

  const audit = auditUpdate(actorUsuario);
  await usuarioRepo.update(id, { ...data, ...audit });

  return usuarioRepo.findById(id);
};

const remove = async (id, actorUsuario) => {
  const existente = await usuarioRepo.findById(id);
  if (!existente) {
    const err = new Error('Usuario no encontrado.');
    err.statusCode = 404;
    throw err;
  }

  const { fecha_baja, usuario_baja } = auditDelete(actorUsuario);
  await usuarioRepo.softDelete(id, fecha_baja, usuario_baja);
};

module.exports = { getAll, getById, create, update, remove };

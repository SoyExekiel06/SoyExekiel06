const { body } = require('express-validator');

const createCarreraValidator = [
  body('nombre')
    .trim()
    .notEmpty().withMessage('El nombre de la carrera es obligatorio.')
    .isLength({ max: 150 }).withMessage('El nombre no puede superar 150 caracteres.'),
];

const updateCarreraValidator = [
  body('nombre')
    .optional()
    .trim()
    .notEmpty().withMessage('El nombre no puede estar vacío.')
    .isLength({ max: 150 }).withMessage('El nombre no puede superar 150 caracteres.'),
];

module.exports = { createCarreraValidator, updateCarreraValidator };

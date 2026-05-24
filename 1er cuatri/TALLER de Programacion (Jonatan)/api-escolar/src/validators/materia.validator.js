const { body } = require('express-validator');

const createMateriaValidator = [
  body('nombre')
    .trim()
    .notEmpty().withMessage('El nombre de la materia es obligatorio.')
    .isLength({ max: 150 }).withMessage('El nombre no puede superar 150 caracteres.'),

  body('carrera_id')
    .notEmpty().withMessage('La carrera es obligatoria.')
    .isInt({ min: 1 }).withMessage('El carrera_id debe ser un número entero positivo.'),
];

const updateMateriaValidator = [
  body('nombre')
    .optional()
    .trim()
    .notEmpty().withMessage('El nombre no puede estar vacío.')
    .isLength({ max: 150 }).withMessage('El nombre no puede superar 150 caracteres.'),

  body('carrera_id')
    .optional()
    .isInt({ min: 1 }).withMessage('El carrera_id debe ser un número entero positivo.'),
];

module.exports = { createMateriaValidator, updateMateriaValidator };

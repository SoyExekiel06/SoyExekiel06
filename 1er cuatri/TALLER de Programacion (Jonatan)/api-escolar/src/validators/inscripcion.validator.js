const { body } = require('express-validator');

const createInscripcionValidator = [
  body('alumno_id')
    .notEmpty().withMessage('El alumno_id es obligatorio.')
    .isInt({ min: 1 }).withMessage('El alumno_id debe ser un número entero positivo.'),

  body('materia_id')
    .notEmpty().withMessage('La materia_id es obligatoria.')
    .isInt({ min: 1 }).withMessage('La materia_id debe ser un número entero positivo.'),
];

module.exports = { createInscripcionValidator };

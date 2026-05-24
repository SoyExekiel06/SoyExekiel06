const { body } = require('express-validator');

const createUsuarioValidator = [
  body('nombre')
    .trim()
    .notEmpty().withMessage('El nombre es obligatorio.')
    .isLength({ max: 100 }).withMessage('El nombre no puede superar 100 caracteres.'),

  body('mail')
    .trim()
    .notEmpty().withMessage('El mail es obligatorio.')
    .isEmail().withMessage('El mail no tiene un formato válido.'),

  body('usuario')
    .trim()
    .notEmpty().withMessage('El campo usuario es obligatorio.')
    .isLength({ min: 3, max: 50 }).withMessage('El usuario debe tener entre 3 y 50 caracteres.')
    .matches(/^[a-zA-Z0-9._-]+$/).withMessage('El usuario solo puede contener letras, números, puntos, guiones y guiones bajos.'),

  body('password')
    .notEmpty().withMessage('La password es obligatoria.')
    .isLength({ min: 8 }).withMessage('La password debe tener al menos 8 caracteres.')
    .matches(/[A-Z]/).withMessage('La password debe incluir al menos una mayúscula.')
    .matches(/[0-9]/).withMessage('La password debe incluir al menos un número.'),

  body('rol_id')
    .notEmpty().withMessage('El rol es obligatorio.')
    .isInt({ min: 1 }).withMessage('El rol_id debe ser un número entero positivo.'),
];

const updateUsuarioValidator = [
  body('nombre')
    .optional()
    .trim()
    .notEmpty().withMessage('El nombre no puede estar vacío.')
    .isLength({ max: 100 }).withMessage('El nombre no puede superar 100 caracteres.'),

  body('mail')
    .optional()
    .trim()
    .isEmail().withMessage('El mail no tiene un formato válido.'),

  body('rol_id')
    .optional()
    .isInt({ min: 1 }).withMessage('El rol_id debe ser un número entero positivo.'),
];

module.exports = { createUsuarioValidator, updateUsuarioValidator };

const { body } = require('express-validator');

const loginValidator = [
  body('usuario')
    .trim()
    .notEmpty().withMessage('El campo usuario es obligatorio.'),
  body('password')
    .notEmpty().withMessage('El campo password es obligatorio.'),
];

module.exports = { loginValidator };

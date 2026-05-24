const { Router } = require('express');
const authController = require('../controllers/auth.controller');
const { loginValidator } = require('../validators/auth.validator');
const { validateRequest } = require('../middlewares/validate.middleware');

const router = Router();

// POST /auth/login
router.post('/login', loginValidator, validateRequest, authController.login);

module.exports = router;

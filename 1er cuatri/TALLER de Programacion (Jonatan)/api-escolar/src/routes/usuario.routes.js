const { Router } = require('express');
const usuarioController = require('../controllers/usuario.controller');
const { verifyToken, authorizeRoles } = require('../middlewares/auth.middleware');
const { createUsuarioValidator, updateUsuarioValidator } = require('../validators/usuario.validator');
const { validateRequest } = require('../middlewares/validate.middleware');

const router = Router();

// Todas las rutas de usuarios requieren autenticación
router.use(verifyToken);

// Solo admin puede gestionar usuarios
router.get('/',    authorizeRoles('Administrador'), usuarioController.getAll);
router.get('/:id', authorizeRoles('Administrador'), usuarioController.getById);
router.post('/',   authorizeRoles('Administrador'), createUsuarioValidator, validateRequest, usuarioController.create);
router.put('/:id', authorizeRoles('Administrador'), updateUsuarioValidator, validateRequest, usuarioController.update);
router.delete('/:id', authorizeRoles('Administrador'), usuarioController.remove);

module.exports = router;

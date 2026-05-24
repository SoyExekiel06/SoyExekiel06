const { Router } = require('express');
const carreraController = require('../controllers/carrera.controller');
const { verifyToken, authorizeRoles } = require('../middlewares/auth.middleware');
const { createCarreraValidator, updateCarreraValidator } = require('../validators/carrera.validator');
const { validateRequest } = require('../middlewares/validate.middleware');

const router = Router();

router.use(verifyToken);

// Lectura: admin y coordinador
router.get('/',    authorizeRoles('Administrador', 'Coordinador'), carreraController.getAll);
router.get('/:id', authorizeRoles('Administrador', 'Coordinador'), carreraController.getById);

// Escritura: solo admin
router.post('/',      authorizeRoles('Administrador'), createCarreraValidator, validateRequest, carreraController.create);
router.put('/:id',    authorizeRoles('Administrador'), updateCarreraValidator, validateRequest, carreraController.update);
router.delete('/:id', authorizeRoles('Administrador'), carreraController.remove);

module.exports = router;

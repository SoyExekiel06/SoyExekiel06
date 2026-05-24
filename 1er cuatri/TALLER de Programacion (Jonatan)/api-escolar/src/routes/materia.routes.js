const { Router } = require('express');
const materiaController = require('../controllers/materia.controller');
const { verifyToken, authorizeRoles } = require('../middlewares/auth.middleware');
const { createMateriaValidator, updateMateriaValidator } = require('../validators/materia.validator');
const { validateRequest } = require('../middlewares/validate.middleware');

const router = Router();

router.use(verifyToken);

// Lectura: todos los roles autenticados
router.get('/',    materiaController.getAll);
router.get('/:id', materiaController.getById);

// Alumnos de una materia: solo admin y coordinador
router.get('/:id/alumnos', authorizeRoles('Administrador', 'Coordinador'), materiaController.getAlumnosByMateria);

// Escritura: solo admin
router.post('/',      authorizeRoles('Administrador'), createMateriaValidator, validateRequest, materiaController.create);
router.put('/:id',    authorizeRoles('Administrador'), updateMateriaValidator, validateRequest, materiaController.update);
router.delete('/:id', authorizeRoles('Administrador'), materiaController.remove);

module.exports = router;

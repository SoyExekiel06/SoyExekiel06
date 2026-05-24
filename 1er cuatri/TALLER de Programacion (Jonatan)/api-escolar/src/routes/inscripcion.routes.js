const { Router } = require('express');
const inscripcionController = require('../controllers/inscripcion.controller');
const { verifyToken, authorizeRoles } = require('../middlewares/auth.middleware');
const { createInscripcionValidator } = require('../validators/inscripcion.validator');
const { validateRequest } = require('../middlewares/validate.middleware');

const router = Router();

router.use(verifyToken);

// POST /inscripciones → admin o alumno (el service controla que el alumno solo pueda inscribirse a sí mismo)
router.post(
  '/',
  authorizeRoles('Administrador', 'Alumno'),
  createInscripcionValidator,
  validateRequest,
  inscripcionController.create
);

// DELETE /inscripciones/:id → admin o alumno dueño (controlado en el service)
router.delete('/:id', authorizeRoles('Administrador', 'Alumno'), inscripcionController.remove);

module.exports = router;

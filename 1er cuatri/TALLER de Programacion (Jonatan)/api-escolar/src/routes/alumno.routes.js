const { Router } = require('express');
const inscripcionController = require('../controllers/inscripcion.controller');
const { verifyToken, authorizeRoles } = require('../middlewares/auth.middleware');

const router = Router();

router.use(verifyToken);

// GET /alumnos/:id/materias → admin, coordinador, o el propio alumno (controlado en el service)
router.get(
  '/:id/materias',
  authorizeRoles('Administrador', 'Coordinador', 'Alumno'),
  inscripcionController.getMateriasByAlumno
);

module.exports = router;

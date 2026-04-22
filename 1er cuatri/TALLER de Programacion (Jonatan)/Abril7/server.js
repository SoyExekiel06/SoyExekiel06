// ============================================
// SERVIDOR BÁSICO CON NODE.JS Y EXPRESS
// ============================================

const express = require("express");

// 2. CREAR LA APLICACIÓN
const app = express();

// 3. PUERTO
const PORT = 3000;

// ============================================
// MIDDLEWARES (funciones que se ejecutan antes de las rutas)
// ============================================

// Permite que el servidor entienda JSON en el body de las requests
// Sin esto, req.body estaría vacío en las rutas POST
app.use(express.json());

// ============================================
// RUTAS
// ============================================

// RUTA 1: GET /
// Responde con texto plano cuando alguien visita la raíz
app.get("/", (req, res) => {
  res.send("Servidor funcionando");
});

// RUTA 2: GET /api/saludo
app.get("/api/saludo", (req, res) => {
  // res.json() convierte el objeto a JSON y lo envía
  res.json({ mensaje: "Hola mundo" });
});

// RUTA 3: POST /api/datos
// Recibe JSON y lo devuelve exactamente igual (echo)
app.post("/api/datos", (req, res) => {
  // req.body contiene el JSON que mandó el cliente
  const datosRecibidos = req.body;

  // Lo devolvemos tal cual
  res.json(datosRecibidos);
});

// ============================================
// INICIAR EL SERVIDOR
// ============================================

// app.listen() arranca el servidor en el puerto indicado
// El callback se ejecuta cuando el servidor ya está listo
app.listen(PORT, () => {
  console.log(`✅ Servidor corriendo en http://localhost:${PORT}`);
  console.log(`   GET  /           → texto plano`);
  console.log(`   GET  /api/saludo → JSON con saludo`);
  console.log(`   POST /api/datos  → echo del JSON recibido`);
});
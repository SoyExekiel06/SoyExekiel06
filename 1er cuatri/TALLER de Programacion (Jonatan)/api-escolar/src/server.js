require('dotenv').config(); // Cargar .env PRIMERO, antes de cualquier otra importación

const app = require('./app');
const { testConnection } = require('./config/database');

const PORT = process.env.PORT || 3000;

/**
 * Arranca el servidor solo si la conexión a la DB es exitosa.
 * Esto previene que la API esté corriendo con la DB caída.
 */
const startServer = async () => {
  try {
    await testConnection();

    app.listen(PORT, () => {
      console.log(`Servidor corriendo en http://localhost:${PORT}`);
      console.log(`Ambiente: ${process.env.NODE_ENV || 'development'}`);
      console.log(`Health check: http://localhost:${PORT}/health`);
    });
  } catch (error) {
    console.error('Error al iniciar el servidor:', error.message);
    process.exit(1);
  }
};

// Manejo de errores no capturados (seguridad: evita que el proceso muera silenciosamente)
process.on('unhandledRejection', (reason) => {
  console.error('Unhandled Promise Rejection:', reason);
  process.exit(1);
});

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  process.exit(1);
});

startServer();

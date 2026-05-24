const mysql = require('mysql2/promise');

/**
 * Pool de conexiones MySQL.
 * Usar pool en lugar de conexiones individuales mejora el rendimiento
 * y evita agotar los recursos del servidor de base de datos.
 */
const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT) || 3306,
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'api_escolar',
  waitForConnections: true,
  connectionLimit: parseInt(process.env.DB_CONNECTION_LIMIT) || 10,
  queueLimit: 0,
  // Retorna objetos simples en lugar de RowDataPacket
  // para mayor comodidad al serializar a JSON
  decimalNumbers: true,
});

/**
 * Verifica la conectividad con la base de datos al inicio.
 * Lanza error si no se puede conectar, evitando que la app arranque rota.
 */
const testConnection = async () => {
  try {
    const connection = await pool.getConnection();
    console.log('Conexión a MySQL establecida correctamente.');
    connection.release();
  } catch (error) {
    console.error('Error al conectar con MySQL:', error.message);
    process.exit(1); // Detiene el proceso si no hay DB
  }
};

module.exports = { pool, testConnection };

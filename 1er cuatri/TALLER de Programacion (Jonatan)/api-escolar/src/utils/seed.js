require('dotenv').config();
const bcrypt = require('bcryptjs');
const { pool, testConnection } = require('../config/database');

/**
 * Script de seed para poblar la base de datos con datos iniciales.
 * Ejecutar con: npm run seed
 * IMPORTANTE: Solo ejecutar una vez o en entornos de desarrollo.
 */
const seed = async () => {
  await testConnection();
  const conn = await pool.getConnection();

  try {
    await conn.beginTransaction();

    // -- Roles
    console.log('Insertando roles...');
    await conn.execute(`
      INSERT IGNORE INTO roles (id, nombre) VALUES
        (1, 'Administrador'),
        (2, 'Coordinador'),
        (3, 'Alumno')
    `);

    // -- Admin por defecto 
    console.log('Insertando usuario administrador...');
    const saltRounds = parseInt(process.env.BCRYPT_SALT_ROUNDS) || 12;
    const passwordHash = await bcrypt.hash('Admin1234!', saltRounds);
    const now = new Date();

    await conn.execute(`
      INSERT IGNORE INTO usuarios
        (nombre, mail, usuario, password, rol_id, fecha_alta, usuario_alta)
      VALUES
        (?, ?, ?, ?, ?, ?, ?)
    `, ['Administrador Sistema', 'admin@escuela.com', 'admin', passwordHash, 1, now, 'seed']);

    // -- Carreras de ejemplo 
    console.log('Insertando carreras...');
    await conn.execute(`
      INSERT IGNORE INTO carreras (nombre, fecha_alta, usuario_alta) VALUES
        ('Ingeniería en Sistemas', ?, 'seed'),
        ('Licenciatura en Matemáticas', ?, 'seed'),
        ('Tecnicatura en Programación', ?, 'seed')
    `, [now, now, now]);

    // -- Materias de ejemplo 
    console.log('Insertando materias...');
    const [carreras] = await conn.execute('SELECT id FROM carreras WHERE fecha_baja IS NULL LIMIT 1');
    const carreraId = carreras[0]?.id || 1;

    await conn.execute(`
      INSERT IGNORE INTO materias (nombre, carrera_id, fecha_alta, usuario_alta) VALUES
        ('Algoritmos y Estructuras de Datos', ?, ?, 'seed'),
        ('Bases de Datos', ?, ?, 'seed'),
        ('Programación Orientada a Objetos', ?, ?, 'seed'),
        ('Redes y Comunicaciones', ?, ?, 'seed')
    `, [carreraId, now, carreraId, now, carreraId, now, carreraId, now]);

    // -- Alumno de ejemplo 
    console.log('Insertando alumno de prueba...');
    const alumnoHash = await bcrypt.hash('Alumno1234!', saltRounds);
    await conn.execute(`
      INSERT IGNORE INTO usuarios
        (nombre, mail, usuario, password, rol_id, fecha_alta, usuario_alta)
      VALUES
        (?, ?, ?, ?, ?, ?, ?)
    `, ['Juan Pérez', 'juan@mail.com', 'jperez', alumnoHash, 3, now, 'seed']);

    await conn.commit();
    console.log('Seed completado exitosamente.');
    console.log('');
    console.log('Credenciales de acceso:');
    console.log('   Admin  → usuario: admin     | password: Admin1234!');
    console.log('   Alumno → usuario: jperez    | password: Alumno1234!');
  } catch (error) {
    await conn.rollback();
    console.error('Error en seed:', error.message);
    throw error;
  } finally {
    conn.release();
    pool.end();
  }
};

seed().catch(() => process.exit(1));

-- ============================================================
--  API ESCOLAR - Script de base de datos
--  MySQL 8.0+
--  Ejecutar con: mysql -u root -p < database/schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS api_escolar
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE api_escolar;

-- ─── ROLES ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS roles (
  id     INT          NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(50)  NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_roles_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── USUARIOS ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS usuarios (
  id                   INT           NOT NULL AUTO_INCREMENT,
  nombre               VARCHAR(100)  NOT NULL,
  mail                 VARCHAR(150)  NOT NULL,
  usuario              VARCHAR(50)   NOT NULL,
  password             VARCHAR(255)  NOT NULL,
  rol_id               INT           NOT NULL,

  -- Auditoría
  fecha_alta           DATETIME      NOT NULL,
  usuario_alta         VARCHAR(50)   NOT NULL,
  fecha_modificacion   DATETIME      DEFAULT NULL,
  usuario_modificacion VARCHAR(50)   DEFAULT NULL,
  fecha_baja           DATETIME      DEFAULT NULL,
  usuario_baja         VARCHAR(50)   DEFAULT NULL,

  PRIMARY KEY (id),
  UNIQUE KEY uq_usuarios_usuario (usuario),
  UNIQUE KEY uq_usuarios_mail    (mail),
  CONSTRAINT fk_usuarios_rol FOREIGN KEY (rol_id) REFERENCES roles(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── CARRERAS ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS carreras (
  id                   INT           NOT NULL AUTO_INCREMENT,
  nombre               VARCHAR(150)  NOT NULL,

  -- Auditoría
  fecha_alta           DATETIME      NOT NULL,
  usuario_alta         VARCHAR(50)   NOT NULL,
  fecha_modificacion   DATETIME      DEFAULT NULL,
  usuario_modificacion VARCHAR(50)   DEFAULT NULL,
  fecha_baja           DATETIME      DEFAULT NULL,
  usuario_baja         VARCHAR(50)   DEFAULT NULL,

  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── MATERIAS ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS materias (
  id                   INT           NOT NULL AUTO_INCREMENT,
  nombre               VARCHAR(150)  NOT NULL,
  carrera_id           INT           NOT NULL,

  -- Auditoría
  fecha_alta           DATETIME      NOT NULL,
  usuario_alta         VARCHAR(50)   NOT NULL,
  fecha_modificacion   DATETIME      DEFAULT NULL,
  usuario_modificacion VARCHAR(50)   DEFAULT NULL,
  fecha_baja           DATETIME      DEFAULT NULL,
  usuario_baja         VARCHAR(50)   DEFAULT NULL,

  PRIMARY KEY (id),
  CONSTRAINT fk_materias_carrera FOREIGN KEY (carrera_id) REFERENCES carreras(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── INSCRIPCIONES ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS inscripciones (
  id                   INT       NOT NULL AUTO_INCREMENT,
  alumno_id            INT       NOT NULL,
  materia_id           INT       NOT NULL,

  -- Auditoría
  fecha_alta           DATETIME  NOT NULL,
  usuario_alta         VARCHAR(50) NOT NULL,
  fecha_modificacion   DATETIME  DEFAULT NULL,
  usuario_modificacion VARCHAR(50) DEFAULT NULL,
  fecha_baja           DATETIME  DEFAULT NULL,
  usuario_baja         VARCHAR(50) DEFAULT NULL,

  PRIMARY KEY (id),
  -- Índice único parcial: evita duplicados solo en inscripciones activas.
  -- NOTA: MySQL no soporta índices parciales nativos con WHERE,
  -- pero la lógica de duplicados se maneja en la capa de servicio.
  CONSTRAINT fk_inscripciones_alumno  FOREIGN KEY (alumno_id)  REFERENCES usuarios(id),
  CONSTRAINT fk_inscripciones_materia FOREIGN KEY (materia_id) REFERENCES materias(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── DATOS INICIALES: ROLES ───────────────────────────────────
INSERT INTO roles (id, nombre) VALUES
  (1, 'Administrador'),
  (2, 'Coordinador'),
  (3, 'Alumno')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

-- ============================================================
--  FIN DEL SCRIPT
--  Después de ejecutar esto, correr: npm run seed
--  para cargar datos de prueba y el usuario admin.
-- ============================================================

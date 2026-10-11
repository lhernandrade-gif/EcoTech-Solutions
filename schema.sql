-- Esquema base generado con IA, luego modificado para el caso específico de EcoTech Solutions.

-- ============================================================
-- Configuración de la Base de Datos
-- ============================================================

DROP DATABASE IF EXISTS ecotech;

CREATE DATABASE ecotech
    CHARACTER SET utf8mb4 -- Establece compatibilidad extendida con caracteres Unicode
    COLLATE utf8mb4_0900_ai_ci; -- Esta línea permite comparar valores sin importar las tildes o capitalización (por ej. un usuario que busca "jose" puede encontrar "José")

USE ecotech;


-- ============================================================
-- Tabla: empleados
-- ============================================================

CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,

    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50) NULL,

    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50) NOT NULL,

    rut VARCHAR(12) NOT NULL,

    direccion VARCHAR(255) NULL,
    telefono VARCHAR(30) NULL,

    email VARCHAR(255) NOT NULL,

    fecha_inicio_contrato DATE NULL,

    salario INT NULL,

    CONSTRAINT uq_empleados_rut
        UNIQUE (rut),

    CONSTRAINT uq_empleados_email
        UNIQUE (email),

    CONSTRAINT chk_empleados_salario
        CHECK (salario IS NULL OR salario >= 0)
);


-- ============================================================
-- Datos de Prueba
-- ============================================================

INSERT INTO empleados (
    primer_nombre,
    segundo_nombre,
    primer_apellido,
    segundo_apellido,
    rut,
    direccion,
    telefono,
    email,
    fecha_inicio_contrato,
    salario
)
VALUES
(
    'José',
    'Carlos',
    'Pérez',
    'González',
    '12345678-9',
    'Av. Calle 123',
    '+56 9 1234 5678',
    'jose.perez@ejemplo.cl',
    '2026-01-15',
    800000
);

-- ============================================================
-- Verificación Básica
-- ============================================================

SELECT * FROM empleados;
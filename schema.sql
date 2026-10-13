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
    empleado_id INT AUTO_INCREMENT PRIMARY KEY,

    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),

    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50) NOT NULL,

    rut VARCHAR(12) NOT NULL,

    direccion VARCHAR(255),
    telefono VARCHAR(30),

    email VARCHAR(255) NOT NULL,

    fecha_inicio_contrato DATE,

    salario INT,

    CONSTRAINT uq_empleados_rut
        UNIQUE (rut),

    CONSTRAINT uq_empleados_email
        UNIQUE (email),

    CONSTRAINT chk_empleados_salario
        CHECK (salario IS NULL OR salario >= 0)
);

-- ============================================================
-- Datos de Prueba: empleados (5 registros)
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
    960000
),
(
    'Francisca',
    'Andrea',
    'Soto',
    'Muñoz',
    '18456789-2',
    'Av. Providencia 1450, Santiago',
    '+56 9 2345 6789',
    'maria.soto@ejemplo.cl',
    '2025-08-01',
    920000
),
(
    'Pedro',
    NULL,
    'Contreras',
    'Rojas',
    '16789432-5',
    'Los Robles 456, Valparaíso',
    '+56 9 3456 7890',
    'juan.contreras@ejemplo.cl',
    '2024-11-10',
    800000
),
(
    'Camila',
    'Fernanda',
    'Fuentes',
    'Silva',
    '20567891-3',
    'Av. Alemania 890, Temuco',
    '+56 9 4567 8901',
    'camila.fuentes@ejemplo.cl',
    '2026-03-01',
    860000
),
(
    'David',
    'Ignacio',
    'Vargas',
    'Ojeda',
    '19234567-8',
    'Av. España 321, Concepción',
    '+56 9 5678 9012',
    'diego.morales@ejemplo.cl',
    '2025-05-20',
    820000
);

-- ============================================================
-- Verificación Básica
-- ============================================================

SELECT * FROM empleados;

-- ============================================================
-- Tabla: proyectos
-- ============================================================

CREATE TABLE proyectos (
    proyecto_id INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(150),
    descripcion TEXT,
    fecha_proyecto DATE
);

-- ===================================================================
-- Tabla: proyecto_empleados
-- Tabla asociativa para la relación entre proyectos y empleados (N:M)
-- ===================================================================

CREATE TABLE proyecto_empleados (
    proyecto_id INT NOT NULL,
    empleado_id INT NOT NULL,

    PRIMARY KEY (proyecto_id, empleado_id),

    CONSTRAINT fk_proyecto_empleados_proyecto
        FOREIGN KEY (proyecto_id)
        REFERENCES proyectos(proyecto_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_proyecto_empleados_empleado
        FOREIGN KEY (empleado_id)
        REFERENCES empleados(empleado_id)
        ON DELETE CASCADE
);


-- ============================================================
-- Datos de prueba: proyectos (5 registros)
-- ============================================================

INSERT INTO proyectos (
    nombre,
    descripcion,
    fecha_proyecto
)
VALUES
(
    'Plataforma de Reciclaje Inteligente',
    'Desarrollo de una plataforma para gestionar puntos de reciclaje y monitorear los materiales recolectados.',
    '2026-01-20'
),
(
    'Monitoreo Energético Solar',
    'Implementación de un sistema para registrar y analizar la generación de energía mediante paneles solares.',
    '2026-02-15'
),
(
    'Gestión de Residuos Electrónicos',
    'Diseño de una solución para registrar, clasificar y gestionar residuos de aparatos electrónicos.',
    '2026-03-10'
),
(
    'Sensores Ambientales IoT',
    'Instalación de sensores conectados para medir la calidad del aire y la temperatura en espacios urbanos.',
    '2026-04-05'
),
(
    'Optimización del Consumo de Agua',
    'Desarrollo de un sistema de seguimiento del consumo de agua para detectar pérdidas y promover el ahorro.',
    '2026-05-12'
);

-- ============================================================
-- Datos de prueba: empleados asignados a proyectos
-- ============================================================

INSERT INTO proyecto_empleados (
    proyecto_id,
    empleado_id
)
VALUES
(1, 1),
(1, 2),
(2, 2),
(2, 3),
(3, 1),
(3, 4),
(4, 3),
(4, 5),
(5, 4),
(5, 5);

-- ============================================================
-- Verificación
-- ============================================================

SELECT * FROM proyectos;

SELECT * FROM proyecto_empleados;

SELECT
    p.proyecto_id,
    p.nombre AS proyecto,
    p.fecha_proyecto,
    e.empleado_id AS empleado_id,
    CONCAT(
        e.primer_nombre, ' ',
        e.primer_apellido, ' ',
        e.segundo_apellido
    ) AS empleado
FROM proyectos p
LEFT JOIN proyecto_empleados pe
    ON p.proyecto_id = pe.proyecto_id
LEFT JOIN empleados e
    ON pe.empleado_id = e.empleado_id
ORDER BY p.proyecto_id, e.empleado_id;

-- ============================================================
-- Tabla: departamentos
-- ============================================================

CREATE TABLE departamentos (
    departamento_id INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100),

    gerente INT,

    CONSTRAINT uq_departamentos_nombre
        UNIQUE (nombre),

    CONSTRAINT fk_departamentos_gerente
        FOREIGN KEY (gerente)
        REFERENCES empleados(empleado_id)
        ON DELETE SET NULL
);

-- ============================================================
-- Tabla: departamento_empleados
-- ============================================================

CREATE TABLE departamento_empleados (
    departamento_id INT NOT NULL,
    empleado_id INT NOT NULL,

    PRIMARY KEY (departamento_id, empleado_id),

    -- Cada empleado pertenece a un solo departamento
    CONSTRAINT uq_departamento_empleados_empleado
        UNIQUE (empleado_id),

    CONSTRAINT fk_departamento_empleados_departamento
        FOREIGN KEY (departamento_id)
        REFERENCES departamentos(departamento_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_departamento_empleados_empleado
        FOREIGN KEY (empleado_id)
        REFERENCES empleados(empleado_id)
        ON DELETE CASCADE
);

-- ============================================================
-- Datos de prueba: departamentos (2 registros)
-- ============================================================

INSERT INTO departamentos (
    nombre,
    gerente
)
VALUES
(
    'Tecnología e Innovación',
    1
),
(
    'Gestión Ambiental',
    4
);

-- ============================================================
-- Datos de prueba: asignación de empleados
-- ============================================================

INSERT INTO departamento_empleados (
    departamento_id,
    empleado_id
)
VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 4),
(2, 5);

-- ============================================================
-- Verificación
-- ============================================================

SELECT * FROM departamentos;

SELECT * FROM departamento_empleados;

-- ============================================================
-- Consulta: departamentos, gerentes y empleados
-- ============================================================

SELECT
    d.departamento_id,
    d.nombre AS departamento,
    CONCAT(
        g.primer_nombre, ' ',
        g.primer_apellido, ' ',
        g.segundo_apellido
    ) AS gerente,
    e.empleado_id AS empleado_id,
    CONCAT(
        e.primer_nombre, ' ',
        e.primer_apellido, ' ',
        e.segundo_apellido
    ) AS empleado
FROM departamentos d
LEFT JOIN empleados g
    ON d.gerente = g.empleado_id
LEFT JOIN departamento_empleados de
    ON d.departamento_id = de.departamento_id
LEFT JOIN empleados e
    ON de.empleado_id = e.empleado_id
ORDER BY d.departamento_id, e.empleado_id;

-- ============================================================
-- Tabla: registro_tiempo
-- ============================================================

CREATE TABLE registro_tiempo (
    registro_tiempo_id INT AUTO_INCREMENT PRIMARY KEY,

    fecha DATE NOT NULL,

    horas_trabajadas DECIMAL(4,2) NOT NULL,

    descripcion_tareas TEXT,

    empleado_id INT NOT NULL,

    proyecto_id INT NOT NULL,

    CONSTRAINT chk_registro_tiempo_horas
        CHECK (
            horas_trabajadas > 0
            AND horas_trabajadas <= 24
        ),

    CONSTRAINT fk_registro_tiempo_empleado
        FOREIGN KEY (empleado_id)
        REFERENCES empleados(empleado_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_registro_tiempo_proyecto
        FOREIGN KEY (proyecto_id)
        REFERENCES proyectos(proyecto_id)
        ON DELETE CASCADE
);

-- ============================================================
-- Datos de prueba: registro_tiempo (8 registros)
-- ============================================================

INSERT INTO registro_tiempo (
    fecha,
    horas_trabajadas,
    descripcion_tareas,
    empleado_id,
    proyecto_id
)
VALUES
(
    '2026-06-01',
    6.50,
    'Diseño inicial de la arquitectura de la plataforma de reciclaje.',
    1,
    1
),
(
    '2026-06-02',
    4.00,
    'Desarrollo de módulos para el registro de puntos de reciclaje.',
    2,
    1
),
(
    '2026-06-03',
    5.50,
    'Pruebas de integración y corrección de errores de la plataforma.',
    3,
    1
),
(
    '2026-06-04',
    7.00,
    'Análisis de datos de generación energética de paneles solares.',
    2,
    2
),
(
    '2026-06-05',
    3.50,
    'Documentación de los sensores utilizados para medir la energía.',
    3,
    2
),
(
    '2026-06-08',
    6.00,
    'Clasificación de residuos electrónicos y diseño del flujo de gestión.',
    1,
    3
),
(
    '2026-06-09',
    5.00,
    'Configuración y calibración de sensores ambientales IoT.',
    4,
    4
),
(
    '2026-06-10',
    4.50,
    'Análisis del consumo de agua y elaboración de propuestas de ahorro.',
    5,
    5
);

-- ============================================================
-- Verificación básica
-- ============================================================

SELECT * FROM registro_tiempo;

-- ============================================================
-- Consulta: registros con nombres de empleados y proyectos
-- ============================================================

SELECT
    rt.registro_tiempo_id,
    rt.fecha,
    rt.horas_trabajadas,
    rt.descripcion_tareas,
    rt.empleado_id,
    CONCAT(
        e.primer_nombre, ' ',
        e.primer_apellido, ' ',
        e.segundo_apellido
    ) AS empleado,
    rt.proyecto_id,
    p.nombre AS proyecto
FROM registro_tiempo rt
INNER JOIN empleados e
    ON rt.empleado_id = e.empleado_id
INNER JOIN proyectos p
    ON rt.proyecto_id = p.proyecto_id
ORDER BY rt.fecha, rt.registro_tiempo_id;
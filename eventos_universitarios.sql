
-- Nombre: Diego Valle Cuevas
-- Grupo: 952
-- Fecha: 11/10/2026
-- Meta 2.3 Desarrollar aplicaciones con conexion a Base de Datos.
-- Script para crear la base de datos eventos_universitarios, la tabla eventos y registrar los eventos de prueba.
-- Se corre una sola vez en MySQL (Workbench o terminal) antes de ejecutar el programa de Python.


-- Paso 2. Creamos la base de datos. El IF NOT EXISTS es para que no marque error si ya existia
CREATE DATABASE IF NOT EXISTS eventos_universitarios;

-- Le decimos a MySQL que todo lo que sigue se hace dentro de esta base de datos
USE eventos_universitarios;


-- Paso 3. Creamos la tabla eventos
-- id: INT con AUTO_INCREMENT para que MySQL le ponga el numero solito y es la clave primaria
-- nombre y lugar: VARCHAR porque son textos de largo variable
-- fecha: DATE (AAAA-MM-DD) y hora: TIME (HH:MM:SS)
-- cupo y registrados: INT porque son cantidades de personas
-- registrados empieza en 0 con DEFAULT, y los CHECK son para que nunca haya mas registrados que cupo
CREATE TABLE IF NOT EXISTS eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    lugar VARCHAR(100) NOT NULL,
    cupo INT NOT NULL,
    registrados INT NOT NULL DEFAULT 0,
    CHECK (cupo > 0),
    CHECK (registrados >= 0 AND registrados <= cupo)
);


-- Paso 4. Registramos los eventos de diferentes tipos, con diferentes fechas, horarios, lugares y capacidades.
-- Pusimos uno lleno (Power BI) y dos que ya pasaron para poder probar las opciones de disponibilidad y proximos.
INSERT INTO eventos (nombre, fecha, hora, lugar, cupo, registrados) VALUES
    ('Conferencia: Inteligencia Artificial en los Negocios', '2026-10-15', '10:00:00', 'Auditorio FCA', 150, 120),
    ('Taller de Power BI desde Cero', '2026-10-17', '16:00:00', 'Laboratorio de Computo 3', 30, 30),
    ('Curso de Python para Analisis de Datos', '2026-10-20', '09:00:00', 'Laboratorio de Computo 1', 25, 18),
    ('Seminario de Emprendimiento e Innovacion', '2026-10-22', '12:00:00', 'Sala Audiovisual', 80, 45),
    ('Festival Cultural de Dia de Muertos', '2026-10-31', '18:00:00', 'Explanada Central', 300, 210),
    ('Torneo Interfacultades de Futbol', '2026-11-07', '08:00:00', 'Cancha de Futbol Campus Otay', 200, 96),
    ('Taller de SQL Avanzado', '2026-11-12', '15:00:00', 'Laboratorio de Computo 2', 35, 12),
    ('Presentacion de Proyectos Integradores', '2026-11-25', '11:00:00', 'Auditorio FCA', 100, 85),
    ('Conferencia de Ciberseguridad', '2026-10-05', '10:00:00', 'Sala Audiovisual', 80, 72),
    ('Carrera Atletica 5K UABC', '2026-09-27', '07:00:00', 'Gimnasio Campus Otay', 250, 180);


-- Revisamos que si se hayan guardado
SELECT * FROM eventos;

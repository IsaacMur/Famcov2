CREATE DATABASE famco;

USE famco;

CREATE TABLE usuarios (
    id_usuario bigint AUTO_INCREMENT primary key,
    nombre_usuario varchar(50) NOT NULL,
    contrasenia_usuario varchar(255) NOT NULL 
);


CREATE TABLE categoria (
    id_categoria bigint AUTO_INCREMENT primary key,
    nombre_categoria varchar(200) NOT NULL
);


CREATE TABLE productos (
    -- Agregar campo de (Marca)
    id_producto bigint AUTO_INCREMENT primary key,
    nombre_producto varchar(200) NOT NULL,
    precio_producto double NOT NULL,
    descripcion_producto text NOT NULL,
    codigo_producto int NOT NULL,
    stock_producto int NOT NULL,
    informacion_adicional text NOT NULL,
    imagen_producto longblob NOT NULL,
    oferta_producto BOOLEAN NOT NULL,
    id_categoria bigint,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);



SELECT * FROM usuarios;

SELECT * FROM productos;

SELECT * FROM categoria

INSERT INTO usuarios (nombre_usuario, contrasenia_usuario)
VALUES ('admin', 'scrypt:32768:8:1$qmPYGaZJluPGeq5F$a51017f52ceb09d944baa87bf9a9a6317bbcc322ff518834e515bb5bb9daf09c91c82957806bddfcedbf2f89f8b8f8f0d3841d7866f2e845f0bd39f895c3ef0a');

INSERT INTO categoria (nombre_categoria)
VALUES 
    ('Instrumental Quirúrgico'),
    ('Equipos de Diagnóstico'),
    ('Material de Curación'),
    ('Suministros para Laboratorio'),
    ('Mobiliario Médico'),
    ('Prótesis y Ortopedia'),
    ('Terapia Respiratoria'),
    ('Equipos de Rehabilitación'),
    ('Descartables Médicos'),
    ('Ropa y Uniformes Médicos'),
    ('Productos de Higiene y Cuidado Personal'),
    ('Medicamentos de Venta Libre'),
    ('Equipos de Monitoreo'),
    ('Accesorios Médicos'),
    ('Equipos de Imagenología');


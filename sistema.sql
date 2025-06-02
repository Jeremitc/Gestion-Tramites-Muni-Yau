

-- Tabla de tipos de trámites
CREATE TABLE tipos_tramite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    tiempo_promedio INTEGER,
    departamento TEXT
);

-- Tabla de ciudadanos
CREATE TABLE ciudadanos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefono TEXT,
    direccion TEXT,
    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal de trámites
CREATE TABLE tramites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    fecha_inicio TEXT NOT NULL,
    tiempo_procesamiento INTEGER NOT NULL,
    estado TEXT NOT NULL CHECK(estado IN ('Recibido', 'En Proceso', 'Completado', 'Rechazado')),
    prioridad TEXT NOT NULL CHECK(prioridad IN ('Alta', 'Media', 'Normal')),
    ciudadano_email TEXT NOT NULL,
    fecha_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    FOREIGN KEY (ciudadano_email) REFERENCES ciudadanos(email)
);

-- Tabla de historial
CREATE TABLE historial_tramites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tramite_id INTEGER NOT NULL,
    estado TEXT NOT NULL,
    observaciones TEXT,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tramite_id) REFERENCES tramites(id)
);

-- Insertar datos iniciales
INSERT INTO tipos_tramite (nombre, descripcion, tiempo_promedio, departamento) VALUES
('Licencia de Construcción', 'Permiso para construcción o remodelación', 15, 'Obras Públicas'),
('Permiso de Comercio', 'Autorización para apertura de negocio', 10, 'Comercio'),
('Certificado de Residencia', 'Documento que acredita residencia', 3, 'Administración'),
('Registro Civil', 'Trámites de nacimiento, matrimonio, etc.', 7, 'Registro Civil'),
('Pago de Impuestos', 'Liquidación y pago de tributos', 1, 'Tesorería');

INSERT INTO ciudadanos (nombre, email, telefono, direccion) VALUES
('Juan Pérez', 'juan@example.com', '5551234567', 'Calle Principal 123'),
('María González', 'maria@example.com', '5557654321', 'Avenida Central 456');

INSERT INTO tramites (tipo, fecha_inicio, tiempo_procesamiento, estado, prioridad, ciudadano_email) VALUES
('Licencia de Construcción', '2023-01-15', 15, 'Completado', 'Alta', 'juan@example.com'),
('Permiso de Comercio', '2023-02-20', 10, 'En Proceso', 'Media', 'maria@example.com'),
('Certificado de Residencia', '2023-03-10', 3, 'Recibido', 'Normal', 'juan@example.com');

INSERT INTO historial_tramites (tramite_id, estado, observaciones) VALUES
(1, 'Recibido', 'Trámite ingresado al sistema'),
(1, 'En Proceso', 'En revisión por el departamento de Obras Públicas'),
(1, 'Completado', 'Trámite aprobado y notificado'),
(2, 'Recibido', 'Trámite ingresado al sistema'),
(2, 'En Proceso', 'En revisión por el departamento de Comercio'),
(3, 'Recibido', 'Trámite ingresado al sistema');

-- Crear índices
CREATE INDEX idx_tramites_prioridad ON tramites(prioridad);
CREATE INDEX idx_tramites_estado ON tramites(estado);
CREATE INDEX idx_tramites_email ON tramites(ciudadano_email);
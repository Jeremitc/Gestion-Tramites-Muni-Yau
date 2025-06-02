CREATE TABLE tramites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    fecha_inicio TEXT NOT NULL,
    tiempo_procesamiento INTEGER,
    estado TEXT NOT NULL,
    prioridad TEXT,
    ciudadano_email TEXT
);
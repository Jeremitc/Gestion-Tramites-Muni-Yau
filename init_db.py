import sqlite3

def init_db():
    conn = sqlite3.connect('tramites.db')
    cursor = conn.cursor()
    
    # Tabla principal de trámites
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tramites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            fecha_inicio TEXT NOT NULL,
            tiempo_procesamiento INTEGER NOT NULL,
            estado TEXT NOT NULL CHECK(estado IN ('Recibido', 'En Proceso', 'Completado', 'Rechazado')),
            prioridad TEXT NOT NULL CHECK(prioridad IN ('Alta', 'Media', 'Normal')),
            ciudadano_email TEXT NOT NULL,
            fecha_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP,
            observaciones TEXT
        )
    ''')
    
    # Tabla de tipos de trámites
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tipos_tramite (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            tiempo_promedio INTEGER,
            departamento TEXT
        )
    ''')
    
    # Tabla de ciudadanos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ciudadanos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefono TEXT,
            direccion TEXT,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de historial
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_tramites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tramite_id INTEGER NOT NULL,
            estado TEXT NOT NULL,
            observaciones TEXT,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tramite_id) REFERENCES tramites(id)
        )
    ''')
    
    # Datos iniciales
    try:
        cursor.executemany('''
            INSERT INTO tipos_tramite (nombre, descripcion, tiempo_promedio, departamento) 
            VALUES (?, ?, ?, ?)
        ''', [
            ('Licencia de Construcción', 'Permiso para construcción o remodelación', 15, 'Obras Públicas'),
            ('Permiso de Comercio', 'Autorización para apertura de negocio', 10, 'Comercio'),
            ('Certificado de Residencia', 'Documento que acredita residencia', 3, 'Administración'),
            ('Registro Civil', 'Trámites de nacimiento, matrimonio, etc.', 7, 'Registro Civil'),
            ('Pago de Impuestos', 'Liquidación y pago de tributos', 1, 'Tesorería')
        ])
        
        # Insertar algunos datos de ejemplo
        cursor.execute('''
            INSERT INTO ciudadanos (nombre, email, telefono, direccion)
            VALUES (?, ?, ?, ?)
        ''', ('Juan Pérez', 'juan@example.com', '5551234567', 'Calle Principal 123'))
        
        cursor.execute('''
            INSERT INTO tramites (tipo, fecha_inicio, tiempo_procesamiento, estado, prioridad, ciudadano_email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Licencia de Construcción', '2023-01-15', 15, 'Completado', 'Alta', 'juan@example.com'))
        
        cursor.execute('''
            INSERT INTO historial_tramites (tramite_id, estado, observaciones)
            VALUES (?, ?, ?)
        ''', (1, 'Recibido', 'Trámite ingresado al sistema'))
        
        cursor.execute('''
            INSERT INTO historial_tramites (tramite_id, estado, observaciones)
            VALUES (?, ?, ?)
        ''', (1, 'En Proceso', 'En revisión por el departamento de Obras Públicas'))
        
        cursor.execute('''
            INSERT INTO historial_tramites (tramite_id, estado, observaciones)
            VALUES (?, ?, ?)
        ''', (1, 'Completado', 'Trámite aprobado y notificado'))
        
    except sqlite3.IntegrityError:
        pass  # Los datos ya existen
    
    # Índices
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tramites_prioridad ON tramites(prioridad)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tramites_estado ON tramites(estado)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tramites_email ON tramites(ciudadano_email)')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
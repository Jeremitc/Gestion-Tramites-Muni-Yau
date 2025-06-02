import sqlite3

conn = sqlite3.connect('tramites.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tramites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        fecha_inicio TEXT,
        tiempo_procesamiento INTEGER,
        estado TEXT,
        prioridad TEXT,
        ciudadano_email TEXT
    )
''')
conn.commit()
conn.close()
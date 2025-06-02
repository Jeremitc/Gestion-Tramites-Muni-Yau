from flask import Flask, request, render_template, redirect, url_for, flash, abort
import sqlite3
from datetime import datetime, date
from Clasi_prio import clasificar_tramite, priorizar_tramite, guardar_tramite

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

def get_db_connection():
    conn = sqlite3.connect('tramites.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_tramites_stats(conn):
    stats = {
        'total_tramites': 0,
        'completed_tramites': 0,
        'processing_tramites': 0,
        'high_priority_tramites': 0
    }
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tramites")
    stats['total_tramites'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tramites WHERE estado = 'Completado'")
    stats['completed_tramites'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tramites WHERE estado = 'En Proceso'")
    stats['processing_tramites'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tramites WHERE prioridad = 'Alta'")
    stats['high_priority_tramites'] = cursor.fetchone()[0]
    
    return stats

@app.route('/', methods=['GET', 'POST'])
def inicio():
    conn = get_db_connection()
    error = None
    today = date.today().isoformat()
    
    if request.method == 'POST':
        try:
            tipo = request.form['tipo'].strip()
            fecha = request.form['fecha']
            tiempo = request.form['tiempo']
            email = request.form['email'].strip()
            
            # Validaciones
            if not tipo or not all(c.isalpha() or c.isspace() for c in tipo):
                raise ValueError("El tipo de trámite debe contener solo letras y espacios.")
            
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            if fecha_obj < date.today():
                raise ValueError("La fecha no puede ser anterior a hoy.")
            
            if not tiempo.isdigit() or int(tiempo) < 1 or int(tiempo) > 30:
                raise ValueError("El tiempo estimado debe ser un número entre 1 y 30 días.")
            
            if not email or '@' not in email or '.' not in email:
                raise ValueError("Por favor ingrese un email válido.")
            
            # Procesar trámite
            tipo_clasificado = clasificar_tramite(int(tiempo))
            estado = 'Recibido'
            prioridad = priorizar_tramite(int(tiempo))
            
            guardar_tramite(tipo_clasificado, fecha, int(tiempo), estado, prioridad, email, conn)
            conn.commit()
            
            flash('Trámite registrado con éxito!', 'success')
            return redirect(url_for('exito'))
            
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Error inesperado al registrar el trámite: {str(e)}"
    
    # Obtener trámites existentes
    tramites = conn.execute("""
        SELECT id, tipo, fecha_inicio, tiempo_procesamiento, estado, prioridad, ciudadano_email 
        FROM tramites 
        ORDER BY CASE prioridad WHEN 'Alta' THEN 1 ELSE 2 END, fecha_inicio
    """).fetchall()
    
    stats = get_tramites_stats(conn)
    conn.close()
    
    return render_template('inicio.html', 
                         tramites=tramites, 
                         error=error, 
                         today=today,
                         total_tramites=stats['total_tramites'],
                         completed_tramites=stats['completed_tramites'],
                         processing_tramites=stats['processing_tramites'],
                         high_priority_tramites=stats['high_priority_tramites'])

@app.route('/exito')
def exito():
    return render_template('exito.html')

@app.route('/tramite/<int:id>')
def detalle_tramite(id):
    conn = get_db_connection()
    tramite = conn.execute('SELECT * FROM tramites WHERE id = ?', (id,)).fetchone()
    
    if not tramite:
        conn.close()
        abort(404)
    
    ciudadano = conn.execute(
        'SELECT * FROM ciudadanos WHERE email = ?', (tramite['ciudadano_email'],)
    ).fetchone()
    
    historial = conn.execute(
        'SELECT * FROM historial_tramites WHERE tramite_id = ? ORDER BY fecha DESC', (id,)
    ).fetchall()
    
    conn.close()
    return render_template('detalle.html', 
                         tramite=tramite,
                         ciudadano=ciudadano,
                         historial=historial)

@app.route('/buscar', methods=['GET'])
def buscar_tramites():
    conn = get_db_connection()
    tramite_id = request.args.get('id')
    tipo = request.args.get('tipo')
    estado = request.args.get('estado')
    
    query = 'SELECT id, tipo, fecha_inicio, estado FROM tramites WHERE 1=1'
    params = []
    
    if tramite_id:
        query += ' AND id = ?'
        params.append(tramite_id)
    if tipo:
        query += ' AND tipo = ?'
        params.append(tipo)
    if estado:
        query += ' AND estado = ?'
        params.append(estado)
    
    query += ' ORDER BY fecha_inicio DESC'
    resultados = conn.execute(query, params).fetchall()
    tipos_tramite = conn.execute('SELECT nombre FROM tipos_tramite').fetchall()
    conn.close()
    
    return render_template('buscar.html',
                         resultados=resultados,
                         tipos_tramite=tipos_tramite)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime
from Clasi_prio import clasificar_tramite, priorizar_tramite, guardar_tramite

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tramites.db')
    return conn

@app.route('/', methods=['GET', 'POST'])
def inicio():
    conn = get_db_connection()
    cursor = conn.cursor()
    error = None
    if request.method == 'POST':
        try:
            tipo = request.form['tipo'].strip()
            fecha = request.form['fecha']
            tiempo = request.form['tiempo']
            email = request.form['email'].strip()
            
            # Validaciones
            if not tipo or not all(c.isalpha() or c.isspace() for c in tipo):
                raise ValueError("El tipo debe contener solo letras y espacios.")
            if not fecha:
                raise ValueError("La fecha es obligatoria.")
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
            if fecha_obj < datetime.today():
                raise ValueError("La fecha no puede ser anterior a hoy.")
            if not tiempo.isdigit() or int(tiempo) < 1 or int(tiempo) > 30:
                raise ValueError("El tiempo estimado debe ser un número entre 1 y 30 días.")
            if not email or '@' not in email or '.' not in email:
                raise__()
            # Clasificar y priorizar el trámite
            tipo_clasificado = clasificar_tramite(int(tiempo))
            estado = 'Recibido'
            guardar_tramite(tipo_clasificado, fecha, int(tiempo), estado, email, conn)
            conn.commit()
            conn.close()
            return redirect(url_for('exito'))
        except ValueError as e:
            conn.rollback()
            error = str(e)
        except Exception as e:
            conn.rollback()
            error = f"Error al registrar el trámite: {str(e)}"
    # Mostrar trámites existentes
    cursor.execute("SELECT id, tipo, fecha_inicio, tiempo_procesamiento, estado, prioridad, ciudadano_email FROM tramites")
    tramites = cursor.fetchall()
    conn.close()
    return render_template('inicio.html', tramites=tramites, error=error)

@app.route('/exito')
def exito():
    return render_template('exito.html')

if __name__ == '__main__':
    app.run(debug=True)
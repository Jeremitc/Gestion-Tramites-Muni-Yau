# Gestión de Trámites - Municipalidad de Yau

## Descripción del Proyecto
Este proyecto es una aplicación web desarrollada para la **Municipalidad de Yau** que permite gestionar trámites de manera eficiente. Los usuarios (ciudadanos o empleados) pueden registrar trámites, clasificarlos automáticamente, priorizarlos y visualizarlos en una interfaz moderna y responsive. Utiliza Flask para el backend, SQLite para la base de datos, y un modelo de machine learning para clasificar trámites, todo envuelto en una interfaz atractiva con Tailwind CSS, animaciones, gradientes y sombras.

### Propósito
El sistema aborda problemas comunes en la gestión municipal de trámites, como:
- **Desorganización**: Reemplaza procesos manuales (papel o hojas de cálculo) con un registro centralizado en una base de datos.
- **Inconsistencia**: Clasifica automáticamente el tipo de trámite usando machine learning.
- **Falta de priorización**: Asigna prioridades ("Alta" o "Normal") según el tiempo estimado.
- **Dificultad de seguimiento**: Muestra trámites registrados y confirma el registro con una página de éxito.
- **Usabilidad pobre**: Ofrece una interfaz responsive, visualmente atractiva con animaciones, gradientes y sombras.

## Características
- **Registro de Trámites**: Formulario para ingresar tipo, fecha, tiempo estimado (días) y email.
- **Clasificación Automática**: Un modelo de regresión logística predice el tipo de trámite basado en el tiempo de procesamiento.
- **Priorización**: Asigna "Alta" (tiempo > 5 días) o "Normal" (≤ 5 días) automáticamente.
- **Visualización**: Tabla responsive que muestra ID, tipo, fecha, tiempo, estado, prioridad y email.
- **Confirmación**: Página de éxito con animaciones y redirección automática tras 5 segundos.
- **Diseño**: Interfaz moderna con Tailwind CSS, gradientes, sombras, animaciones (fade-in, pulse, lift on hover) y responsividad para móviles, tabletas y escritorios.
- **Validación**: Controles en el frontend (HTML) y backend para evitar datos incorrectos (ej. fecha pasada, tiempo inválido, email malformado).

## Tecnologías Utilizadas
- **Backend**:
  - Python 3.x
  - Flask: Framework web para manejar rutas y renderizar templates.
  - SQLite: Base de datos ligera para almacenar trámites.
- **Machine Learning**:
  - Pandas: Manejo de datos históricos.
  - Scikit-learn: Modelos de regresión logística y preprocesamiento (LabelEncoder, train_test_split).
- **Frontend**:
  - HTML: Estructura de las páginas (`inicio.html`, `exito.html`).
  - Tailwind CSS (v2.2.19): Estilos responsive, gradientes, sombras y diseño moderno.
  - CSS Personalizado: Animaciones (fadeIn, pulse) y efectos de elevación al pasar el mouse.
  - JavaScript: Conteo regresivo para redirección en la página de éxito.
- **Datos**:
  - CSV: Archivo `tramites_historicos.csv` para entrenar el modelo de clasificación.

## Estructura del Proyecto
```
gestion-tramites-municipalidad-yau/
│
├── app.py                  # Aplicación Flask principal: rutas, lógica y validaciones
├── Clasi_prio.py           # Lógica de clasificación y priorización de trámites
├── tramites.db             # Base de datos SQLite para almacenar trámites
├── tramites_historicos.csv # Datos históricos para entrenar el modelo
├── templates/              # Carpeta para templates HTML
│   ├── inicio.html         # Página principal con formulario y tabla de trámites
│   └── exito.html          # Página de confirmación tras registro exitoso
└── README.md               # Documentación del proyecto (este archivo)
```

## Requisitos
- **Python 3.x** (recomendado: 3.8 o superior)
- **Librerías Python**:
  - Flask: `pip install flask`
  - Pandas: `pip install pandas`
  - Scikit-learn: `pip install scikit-learn`
- **Navegador web**: Chrome, Firefox, Edge, etc. (para visualizar la interfaz)
- **Conexión a internet**: Para cargar Tailwind CSS desde CDN (https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css)

## Instalación
1. **Clonar o descargar el proyecto**:
   - Descarga los archivos o clona el repositorio a tu máquina local.
2. **Crear un entorno virtual**:
   ```bash
   python -m venv env
   ```
   - Activar en Windows: `env\Scripts\activate`
   - Activar en macOS/Linux: `source env/bin/activate`
3. **Instalar dependencias**:
   ```bash
   pip install flask pandas scikit-learn
   ```
4. **Inicializar la base de datos**:
   - Crea la tabla `tramites` ejecutando este script (guarda como `init_db.py` y corre con `python init_db.py`):
     ```python
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
     ```
5. **Asegurar datos históricos**:
   - Verifica que `tramites_historicos.csv` esté en el directorio raíz con este formato:
     ```
     tipo,tiempo_procesamiento
     licencia,3
     permiso,7
     servicio,2
     licencia,4
     permiso,8
     servicio,1
     licencia,6
     ```

## Uso
1. **Iniciar la aplicación**:
   - Desde la terminal, en el directorio del proyecto, ejecuta:
     ```bash
     python app.py
     ```
   - Esto inicia un servidor local en `http://127.0.0.1:5000` (modo debug activado).
2. **Acceder a la interfaz**:
   - Abre un navegador y visita `http://127.0.0.1:5000`.
3. **Registrar un trámite**:
   - Completa el formulario en `inicio.html`:
     - **Tipo**: Solo letras y espacios (ej. "Poder").
     - **Fecha**: Selecciona una fecha no anterior a hoy (valor por defecto: 2025-06-01).
     - **Tiempo estimado**: Número entre 1 y 30 días.
     - **Email**: Dirección válida (ej. "jeremy.genial1@gmail.com").
   - Haz clic en "Enviar".
4. **Resultado**:
   - Si hay errores, verás un mensaje en rojo en la página principal.
   - Si es exitoso, serás redirigido a `exito.html`, que muestra una confirmación animada y te devuelve a la página principal en 5 segundos.
5. **Visualizar trámites**:
   - La tabla en `inicio.html` muestra todos los trámites registrados con ID, tipo, fecha, tiempo, estado, prioridad y email.

## Detalles de los Archivos

### 1. `app.py`
- **Función**: Servidor Flask que maneja rutas y lógica.
- **Rutas**:
  - `/` (GET, POST): Muestra el formulario y la tabla; procesa el registro de trámites.
  - `/exito` (GET): Muestra la página de confirmación.
- **Validaciones**:
  - Tipo: Solo letras y espacios.
  - Fecha: No anterior a hoy.
  - Tiempo: Entre 1 y 30 días.
  - Email: Debe incluir "@" y ".".
- **Redirección**: Tras un registro exitoso, va a la página de éxito.

### 2. `Clasi_prio.py`
- **Función**: Clasifica y prioriza trámites.
- **Componentes**:
  - Carga `tramites_historicos.csv` y entrena un modelo de regresión logística.
  - `clasificar_tramite(tiempo)`: Predice el tipo (ej. "licencia", "permiso") según el tiempo.
  - `priorizar_tramite(tiempo)`: Asigna "Alta" (> 5 días) o "Normal" (≤ 5 días).
  - `guardar_tramite(...)`: Inserta el trámite en la base de datos.

### 3. `inicio.html`
- **Función**: Página principal con formulario y tabla.
- **Diseño**:
  - Gradientes (fondo, botones, tabla), sombras profundas, animaciones (fade-in, pulse, elevación al pasar el mouse).
  - Responsive: Ajustes para móviles (p-4), tabletas (sm:p-6) y escritorios (md:p-8).
  - Muestra errores en rojo si la validación falla.

### 4. `exito.html`
- **Función**: Confirma el registro exitoso.
- **Diseño**:
  - Fondo con gradiente verde-azul, sombras marcadas, animación de escala al interactuar.
  - Conteo regresivo (5 segundos) con JavaScript para redirigir a `inicio.html`.
  - Botón manual para volver antes.

### 5. `tramites_historicos.csv`
- **Función**: Datos históricos para entrenar el modelo.
- **Formato**: Columnas `tipo` (texto) y `tiempo_procesamiento` (número).

## Limitaciones
- **Modelo simple**: La clasificación se basa solo en el tiempo de procesamiento; podría incluir más variables (ej. descripción).
- **Seguridad**: No hay autenticación ni protección contra accesos no autorizados.
- **Estados**: Solo usa "Recibido"; no permite actualizar a "En Proceso" o "Completado".
- **Producción**: El servidor Flask en modo debug no es apto para uso real; usa un servidor WSGI (ej. Gunicorn) para producción.

## Posibles Mejoras
- Agregar un sistema de login para restringir el acceso.
- Permitir actualizar el estado de los trámites desde la interfaz.
- Enviar notificaciones por email al registrar un trámite.
- Mejorar el modelo de machine learning con más datos y características.
- Añadir filtros o búsqueda en la tabla de trámites.

## Notas
- **Fecha actual**: El sistema asume una fecha base (2025-06-01) para validaciones y valores por defecto.
- **Advertencia**: El servidor Flask en modo debug muestra mensajes como "WARNING: This is a development server...". Para producción, configura un servidor WSGI.

## Autor
Desarrollado para la Municipalidad de Yau, con el soporte de herramientas de IA para la generación de código y documentación.

## Licencia
Este proyecto es de uso libre para fines educativos y de prueba. Para uso comercial, consulta con los desarrolladores o la Municipalidad de Yau.
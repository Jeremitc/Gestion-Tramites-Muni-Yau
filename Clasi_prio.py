import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Cargar datos
data = pd.read_csv('tramites_historicos.csv')
data = data.dropna()  # Limpiar datos faltantes

# Codificar etiquetas (e.g., tipo: licencia, permiso)
le_tipo = LabelEncoder()
data['tipo_cod'] = le_tipo.fit_transform(data['tipo'])

# Entrenar modelo de clasificación
X = data[['tiempo_procesamiento']]  # Características simples
y = data['tipo_cod']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
modelo_clasificacion = LogisticRegression()
modelo_clasificacion.fit(X_train, y_train)

# Predecir tipo de trámite
def clasificar_tramite(tiempo):
    pred = modelo_clasificacion.predict(pd.DataFrame({'tiempo_procesamiento': [tiempo]}))
    return le_tipo.inverse_transform(pred)[0]

# Priorizar (regla simple: tiempo largo = alta prioridad)
def priorizar_tramite(tiempo):
    return 'Alta' if tiempo > 5 else 'Normal'  # Ejemplo: >5 días es urgente

# Guardar trámite en la base de datos
def guardar_tramite(tipo, fecha, tiempo, estado, email, conn):
    prioridad = priorizar_tramite(tiempo)
    conn.execute("INSERT INTO tramites (tipo, fecha_inicio, tiempo_procesamiento, estado, prioridad, ciudadano_email) VALUES (?, ?, ?, ?, ?, ?)",
                 (tipo, fecha, tiempo, estado, prioridad, email))
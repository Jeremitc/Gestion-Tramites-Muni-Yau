import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Cargar y preparar datos
def load_and_prepare_data():
    try:
        data = pd.read_csv('tramites_historicos.csv')
        data = data.dropna()
        
        # Codificar tipos de trámite
        le_tipo = LabelEncoder()
        data['tipo_cod'] = le_tipo.fit_transform(data['tipo'])
        
        return data, le_tipo
    except Exception as e:
        print(f"Error loading data: {e}")
        # Datos de ejemplo si el archivo no existe
        data = pd.DataFrame({
            'tipo': ['Licencia', 'Permiso', 'Certificado', 'Registro', 'Autorización'],
            'tiempo_procesamiento': [3, 7, 2, 5, 10]
        })
        le_tipo = LabelEncoder()
        data['tipo_cod'] = le_tipo.fit_transform(data['tipo'])
        return data, le_tipo

# Entrenar modelo
def train_model():
    data, le_tipo = load_and_prepare_data()
    
    X = data[['tiempo_procesamiento']]
    y = data['tipo_cod']
    
    # Mejor modelo (RandomForest en lugar de LogisticRegression)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluar modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")
    
    return model, le_tipo

# Cargar modelo una vez al importar
modelo_clasificacion, le_tipo = train_model()

def clasificar_tramite(tiempo):
    try:
        pred = modelo_clasificacion.predict(pd.DataFrame({'tiempo_procesamiento': [tiempo]}))
        return le_tipo.inverse_transform(pred)[0]
    except Exception as e:
        print(f"Error in classification: {e}")
        # Fallback si hay problemas con el modelo
        if tiempo <= 3:
            return "Trámite Rápido"
        elif tiempo <= 7:
            return "Trámite Regular"
        else:
            return "Trámite Complejo"

def priorizar_tramite(tiempo):
    # Reglas mejoradas de priorización
    if tiempo > 10:
        return "Alta"
    elif tiempo > 5:
        return "Media"
    else:
        return "Normal"

def guardar_tramite(tipo, fecha, tiempo, estado, prioridad, email, conn):
    try:
        conn.execute("""
            INSERT INTO tramites (tipo, fecha_inicio, tiempo_procesamiento, estado, prioridad, ciudadano_email) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tipo, fecha, tiempo, estado, prioridad, email))
    except Exception as e:
        print(f"Error saving tramite: {e}")
        raise
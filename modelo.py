from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import random

def preprocesar(texto):
    return texto.lower()

# Frases base según gravedad
frases = {
    "bajo": [
        "Error menor en la interfaz",
        "Retraso pequeño en la respuesta",
        "Problema con la visualización",
        "Incidencia leve en el sistema",
        "Fallo temporal sin impacto",
        "Aviso de actualización pendiente",
        "Notificación sin importancia",
        "Pequeña falla en el módulo X"
    ],
    "medio": [
        "Sistema lento pero funcional",
        "Error que afecta a algunos usuarios",
        "Interrupción temporal de servicio",
        "Problema con carga de datos",
        "Fallos intermitentes en la red",
        "Error en módulo importante",
        "Problema con acceso a funciones",
        "Retraso significativo en procesos"
    ],
    "grave": [
        "Falla grave que afecta a múltiples usuarios",
        "Error crítico en el procesamiento",
        "Pérdida de datos parcial",
        "Caída del servicio principal",
        "Incidencia que bloquea tareas",
        "Mal funcionamiento prolongado",
        "Error en sistema de seguridad",
        "Fallo que impide operaciones"
    ],
    "muy grave": [
        "Pérdida total de datos",
        "Caída completa del sistema",
        "Brecha grave de seguridad",
        "Interrupción total del servicio",
        "Incidencia que pone en riesgo el negocio",
        "Error irreversible en base de datos",
        "Fallo crítico que paraliza la empresa",
        "Ataque cibernético con consecuencias graves"
    ]
}

# Función para generar textos aleatorios
def generar_textos(num):
    textos = []
    etiquetas = []
    categorias = list(frases.keys())
    for _ in range(num):
        cat = random.choice(categorias)
        texto = random.choice(frases[cat])
        sufijos = ["", " ayer", " esta mañana", " desde ayer", " hoy", " hace una hora"]
        texto += random.choice(sufijos)
        textos.append(preprocesar(texto))
        etiquetas.append(cat)
    return textos, etiquetas

# Generar 1000 ejemplos sintéticos
textos, etiquetas = generar_textos(1000)

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    textos, etiquetas, test_size=0.2, random_state=42, stratify=etiquetas
)

# Vectorizar textos
vectorizer = TfidfVectorizer()
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Entrenar modelo
model = MultinomialNB()
model.fit(X_train_vect, y_train)

# Predecir y evaluar
y_pred = model.predict(X_test_vect)
print(classification_report(y_test, y_pred, zero_division=0))

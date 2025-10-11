from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import random

# Función de preprocesamiento
def preprocesar(texto):
    return texto.lower().strip()

# Frases originales por categoría con mejora de casos graves
frases = {
    "bajo": [
        "Error menor en la interfaz",
        "Retraso pequeño en la respuesta",
        "Problema con la visualización",
        "Incidencia leve en el sistema",
        "Fallo temporal sin impacto",
        "Aviso de actualización pendiente",
        "Notificación sin importancia",
        "Pequeña falla en el módulo X",
        "Mensaje de error confuso",
        "Problema con iconos gráficos",
        "Inconveniente menor en la configuración",
        "Pequeño desajuste en el diseño",
        "Retraso en notificaciones no críticas",
        "Problema con formatos de fecha",
        "Error en traducción o localización",
        "Discrepancia menor en reportes",
        "Notificación duplicada sin impacto",
        "Problema menor con el navegador",
        "Fallo en tooltip o ayuda contextual",
        "Error menor en validación de formulario",
        "Dificultad leve para encontrar opciones",
        "Error en etiquetas o textos informativos",
        "Problema menor en el sistema de ayuda",
        "Pequeña inconsistencia en colores o temas",
        "Advertencia por versión obsoleta",
        "Error en vista previa de documentos",
        "Incidencia menor en sistema de búsqueda",
        "Problema con zoom o escalado en pantalla",
        "Error de redirección no crítica",
        "Problema menor con botones o enlaces",
    ],
    "medio": [
        "Sistema lento pero funcional",
        "Error que afecta a algunos usuarios",
        "Interrupción temporal de servicio",
        "Problema con carga de datos",
        "Fallos intermitentes en la red",
        "Error en módulo importante",
        "Problema con acceso a funciones",
        "Retraso significativo en procesos",
        "Incidencia en sincronización de datos",
        "Error en generación de reportes",
        "Falla en actualización de información",
        "Problemas con notificaciones push",
        "Error intermitente en autenticación",
        "Desconexiones frecuentes",
        "Inconsistencias en bases de datos locales",
        "Problemas con integración de API",
        "Errores en exportación de archivos",
        "Limitación temporal en funcionalidades",
        "Problema con permisos de usuario",
        "Falla en sistema de backup parcial",
        "Interrupción en flujo de trabajo",
        "Error en configuración de usuario",
        "Problema en gestión de sesiones",
        "Error en manejo de archivos adjuntos",
        "Fallo en actualización automática",
        "Problemas con notificaciones por email",
        "Error en conexión a bases de datos externas",
        "Falla en sincronización con sistemas externos",
        "Retrasos en procesamiento de pagos",
        "Error en validación de datos de entrada",
    ],
    "grave": [
        "Falla grave que afecta a múltiples usuarios",
        "Error crítico en el procesamiento",
        "Pérdida de datos parcial",
        "Caída del servicio principal",
        "Incidencia que bloquea tareas",
        "Mal funcionamiento prolongado",
        "Error en sistema de seguridad",
        "Fallo que impide operaciones",
        "Problema serio en el sistema de pagos",
        "Falla en integridad de datos",
        "Errores en autenticación masiva",
        "Interrupción en comunicación con servidores",
        "Inaccesibilidad prolongada de funciones críticas",
        "Fallo en la actualización del sistema",
        "Problemas con cifrado de datos",
        "Incidencia en sistema de gestión documental",
        "Error grave en sistema de inventarios",
        "Falla en balanceo de carga",
        "Desincronización masiva de datos",
        "Problema en restauración de backups",
        "Error grave en control de versiones",
        "Fallo en sistema de notificaciones críticas",
        "Problemas en procesamiento batch",
        "Inconsistencia en datos financieros",
        "Falla en monitorización del sistema",
        "Error en sistema de auditoría",
        "Fallo en acceso a recursos compartidos",
        "Problema con escalabilidad del sistema",
        "Error en gestión de licencias",
        "Falla en procesos automatizados",
    ],
    "muy grave": [
        "Pérdida total de datos",
        "Caída completa del sistema",
        "Brecha grave de seguridad",
        "Interrupción total del servicio",
        "Incidencia que pone en riesgo el negocio",
        "Error irreversible en base de datos",
        "Fallo crítico que paraliza la empresa",
        "Ataque cibernético con consecuencias graves",
        "Compromiso de datos personales sensibles",
        "Desastre en infraestructura tecnológica",
        "Interrupción masiva en red corporativa",
        "Fallo en sistema de emergencia",
        "Pérdida de acceso a sistemas clave",
        "Corrupción completa de base de datos",
        "Desplome de plataforma web",
        "Incidencia que genera pérdidas económicas severas",
        "Fallo en sistema de respaldo y recuperación",
        "Ataque de ransomware con cifrado masivo",
        "Caída prolongada sin fecha de solución",
        "Incumplimiento regulatorio grave por fallo técnico",
        "Fallo total en sistema de autenticación",
        "Pérdida de integridad en sistema contable",
        "Desconexión global de servicios críticos",
        "Error catastrófico en hardware central",
        "Fallo en redundancia y alta disponibilidad",
        "Incidente que afecta la continuidad del negocio",
        "Violación masiva de datos personales",
        "Interrupción de servicios gubernamentales",
        "Destrucción de datos irrecuperable",
        "Fallo crítico en sistemas de salud",
        # Nuevos casos de emergencia añadidos
        "Incendio en el equipo",
        "Fuego en el ordenador",
        "Riesgo eléctrico grave",
        "Explosión potencial",
        "Emergencia crítica de seguridad",
    ]
}

# Datos globales para permitir aprendizaje incremental
X_textos, y_etiquetas = [], []

def generar_textos(num):
    textos, etiquetas = [], []
    categorias = list(frases.keys())
    sufijos = ["", " ayer", " hoy", " desde hace una hora", " recientemente", " durante la noche"]
    for _ in range(num):
        cat = random.choice(categorias)
        texto = random.choice(frases[cat])
        texto += random.choice(sufijos)
        textos.append(preprocesar(texto))
        etiquetas.append(cat)
    return textos, etiquetas

# Inicializar dataset
X_textos, y_etiquetas = generar_textos(1000)

# Vectorizador y modelo globales
vectorizer = TfidfVectorizer()
X_vect = vectorizer.fit_transform(X_textos)
model = MultinomialNB()
model.fit(X_vect, y_etiquetas)

# Función para predecir prioridad
def predecir_prioridad(texto):
    texto_proc = preprocesar(texto)
    vect = vectorizer.transform([texto_proc])
    return model.predict(vect)[0]

# Función para aprender una nueva incidencia y reentrenar
def aprender_incidencia(texto, prioridad):
    global X_textos, y_etiquetas, vectorizer, model
    X_textos.append(preprocesar(texto))
    y_etiquetas.append(prioridad)

    # Reentrenar vectorizador y modelo
    vectorizer = TfidfVectorizer()
    X_vect = vectorizer.fit_transform(X_textos)
    model = MultinomialNB()
    model.fit(X_vect, y_etiquetas)

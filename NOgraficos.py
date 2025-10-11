import sqlite3
import matplotlib.pyplot as plt

# Conectar a la base de datos (asegúrate de que esté en la misma carpeta)
conn = sqlite3.connect('BBDD-SQLITE.db')
cursor = conn.cursor()

# Consulta: contar incidencias por nivel de categoría
cursor.execute("""
    SELECT c.nivel, COUNT(i.id_in) as total
    FROM categorias c
    LEFT JOIN incidencias i ON c.id_cat = i.id_cat
    GROUP BY c.nivel
""")

# Obtener los datos
resultados = cursor.fetchall()

# Separar los datos
categorias = [fila[0] for fila in resultados]
cantidades = [fila[1] for fila in resultados]

# Crear gráfico de pastel
plt.figure(figsize=(8,8))
plt.pie(
    cantidades,
    labels=categorias,
    autopct='%1.1f%%',
    startangle=140,
    shadow=True
)
plt.title("Distribución de incidencias por categoría")
plt.axis('equal')
plt.show()

# Cerrar conexión
conn.close()

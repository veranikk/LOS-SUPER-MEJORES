import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class EstadisticasTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # Inicializar la interfaz gráfica

    def init_ui(self):
        layout = QVBoxLayout()  # Layout vertical para organizar los widgets

        # Crear y configurar un QLabel que actúa como título de la pestaña
        titulo = QLabel("📊 Estadísticas de Incidencias")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)  # Añadir título al layout

        # Crear una figura de matplotlib con tamaño 8x8 pulgadas
        self.figure = Figure(figsize=(8, 8))
        # Crear un canvas para poder mostrar la figura en PyQt
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)  # Añadir canvas al layout

        # Crear dos ejes (subplots) dentro de la figura:
        # ax_categorias para el gráfico circular (pie chart) arriba
        self.ax_categorias = self.figure.add_subplot(211)
        # ax_estados para el gráfico de barras abajo
        self.ax_estados = self.figure.add_subplot(212)

        self.setLayout(layout)  # Establecer el layout para este widget

        # Llamar funciones para dibujar ambos gráficos inicialmente
        self.actualizar_grafico_categorias()
        self.actualizar_grafico_estados()

    def actualizar_grafico_categorias(self):
        """Genera y muestra un gráfico circular con la distribución de incidencias por categoría."""
        # Conectar con la base de datos SQLite
        conn = sqlite3.connect("BBDD-SQLITE.db")
        cursor = conn.cursor()

        # Consulta para obtener categorías y el número total de incidencias por categoría
        cursor.execute("""
            SELECT c.nivel, COUNT(i.id_in) as total
            FROM categorias c
            LEFT JOIN incidencias i ON c.id_cat = i.id_cat
            GROUP BY c.nivel
        """)
        resultados = cursor.fetchall()
        conn.close()  # Cerrar la conexión a la base de datos

        # Separar datos: categorías y cantidades solo si hay incidencias (>0)
        categorias = [fila[0] for fila in resultados if fila[1] > 0]
        cantidades = [fila[1] for fila in resultados if fila[1] > 0]

        self.ax_categorias.clear()  # Limpiar el área de dibujo antes de graficar

        if not categorias:
            # Si no hay datos, mostrar mensaje en el gráfico
            self.ax_categorias.text(0.5, 0.5, "No hay incidencias registradas",
                                    ha="center", va="center", fontsize=12)
        else:
            # Definir colores para las secciones del gráfico circular
            colores = ["#4CAF50", "#FF9800", "#F44336", "#2196F3", "#9C27B0"]
            # Dibujar gráfico circular (pie chart)
            wedges, texts, autotexts = self.ax_categorias.pie(
                cantidades,
                labels=categorias,
                autopct=lambda p: f'{p:.1f}%' if p > 0 else '',  # Mostrar porcentaje solo si > 0
                startangle=140,      # Ángulo inicial del gráfico
                shadow=True,         # Sombra en el gráfico
                colors=colores[:len(categorias)],  # Colores según número de categorías
                textprops={'fontsize': 10},        # Tamaño de texto de etiquetas
                radius=1.2,          # Tamaño del círculo más grande
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'}  # Bordes blancos entre secciones
            )
            # Ajustar tamaño de las etiquetas y porcentajes
            for t in texts:
                t.set_fontsize(10)
            for at in autotexts:
                at.set_fontsize(9)
            # Título del gráfico circular
            self.ax_categorias.set_title("Distribución de incidencias por categoría", fontsize=12)
            self.ax_categorias.axis("equal")  # Ejes iguales para que el pie sea circular

        self.canvas.draw()  # Renderizar el canvas para mostrar el gráfico actualizado

    def actualizar_grafico_estados(self):
        """Genera y muestra un gráfico de barras con el número de incidencias por estado."""
        # Conectar con la base de datos SQLite
        conn = sqlite3.connect("BBDD-SQLITE.db")
        cursor = conn.cursor()

        # Consulta para obtener estados y número total de incidencias por estado
        cursor.execute("""
            SELECT estado_in, COUNT(id_in) as total
            FROM incidencias
            GROUP BY estado_in
        """)
        resultados = cursor.fetchall()
        conn.close()  # Cerrar la conexión

        estados = [fila[0] for fila in resultados]      # Estados (categorías)
        cantidades = [fila[1] for fila in resultados]   # Cantidades por estado

        self.ax_estados.clear()  # Limpiar gráfico previo

        if not estados:
            # Mostrar mensaje si no hay datos
            self.ax_estados.text(0.5, 0.5, "No hay incidencias registradas",
                                 ha="center", va="center", fontsize=12)
        else:
            colores = ["#4CAF50", "#FF9800", "#F44336"]  # Colores para barras
            # Dibujar gráfico de barras con estados y sus cantidades
            self.ax_estados.bar(estados, cantidades, color=colores[:len(estados)])
            self.ax_estados.set_title("Número de incidencias por estado", fontsize=12)
            self.ax_estados.set_ylabel("Cantidad")
            self.ax_estados.set_xlabel("Estado")

            # Añadir etiquetas con los valores encima de cada barra
            for idx, valor in enumerate(cantidades):
                self.ax_estados.text(idx, valor + 0.1, str(valor), ha="center", va="bottom")

        self.canvas.draw()  # Actualizar el canvas para mostrar cambios
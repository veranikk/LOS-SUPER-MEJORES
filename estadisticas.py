import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class EstadisticasTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        titulo = QLabel("📊 Estadísticas de Incidencias")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        # Crear las figuras
        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Crear otra figura para las incidencias por estado
        self.figure_estado = Figure(figsize=(8, 5))
        self.canvas_estado = FigureCanvas(self.figure_estado)
        layout.addWidget(self.canvas_estado)

        self.setLayout(layout)

        # Dibujar gráficos
        self.actualizar_grafico_categorias()
        self.actualizar_grafico_estados()

    def actualizar_grafico_categorias(self):
        """Gráfico circular de distribución de incidencias por categoría (nivel de prioridad)."""
        conn = sqlite3.connect("BBDD-SQLITE.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.nivel, COUNT(i.id_in) as total
            FROM categorias c
            LEFT JOIN incidencias i ON c.id_cat = i.id_cat
            GROUP BY c.nivel
        """)

        resultados = cursor.fetchall()
        conn.close()

        # Filtrar categorías vacías
        categorias = [fila[0] for fila in resultados if fila[1] > 0]
        cantidades = [fila[1] for fila in resultados if fila[1] > 0]

        ax = self.figure.subplots()
        ax.clear()

        if not categorias:
            ax.text(0.5, 0.5, "No hay incidencias registradas", ha="center", va="center", fontsize=12)
        else:
            colores = ["#4CAF50", "#FF9800", "#F44336", "#2196F3", "#9C27B0"]
            wedges, texts, autotexts = ax.pie(
                cantidades,
                labels=categorias,
                autopct=lambda p: f'{p:.1f}%' if p > 0 else '',
                startangle=140,
                shadow=True,
                colors=colores[:len(categorias)],
                textprops={'fontsize': 10}
            )
            for t in texts:
                t.set_fontsize(10)
            for at in autotexts:
                at.set_fontsize(9)
            ax.set_title("Distribución de incidencias por categoría", fontsize=12)
            ax.axis("equal")

        self.canvas.draw()

    def actualizar_grafico_estados(self):
        """Gráfico de barras con el número de incidencias por estado."""
        conn = sqlite3.connect("BBDD-SQLITE.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT estado_in, COUNT(id_in) as total
            FROM incidencias
            GROUP BY estado_in
        """)

        resultados = cursor.fetchall()

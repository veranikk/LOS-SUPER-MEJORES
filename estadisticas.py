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

        # Título de la pestaña
        titulo = QLabel("📊 Estadísticas de Incidencias")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        # Crear figura única para todo, y dos ejes: uno para el pie, otro para barras
        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Crear ejes independientes
        self.ax_categorias = self.figure.add_subplot(211)  # Pie chart en la parte superior
        self.ax_estados = self.figure.add_subplot(212)     # Gráfico de barras en la parte inferior

        self.setLayout(layout)

        # Dibujar gráficos
        self.actualizar_grafico_categorias()
        self.actualizar_grafico_estados()

    def actualizar_grafico_categorias(self):
        """Gráfico circular de distribución de incidencias por categoría."""
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

        categorias = [fila[0] for fila in resultados if fila[1] > 0]
        cantidades = [fila[1] for fila in resultados if fila[1] > 0]

        self.ax_categorias.clear()  # Limpiar ejes antes de dibujar

        if not categorias:
            self.ax_categorias.text(0.5, 0.5, "No hay incidencias registradas",
                                    ha="center", va="center", fontsize=12)
        else:
            colores = ["#4CAF50", "#FF9800", "#F44336", "#2196F3", "#9C27B0"]
            wedges, texts, autotexts = self.ax_categorias.pie(
                cantidades,
                labels=categorias,
                autopct=lambda p: f'{p:.1f}%' if p > 0 else '',
                startangle=140,
                shadow=True,
                colors=colores[:len(categorias)],
                textprops={'fontsize': 10},
                radius=1.2,  # Círculo más grande
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'}  # borde blanco entre secciones
            )
            for t in texts:
                t.set_fontsize(10)
            for at in autotexts:
                at.set_fontsize(9)
            self.ax_categorias.set_title("Distribución de incidencias por categoría", fontsize=12)
            self.ax_categorias.axis("equal")

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
        conn.close()

        estados = [fila[0] for fila in resultados]
        cantidades = [fila[1] for fila in resultados]

        self.ax_estados.clear()
        if not estados:
            self.ax_estados.text(0.5, 0.5, "No hay incidencias registradas",
                                 ha="center", va="center", fontsize=12)
        else:
            colores = ["#4CAF50", "#FF9800", "#F44336"]
            self.ax_estados.bar(estados, cantidades, color=colores[:len(estados)])
            self.ax_estados.set_title("Número de incidencias por estado", fontsize=12)
            self.ax_estados.set_ylabel("Cantidad")
            self.ax_estados.set_xlabel("Estado")
            for idx, valor in enumerate(cantidades):
                self.ax_estados.text(idx, valor + 0.1, str(valor), ha="center", va="bottom")

        self.canvas.draw()

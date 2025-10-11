from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from registro import RegistroIncidenciaTab
from visualizacion import VisualizacionIncidenciaTab
from estadisticas import EstadisticasTab  # ✅ Nueva pestaña


class MainWindow(QWidget):
    def __init__(self, id_us=1):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Incidencias")
        self.setGeometry(150, 150, 800, 500)
        self.id_us = id_us  # Usuario logueado
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Crear pestañas
        self.visualizacion_tab = VisualizacionIncidenciaTab()
        self.estadisticas_tab = EstadisticasTab()
        self.registro_tab = RegistroIncidenciaTab(self.actualizar_visualizacion, id_us=self.id_us)

        # Añadir pestañas al QTabWidget
        self.tabs.addTab(self.registro_tab, "Registrar Incidencia")
        self.tabs.addTab(self.visualizacion_tab, "Visualizar Incidencias")
        self.tabs.addTab(self.estadisticas_tab, "Estadísticas")

        # Layout principal
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def actualizar_visualizacion(self):
        """Refresca la tabla y los gráficos de estadísticas."""
        try:
            # Refresca la vista de incidencias
            self.visualizacion_tab.aplicar_filtros()

            # Actualiza los gráficos de estadísticas si existen
            if hasattr(self.estadisticas_tab, "actualizar_grafico_categorias"):
                self.estadisticas_tab.actualizar_grafico_categorias()
            if hasattr(self.estadisticas_tab, "actualizar_grafico_estados"):
                self.estadisticas_tab.actualizar_grafico_estados()

            # Cambia a la pestaña de visualización
            self.tabs.setCurrentWidget(self.visualizacion_tab)

        except Exception as e:
            print(f"Error al actualizar la visualización: {e}")

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from registro import RegistroIncidenciaTab
from visualizacion import VisualizacionIncidenciaTab
from estadisticas import EstadisticasTab 

class MainWindow(QWidget):
    def __init__(self, id_us=1):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Incidencias")
        self.setGeometry(150, 150, 800, 500)
        self.id_us = id_us 
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # 🔹 Pasamos la función actualizar_grafico como callback
        self.visualizacion_tab = VisualizacionIncidenciaTab(actualizar_graficas_callback=self.actualizar_visualizacion)
        self.estadisticas_tab = EstadisticasTab()
        self.registro_tab = RegistroIncidenciaTab(self.actualizar_visualizacion, id_us=self.id_us)

        self.tabs.addTab(self.registro_tab, "Registrar Incidencia")
        self.tabs.addTab(self.visualizacion_tab, "Visualizar Incidencias")
        self.tabs.addTab(self.estadisticas_tab, "Estadísticas")
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def actualizar_visualizacion(self):
        """Refresca la tabla y los gráficos de estadísticas."""
        try:
            self.visualizacion_tab.aplicar_filtros()
            if hasattr(self.estadisticas_tab, "actualizar_grafico_categorias"):
                self.estadisticas_tab.actualizar_grafico_categorias()
            if hasattr(self.estadisticas_tab, "actualizar_grafico_estados"):
                self.estadisticas_tab.actualizar_grafico_estados()
            self.tabs.setCurrentWidget(self.visualizacion_tab)
        except Exception as e:
            print(f"Error al actualizar la visualización: {e}")

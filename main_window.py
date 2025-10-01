from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from registro import RegistroIncidenciaTab
from visualizacion import VisualizacionIncidenciaTab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Incidencias")
        self.setGeometry(150, 150, 600, 400)
        self.incidencias = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.visualizacion_tab = VisualizacionIncidenciaTab(self.incidencias)
        self.registro_tab = RegistroIncidenciaTab(self.incidencias, self.actualizar_visualizacion)

        self.tabs.addTab(self.registro_tab, "Registrar Incidencia")
        self.tabs.addTab(self.visualizacion_tab, "Visualizar Incidencias")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def actualizar_visualizacion(self):
        self.visualizacion_tab.aplicar_filtros()
        self.tabs.setCurrentWidget(self.visualizacion_tab)

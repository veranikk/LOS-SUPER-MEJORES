from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from registro import RegistroIncidenciaTab
from visualizacion import VisualizacionIncidenciaTab

class MainWindow(QWidget):
    def __init__(self, id_us=1):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Incidencias")
        self.setGeometry(150, 150, 600, 400)
        self.id_us = id_us  # Usuario logueado
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.visualizacion_tab = VisualizacionIncidenciaTab()
        self.registro_tab = RegistroIncidenciaTab(self.actualizar_visualizacion, id_us=self.id_us)

        self.tabs.addTab(self.registro_tab, "Registrar Incidencia")
        self.tabs.addTab(self.visualizacion_tab, "Visualizar Incidencias")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def actualizar_visualizacion(self):
        self.visualizacion_tab.aplicar_filtros()
        self.tabs.setCurrentWidget(self.visualizacion_tab)

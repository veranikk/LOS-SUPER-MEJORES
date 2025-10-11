from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from registro import RegistroIncidenciaTab
from visualizacion import VisualizacionIncidenciaTab
from estadisticas import EstadisticasTab 

class MainWindow(QWidget):
    #Este es el constructor de la ventana principal, mostrando el nombre de la pestaña y también según el usuario logeado ()
    def __init__(self, id_us=1):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Incidencias")
        self.setGeometry(150, 150, 800, 500)
        self.id_us = id_us 
        self.init_ui()

    #Este se encarga de la interfaz de la ventana, así mostrando diferentes pestañas en la parte superior de la ventana
    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Crea las pestañas, llamando a los diferentes constructores de las diferentes clases
        self.visualizacion_tab = VisualizacionIncidenciaTab()
        self.estadisticas_tab = EstadisticasTab()
        self.registro_tab = RegistroIncidenciaTab(self.actualizar_visualizacion, id_us=self.id_us)

        # Se agregan las pestañas creaddas
        self.tabs.addTab(self.registro_tab, "Registrar Incidencia")
        self.tabs.addTab(self.visualizacion_tab, "Visualizar Incidencias")
        self.tabs.addTab(self.estadisticas_tab, "Estadísticas")
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    # Este sirve para actualizar las incidencias de la tabla, y la gráfica, todo estro en un try, asi en caso de encontrar un error a la hora de actualizar, se muestre un error junto con el error
    def actualizar_visualizacion(self):
        """Refresca la tabla y los gráficos de estadísticas."""
        try:
            # Refresca la vista de incidencias, asi en caso de haber generado uno nuevo también se muestre al momento en la vista de las incidencias
            self.visualizacion_tab.aplicar_filtros()

            # Actualiza las gráficas
            if hasattr(self.estadisticas_tab, "actualizar_grafico_categorias"):
                self.estadisticas_tab.actualizar_grafico_categorias()
            if hasattr(self.estadisticas_tab, "actualizar_grafico_estados"):
                self.estadisticas_tab.actualizar_grafico_estados()

            # Cambia a la pestaña de visualización
            self.tabs.setCurrentWidget(self.visualizacion_tab)

        except Exception as e:
            print(f"Error al actualizar la visualización: {e}")

# Importa los componentes necesarios de PyQt5
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

# Importa las pestañas personalizadas desde otros módulos del proyecto
from registro import RegistroIncidenciaTab
from visualizacion import VisualizacionIncidenciaTab
from estadisticas import EstadisticasTab 


# Clase principal de la aplicación: Ventana principal del sistema de gestión
class MainWindow(QWidget):
    def __init__(self, id_us=1):
        super().__init__()

        # Título y tamaño inicial de la ventana principal
        self.setWindowTitle("Sistema de Gestión de Incidencias")
        self.setGeometry(150, 150, 800, 500)

        # ID del usuario actual (por defecto = 1)
        self.id_us = id_us 

        # Inicializa la interfaz gráfica de la ventana principal
        self.init_ui()


    # Método que crea la estructura visual principal
    def init_ui(self):
        # Crea un layout vertical que contendrá todas las pestañas
        layout = QVBoxLayout()

        # Crea el contenedor de pestañas (QTabWidget)
        self.tabs = QTabWidget()

        # Se crean las tres pestañas principales de la aplicación:
        # 1. Visualización de incidencias
        # 2. Estadísticas
        # 3. Registro de nuevas incidencias

        # La pestaña de visualización recibe un callback para actualizar gráficos
        self.visualizacion_tab = VisualizacionIncidenciaTab(
            actualizar_graficas_callback=self.actualizar_visualizacion
        )

        # La pestaña de estadísticas muestra gráficos de categorías y estados
        self.estadisticas_tab = EstadisticasTab()

        # La pestaña de registro recibe el callback para actualizar las visualizaciones
        # cada vez que se registra una nueva incidencia
        self.registro_tab = RegistroIncidenciaTab(
            self.actualizar_visualizacion, 
            id_us=self.id_us
        )

        # Agrega las pestañas al contenedor (QTabWidget)
        self.tabs.addTab(self.registro_tab, "Registrar Incidencia")
        self.tabs.addTab(self.visualizacion_tab, "Visualizar Incidencias")
        self.tabs.addTab(self.estadisticas_tab, "Estadísticas")

        # Agrega el contenedor de pestañas al layout principal
        layout.addWidget(self.tabs)

        # Establece el layout final de la ventana principal
        self.setLayout(layout)


    # Método encargado de refrescar las pestañas de visualización y estadísticas
    def actualizar_visualizacion(self):
        """Refresca la tabla y los gráficos de estadísticas."""
        try:
            # Aplica filtros en la pestaña de visualización (por ejemplo, actualiza la tabla)
            self.visualizacion_tab.aplicar_filtros()

            # Si la pestaña de estadísticas tiene gráficos de categorías, los actualiza
            if hasattr(self.estadisticas_tab, "actualizar_grafico_categorias"):
                self.estadisticas_tab.actualizar_grafico_categorias()

            # Si la pestaña de estadísticas tiene gráficos de estados, los actualiza
            if hasattr(self.estadisticas_tab, "actualizar_grafico_estados"):
                self.estadisticas_tab.actualizar_grafico_estados()

            # Cambia automáticamente a la pestaña de visualización
            self.tabs.setCurrentWidget(self.visualizacion_tab)

        # Si algo falla durante la actualización, muestra el error en consola
        except Exception as e:
            print(f"Error al actualizar la visualización: {e}")

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem
import db_queries as db

class VisualizacionIncidenciaTab(QWidget):
    def __init__(self):
        super().__init__()
        self.incidencias = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        filtros_layout = QHBoxLayout()

        # Filtro estado
        self.filtro_estado = QComboBox()
        self.filtro_estado.addItem("Todos")
        self.filtro_estado.addItems(["Abierta", "En progreso", "Cerrada"])
        self.filtro_estado.currentIndexChanged.connect(self.aplicar_filtros)
        filtros_layout.addWidget(QLabel("Estado:"))
        filtros_layout.addWidget(self.filtro_estado)

        # Filtro prioridad (categorías)
        self.filtro_prioridad = QComboBox()
        self.filtro_prioridad.addItem("Todas")
        categorias = db.obtener_categorias()
        for c in categorias:
            self.filtro_prioridad.addItem(c[1])
        self.filtro_prioridad.currentIndexChanged.connect(self.aplicar_filtros)
        filtros_layout.addWidget(QLabel("Prioridad:"))
        filtros_layout.addWidget(self.filtro_prioridad)

        layout.addLayout(filtros_layout)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Título", "Descripción", "Estado", "Prioridad"])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.aplicar_filtros()

    def aplicar_filtros(self):
        self.incidencias = db.obtener_incidencias()
        estado_filtro = self.filtro_estado.currentText()
        prioridad_filtro = self.filtro_prioridad.currentText()

        incidencias_filtradas = []
        for inc in self.incidencias:
            if estado_filtro != "Todos" and inc["estado"] != estado_filtro:
                continue
            if prioridad_filtro != "Todas" and inc["prioridad"] != prioridad_filtro:
                continue
            incidencias_filtradas.append(inc)

        self.llenar_tabla(incidencias_filtradas)

    def llenar_tabla(self, datos):
        self.tabla.setRowCount(len(datos))
        for fila, inc in enumerate(datos):
            self.tabla.setItem(fila, 0, QTableWidgetItem(inc["titulo"]))
            self.tabla.setItem(fila, 1, QTableWidgetItem(inc["descripcion"]))
            self.tabla.setItem(fila, 2, QTableWidgetItem(inc["estado"]))
            self.tabla.setItem(fila, 3, QTableWidgetItem(inc["prioridad"]))

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QTableWidget, QTableWidgetItem, QPushButton, QSizePolicy, QHeaderView
)
from PyQt5.QtCore import Qt
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

        # Filtro prioridad
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
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Título", "Descripción", "Estado", "Prioridad", "Acciones"])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)

        # Hacer la tabla responsive
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID ajustado
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Título ajustado
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Descripción ocupa más espacio
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Botones

        # Ajustar altura de filas automáticamente
        self.tabla.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabla.setWordWrap(True)

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
            id_in = inc.get("id_in", None)

            item_id = QTableWidgetItem(str(id_in))
            item_titulo = QTableWidgetItem(inc["titulo"])
            item_desc = QTableWidgetItem(inc["descripcion"])
            item_desc.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
            item_desc.setSizeHint(item_desc.sizeHint())

            self.tabla.setItem(fila, 0, item_id)
            self.tabla.setItem(fila, 1, item_titulo)
            self.tabla.setItem(fila, 2, item_desc)

            # Estado editable con ComboBox
            combo_estado = QComboBox()
            combo_estado.addItems(["Abierta", "En progreso", "Cerrada"])
            combo_estado.setCurrentText(inc["estado"])
            combo_estado.currentTextChanged.connect(lambda nuevo, i=id_in: self.actualizar_estado(i, nuevo))
            self.tabla.setCellWidget(fila, 3, combo_estado)

            self.tabla.setItem(fila, 4, QTableWidgetItem(inc["prioridad"]))

            # Botón Borrar más grande
            btn_borrar = QPushButton("Borrar")
            btn_borrar.setFixedHeight(35)
            btn_borrar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn_borrar.clicked.connect(lambda _, i=id_in: self.borrar_incidencia(i))

            layout_btns = QHBoxLayout()
            layout_btns.addWidget(btn_borrar)
            layout_btns.setContentsMargins(0, 0, 0, 0)
            layout_btns.setAlignment(Qt.AlignCenter)

            widget_btns = QWidget()
            widget_btns.setLayout(layout_btns)
            self.tabla.setCellWidget(fila, 5, widget_btns)

        # Autoajustar filas tras llenado
        self.tabla.resizeRowsToContents()

    def actualizar_estado(self, id_in, nuevo_estado):
        db.actualizar_estado_incidencia(id_in, nuevo_estado)
        self.aplicar_filtros()

    def borrar_incidencia(self, id_in):
        db.borrar_incidencia(id_in)
        self.aplicar_filtros()

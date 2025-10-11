from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
import db_queries as db
from modelo import vectorizer, model, preprocesar, predecir_prioridad, aprender_incidencia

class RegistroIncidenciaTab(QWidget):
    def __init__(self, actualizar_tabla_callback, id_us=1):
        super().__init__()
        self.actualizar_tabla_callback = actualizar_tabla_callback
        self.id_us = id_us  # Usuario logueado
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        self.input_titulo = QLineEdit()
        self.input_titulo.textChanged.connect(self.actualizar_prioridad_ia)
        layout.addWidget(QLabel("Título:"))
        layout.addWidget(self.input_titulo)

        # Descripción
        self.input_descripcion = QLineEdit()
        self.input_descripcion.textChanged.connect(self.actualizar_prioridad_ia)
        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.input_descripcion)

        # Estado
        layout.addWidget(QLabel("Estado:"))
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(["Abierta", "En progreso", "Cerrada"])
        layout.addWidget(self.combo_estado)

        # Prioridad / Categoría (desde BD)
        layout.addWidget(QLabel("Prioridad:"))
        self.combo_prioridad = QComboBox()
        self.categorias = db.obtener_categorias()
        for c in self.categorias:
            self.combo_prioridad.addItem(c[1])
        layout.addWidget(self.combo_prioridad)

        # Botón guardar
        btn_guardar = QPushButton("Registrar Incidencia")
        btn_guardar.clicked.connect(self.guardar_incidencia)
        layout.addWidget(btn_guardar)

        self.setLayout(layout)

        # Variable para guardar la prioridad predicha
        self.prioridad_predicha = None

    def actualizar_prioridad_ia(self):
        # La IA predice prioridad según título + descripción
        titulo = self.input_titulo.text().strip()
        descripcion = self.input_descripcion.text().strip()
        if titulo or descripcion:
            texto = f"{titulo} {descripcion}"
            try:
                self.prioridad_predicha = predecir_prioridad(texto)
                # Opcional: actualizar combo automáticamente
                for idx, cat in enumerate(self.categorias):
                    if cat[1].lower() == self.prioridad_predicha.lower():
                        self.combo_prioridad.setCurrentIndex(idx)
                        break
            except Exception:
                self.prioridad_predicha = None

    def guardar_incidencia(self):
        titulo = self.input_titulo.text().strip()
        descripcion = self.input_descripcion.text().strip()
        estado = self.combo_estado.currentText()
        id_cat = self.categorias[self.combo_prioridad.currentIndex()][0]

        if not titulo or not descripcion:
            QMessageBox.warning(self, "Error", "Debe completar título y descripción")
            return

        # Guardar en la BD
        db.insertar_incidencia(titulo, descripcion, estado, self.id_us, id_cat)

        # Aprender del nuevo registro
        if self.prioridad_predicha:
            texto = f"{titulo} {descripcion}"
            aprender_incidencia(texto, self.prioridad_predicha)

        QMessageBox.information(self, "Éxito", "Incidencia registrada correctamente")

        self.limpiar_campos()
        self.actualizar_tabla_callback()

    def limpiar_campos(self):
        self.input_titulo.clear()
        self.input_descripcion.clear()
        self.combo_estado.setCurrentIndex(0)
        self.combo_prioridad.setCurrentIndex(0)
        self.prioridad_predicha = None

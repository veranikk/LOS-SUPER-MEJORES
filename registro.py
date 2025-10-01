from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QDate

class RegistroIncidenciaTab(QWidget):
    def __init__(self, incidencias, actualizar_tabla_callback):
        super().__init__()
        self.incidencias = incidencias
        self.actualizar_tabla_callback = actualizar_tabla_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_titulo = QLineEdit()
        self.input_descripcion = QLineEdit()
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(["Abierta", "En Progreso", "Cerrada"])
        self.combo_prioridad = QComboBox()
        self.combo_prioridad.addItems(["Baja", "Media", "Alta"])
        self.fecha_incidente = QDateEdit()
        self.fecha_incidente.setDate(QDate.currentDate())
        self.fecha_incidente.setCalendarPopup(True)

        layout.addWidget(QLabel("Título:"))
        layout.addWidget(self.input_titulo)

        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.input_descripcion)

        layout.addWidget(QLabel("Estado:"))
        layout.addWidget(self.combo_estado)

        layout.addWidget(QLabel("Prioridad:"))
        layout.addWidget(self.combo_prioridad)

        layout.addWidget(QLabel("Fecha:"))
        layout.addWidget(self.fecha_incidente)

        btn_guardar = QPushButton("Registrar Incidencia")
        btn_guardar.clicked.connect(self.guardar_incidencia)
        layout.addWidget(btn_guardar)

        self.setLayout(layout)

    def guardar_incidencia(self):
        titulo = self.input_titulo.text().strip()
        descripcion = self.input_descripcion.text().strip()
        estado = self.combo_estado.currentText()
        prioridad = self.combo_prioridad.currentText()
        fecha = self.fecha_incidente.date().toString("yyyy-MM-dd")

        if not titulo or not descripcion:
            QMessageBox.warning(self, "Error", "Debe llenar título y descripción")
            return

        incidencia = {
            "titulo": titulo,
            "descripcion": descripcion,
            "estado": estado,
            "prioridad": prioridad,
            "fecha": fecha
        }
        self.incidencias.append(incidencia)
        QMessageBox.information(self, "Éxito", "Incidencia registrada")

        self.limpiar_campos()
        self.actualizar_tabla_callback()

    def limpiar_campos(self):
        self.input_titulo.clear()
        self.input_descripcion.clear()
        self.combo_estado.setCurrentIndex(0)
        self.combo_prioridad.setCurrentIndex(0)
        self.fecha_incidente.setDate(QDate.currentDate())

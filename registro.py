from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
import db_queries as db
from modelo import vectorizer, model, preprocesar, predecir_prioridad, aprender_incidencia

class RegistroIncidenciaTab(QWidget):
    #Este es el constructor de la clase de registros
    def __init__(self, actualizar_tabla_callback, id_us=1):
        super().__init__()
        self.actualizar_tabla_callback = actualizar_tabla_callback
        self.id_us = id_us 
        self.init_ui()

    # Este método se encarga de la interfaz de la pestaña de generar una incidencia
    def init_ui(self):
        layout = QVBoxLayout()

        # Este agrega la parte de titulo, es decir muestra un label y también el input para escribir el título
        self.input_titulo = QLineEdit()
        self.input_titulo.textChanged.connect(self.actualizar_prioridad_ia)
        layout.addWidget(QLabel("Título:"))
        layout.addWidget(self.input_titulo)

        # Este agrega la parte de descripción de la incidencia, junto con su label y también el input para escribirlo
        self.input_descripcion = QLineEdit()
        self.input_descripcion.textChanged.connect(self.actualizar_prioridad_ia)
        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.input_descripcion)

        # Este muestra un label de "Estado" y un desplegable con todas las opciones posibles de tipos de estado
        layout.addWidget(QLabel("Estado:"))
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(["Abierta", "En progreso", "Cerrada"])
        layout.addWidget(self.combo_estado)

        #Este muestra un desplegable con las opciones de prioridad que existen, estos se muestran según los que se encuentren dentro de la base de datos
        layout.addWidget(QLabel("Prioridad:"))
        self.combo_prioridad = QComboBox()
        self.categorias = db.obtener_categorias()
        for c in self.categorias:
            self.combo_prioridad.addItem(c[1])
        layout.addWidget(self.combo_prioridad)

        #Se agrega un boton de guardar y en caso de ser pinchado se ejecutará el método "guardar_incidencia"
        btn_guardar = QPushButton("Registrar Incidencia")
        btn_guardar.clicked.connect(self.guardar_incidencia)
        layout.addWidget(btn_guardar)

        self.setLayout(layout)

        #Esta parte del código se encarga de guardar la prioridad que ha predicho la inteligencia artificial
        self.prioridad_predicha = None

    #Este método lo usamos para predecir el tipo de prioridad según el contenidgo del título y de la descripción
    def actualizar_prioridad_ia(self):
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

    #Este método se encarga de guardar la incidencia dentro de la base de datos, este guardará en variables la información escrita y posteriormente se llamará al método de insertar datos
    #En caso de que el título o la descripción estén vacias, mostrará un mensaje de error
    def guardar_incidencia(self):
        titulo = self.input_titulo.text().strip()
        descripcion = self.input_descripcion.text().strip()
        estado = self.combo_estado.currentText()
        id_cat = self.categorias[self.combo_prioridad.currentIndex()][0]

        if not titulo or not descripcion:
            QMessageBox.warning(self, "Error", "Debe completar título y descripción")
            return
        db.insertar_incidencia(titulo, descripcion, estado, self.id_us, id_cat)

        # Esta parte enseña a la inteligencia artificial, y así aprender del nuevo registro
        if self.prioridad_predicha:
            texto = f"{titulo} {descripcion}"
            aprender_incidencia(texto, self.prioridad_predicha)

        QMessageBox.information(self, "Éxito", "Incidencia registrada correctamente")

        self.limpiar_campos()
        self.actualizar_tabla_callback()

    #Este método sirve para limpiar todos los campos de la pestaña
    def limpiar_campos(self):
        self.input_titulo.clear()
        self.input_descripcion.clear()
        self.combo_estado.setCurrentIndex(0)
        self.combo_prioridad.setCurrentIndex(0)
        self.prioridad_predicha = None

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import db_queries as db


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 350, 180)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Usuario
        h_usuario = QHBoxLayout()
        h_usuario.addWidget(QLabel("Usuario:"))
        self.input_usuario = QLineEdit()
        h_usuario.addWidget(self.input_usuario)
        self.layout.addLayout(h_usuario)

        # Contraseña
        h_contrasena = QHBoxLayout()
        h_contrasena.addWidget(QLabel("Contraseña:"))
        self.input_contrasena = QLineEdit()
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        h_contrasena.addWidget(self.input_contrasena)
        self.layout.addLayout(h_contrasena)

        # Correo (solo para registro)
        h_correo = QHBoxLayout()
        h_correo.addWidget(QLabel("Correo:"))
        self.input_correo = QLineEdit()
        h_correo.addWidget(self.input_correo)
        self.layout.addLayout(h_correo)
        self.input_correo.hide()
        self.h_correo_layout = h_correo

        # Botones
        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.validar_login)
        self.btn_registrar = QPushButton("Registrarse")
        self.btn_registrar.clicked.connect(self.mostrar_registro)
        self.layout.addWidget(self.btn_login)
        self.layout.addWidget(self.btn_registrar)

        self.setLayout(self.layout)
        self.modo_registro = False

    def validar_login(self):
        usuario = self.input_usuario.text().strip()
        contrasena = self.input_contrasena.text().strip()

        if not usuario or not contrasena:
            QMessageBox.warning(self, "Error", "Debe ingresar usuario y contraseña")
            return

        resultado = db.validar_usuario(usuario, contrasena)
        if resultado:
            id_us = resultado[0] if isinstance(resultado, tuple) else 1  # suponiendo que devuelve (id, usuario)
            QMessageBox.information(self, "Bienvenido", f"Usuario {usuario} validado")
            self.abrir_principal(id_us)
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def mostrar_registro(self):
        if not self.modo_registro:
            self.input_correo.show()
            self.modo_registro = True
            self.btn_registrar.setText("Confirmar Registro")
        else:
            usuario = self.input_usuario.text().strip()
            contrasena = self.input_contrasena.text().strip()
            correo = self.input_correo.text().strip()

            if not usuario or not contrasena or not correo:
                QMessageBox.warning(self, "Error", "Debe completar todos los campos")
                return

            # ✅ Validación de correo
            if "@" not in correo or "." not in correo:
                QMessageBox.warning(self, "Correo inválido", "El correo debe contener '@' y '.'")
                return

            try:
                db.crear_usuario(usuario, contrasena, correo)
                QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
                self.input_correo.hide()
                self.input_correo.clear()
                self.modo_registro = False
                self.btn_registrar.setText("Registrarse")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo registrar el usuario: {e}")

    def abrir_principal(self, id_us=1):
        """Abre la ventana principal después del login."""
        from main_window import MainWindow
        self.main_window = MainWindow(id_us=id_us)
        self.main_window.show()
        self.close()

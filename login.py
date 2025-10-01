from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        h_usuario = QHBoxLayout()
        h_usuario.addWidget(QLabel("Usuario:"))
        self.input_usuario = QLineEdit()
        h_usuario.addWidget(self.input_usuario)
        layout.addLayout(h_usuario)

        h_contrasena = QHBoxLayout()
        h_contrasena.addWidget(QLabel("Contraseña:"))
        self.input_contrasena = QLineEdit()
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        h_contrasena.addWidget(self.input_contrasena)
        layout.addLayout(h_contrasena)

        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.validar_login)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def validar_login(self):
        usuario = self.input_usuario.text()
        contrasena = self.input_contrasena.text()
        if usuario == "admin" and contrasena == "1234":
            self.abrir_principal()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def abrir_principal(self):
        from main_window import MainWindow  # Importar aquí para evitar ciclo
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

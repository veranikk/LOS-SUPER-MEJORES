from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import db_queries as db


class LoginWindow(QWidget):

    # Este es el constructor del login, este se ejecutará cuando se cree la ventana de login
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 350, 180)
        self.init_ui()

    # Crea un layout vertical, para poder gestionar y organizar todos los componentes que se encuentran dentro del mismo
    def init_ui(self):
        self.layout = QVBoxLayout()

        # Generamos un layout horizontal con la etiqueta usuario, para incluir el label y también el input donde escribir el nombre de usuario
        h_usuario = QHBoxLayout()
        h_usuario.addWidget(QLabel("Usuario:"))
        self.input_usuario = QLineEdit()
        h_usuario.addWidget(self.input_usuario)
        self.layout.addLayout(h_usuario)

        # Generamos un layout horizontal para la etiqueta de contraseña, la cual incluirá dentro un label y también un un input para escribirla
        h_contrasena = QHBoxLayout()
        h_contrasena.addWidget(QLabel("Contraseña:"))
        self.input_contrasena = QLineEdit()
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        h_contrasena.addWidget(self.input_contrasena)
        self.layout.addLayout(h_contrasena)

        # Generamos un layout horizontal para el apartado de correos, el cual incluirá lo mismo que las opciones anteriores
        h_correo = QHBoxLayout()
        h_correo.addWidget(QLabel("Correo:"))
        self.input_correo = QLineEdit()
        h_correo.addWidget(self.input_correo)
        self.layout.addLayout(h_correo)
        self.input_correo.hide()
        self.h_correo_layout = h_correo

        # Esta parte del código incluye los diferentes botones, y en caso de clicarlos se ejecutarán el validar_login, o mostrar_registro
        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.validar_login)
        self.btn_registrar = QPushButton("Registrarse")
        self.btn_registrar.clicked.connect(self.mostrar_registro)
        self.layout.addWidget(self.btn_login)
        self.layout.addWidget(self.btn_registrar)

        self.setLayout(self.layout)
        self.modo_registro = False

# Este método sirve para validar si el usuario es correcto o no, en caso de que no se haya escrito un usuario o contraseña mostrará un mensaje de error
# Se llamará al validar_usuario, en caso de que sea verdadero se mostrará una pestaña de bienvenido y se abrirá el panel principal
# En caso de que sea falso, se devolverá un mensaje de error de que el usuario o contraseña son incorrectos
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
# Este método sirve para poder registrar un nuevo usuario, este mostrará el input del correo para poder escribirlo, y un boton de registrar el usuario
# En caso de que el usuario, contraseña o correo no se hayan completado saldrá un mensaje de error, de que falta un campo por completar
# Además se validará de que el correo incluye un @ y un ., en caso de que no, se mostrará una ventana de error de que el correo debe contener dichos caractéres
# Se hará un try, donde se intentará crear el usuario, y se vaciará el campo de correo y se ocultará y se quitará el modo registro
# En caso de que el try muestre un error, debido a que al hacer el insert devuelva un error, mostrará un mensaje en pantalla de que no se ha podido registarr el usuario
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

# Este abrirá el menú principal
    def abrir_principal(self, id_us=1):
        #Abre la ventana principal después del login.
        from main_window import MainWindow
        self.main_window = MainWindow(id_us=id_us)
        self.main_window.show()
        self.close()

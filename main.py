import sys
from PyQt5.QtWidgets import QApplication
from login import LoginWindow

# Este bloque garantiza que el código dentro solo se ejecute
# si este archivo es ejecutado directamente, y no importado como módulo.
if __name__ == '__main__':
    
    # Crea una instancia de QApplication, necesaria para cualquier aplicación PyQt.
    # 'sys.argv' pasa los argumentos de la línea de comandos a la aplicación.
    app = QApplication(sys.argv)
    
    # Crea una instancia de la ventana de inicio de sesión definida en 'login.py'.
    login = LoginWindow()
    
    # Muestra la ventana en pantalla.
    login.show()
    
    # Inicia el bucle principal del programa, que espera eventos (clics, teclas, etc.)
    # hasta que el usuario cierre la aplicación. 'sys.exit()' asegura una salida limpia.
    sys.exit(app.exec_())
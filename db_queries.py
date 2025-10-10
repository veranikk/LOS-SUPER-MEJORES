import sqlite3

DB_PATH = "C:\\Users\\Tarde\\VERA\\PYTHON PARA APP DE IA\\Proyecto APP\\BBDD\\BBDD-SQLITE.db"  

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def close_db(conn):
    conn.commit()
    conn.close()

# ================= Usuarios =================
def obtener_usuarios():
    conn, cursor = connect_db()
    cursor.execute("SELECT id_us, nombre_us, correo_us FROM usuarios")
    usuarios = cursor.fetchall()
    close_db(conn)
    return usuarios

def validar_usuario(usuario, contrasena):
    conn, cursor = connect_db()
    cursor.execute("SELECT id_us, nombre_us FROM usuarios WHERE nombre_us=? AND contrasenia_us=?", (usuario, contrasena))
    resultado = cursor.fetchone()
    close_db(conn)
    return resultado

def crear_usuario(nombre, contrasena, correo):
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO usuarios (nombre_us, contrasenia_us, correo_us) VALUES (?, ?, ?)", (nombre, contrasena, correo))
    close_db(conn)

# ================= Categorías =================
def obtener_categorias():
    conn, cursor = connect_db()
    cursor.execute("SELECT id_cat, nivel FROM categorias")
    categorias = cursor.fetchall()
    close_db(conn)
    return categorias

# ================= Incidencias =================
def insertar_incidencia(titulo, descripcion, estado, id_us, id_cat, tiempo_resol=0):
    conn, cursor = connect_db()
    cursor.execute("""
        INSERT INTO incidencias (nombre_in, descripcion_in, estado_in, tiempo_resol, id_us, id_cat)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, descripcion, estado, tiempo_resol, id_us, id_cat))
    close_db(conn)

def obtener_incidencias():
    conn, cursor = connect_db()
    cursor.execute("""
        SELECT i.nombre_in, i.descripcion_in, i.estado_in, c.nivel, '2025-01-01'  -- fecha ficticia
        FROM incidencias i
        JOIN categorias c ON i.id_cat = c.id_cat
    """)
    resultados = cursor.fetchall()
    close_db(conn)
    incidencias = []
    for r in resultados:
        incidencias.append({
            "titulo": r[0],
            "descripcion": r[1],
            "estado": r[2],
            "prioridad": r[3],
            "fecha": r[4]
        })
    return incidencias

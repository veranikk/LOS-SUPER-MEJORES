import sqlite3

DB_PATH = r"BBDD-SQLITE.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def close_db(conn):
    conn.commit()
    conn.close()


# Este método sirve para devolver todos los datos de los usuarios existentes
def obtener_usuarios():
    conn, cursor = connect_db()
    cursor.execute("SELECT id_us, nombre_us, correo_us FROM usuarios")
    usuarios = cursor.fetchall()
    close_db(conn)
    return usuarios

# Este método sirve para verificar que el usuario y la contraseña introducida en la aplicación se encuentren dentro de la bbdd.
def validar_usuario(usuario, contrasena):
    conn, cursor = connect_db()
    cursor.execute(
        "SELECT id_us, nombre_us FROM usuarios WHERE nombre_us=? AND contrasenia_us=?",
        (usuario, contrasena)
    )
    resultado = cursor.fetchone()
    close_db(conn)
    return resultado

# Este método sirve para generar un nuevo usuario, este contendrá su nombre, contraseña y correo
def crear_usuario(nombre, contrasena, correo):
    conn, cursor = connect_db()
    cursor.execute(
        "INSERT INTO usuarios (nombre_us, contrasenia_us, correo_us) VALUES (?, ?, ?)",
        (nombre, contrasena, correo)
    )
    close_db(conn)


# Este método sirve para devolver todos los datos de la tabla de categorías
def obtener_categorias():
    conn, cursor = connect_db()
    cursor.execute("SELECT id_cat, nivel FROM categorias")
    categorias = cursor.fetchall()
    close_db(conn)
    return categorias


# Este sirve para insertar una nueva incidencia dentro de la bbdd, junto con su titulo, descripción, estado, id del usuario, id de la categoría, el tiempode resolución siempre será 0
def insertar_incidencia(titulo, descripcion, estado, id_us, id_cat, tiempo_resol=0):
    conn, cursor = connect_db()
    cursor.execute("""
        INSERT INTO incidencias (nombre_in, descripcion_in, estado_in, tiempo_resol, id_us, id_cat)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, descripcion, estado, tiempo_resol, id_us, id_cat))
    close_db(conn)

# Este sirve para mostrar todas las incidencias que se encuentren dentro de la bbdd, devolverá todos los campos, se guardan los datos dentro de una array llamada incidencias
def obtener_incidencias():
    conn, cursor = connect_db()
    cursor.execute("""
        SELECT i.id_in, i.nombre_in, i.descripcion_in, i.estado_in, c.nivel, i.tiempo_resol
        FROM incidencias i
        JOIN categorias c ON i.id_cat = c.id_cat
    """)
    resultados = cursor.fetchall()
    close_db(conn)
    incidencias = []
    for r in resultados:
        incidencias.append({
            "id_in": r[0],
            "titulo": r[1],
            "descripcion": r[2],
            "estado": r[3],
            "prioridad": r[4] if r[4] else r[5],  # usar nivel de categoría o tiempo_resol como fallback
        })
    return incidencias

# Este sirve para borrar una incidencia de la bbdd, para esto tendremos que pasarle como parametro la id de la incidencia, para saber cual de todas borrar
def borrar_incidencia(id_in):
    conn, cursor = connect_db()
    cursor.execute("DELETE FROM incidencias WHERE id_in=?", (id_in,))
    close_db(conn)

# Este sirve para actualizar una incidencia de nuestra bbdd, esta dependerá de la id de la incidencia que pasemos como parámetro
def actualizar_estado_incidencia(id_in, nuevo_estado):
    conn, cursor = connect_db()
    cursor.execute("UPDATE incidencias SET estado_in=? WHERE id_in=?", (nuevo_estado, id_in))
    close_db(conn)

import psycopg2
import os

def conectar():
    try:
        # Configuración de la conexión
        conn = psycopg2.connect(
            host=os.getenv("Host"),
            dbname=os.getenv("Database"),
            port=os.getenv("Port"),
            user=os.getenv("User"),
            password=os.getenv("Password")
        )
        return conn
    except Exception as e:
        print("Error al establecer la conexión:", e)
        return None

def crear_tablas():
    # Crear tablas
    db = conectar()
    cursor = db.cursor()

    # Crear esquema
    cursor.execute("CREATE SCHEMA IF NOT EXISTS schema_juegos_docentes;")

    # cursor.execute("DROP SCHEMA IF EXISTS schema_juegos_docentes CASCADE;")
    # cursor.execute("DROP TABLE IF EXISTS schema_juegos_docentes.solicitudes CASCADE;")
    # cursor.execute("DROP TABLE IF EXISTS schema_juegos_docentes.valoraciones CASCADE;")
    # cursor.execute("DROP TABLE IF EXISTS schema_juegos_docentes.juegos CASCADE;")
    # cursor.execute("DROP TABLE IF EXISTS schema_juegos_docentes.usuarios CASCADE;")
    
    # Tabla de usuarios
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.usuarios "
    "(id SERIAL PRIMARY KEY, "
    "usuario VARCHAR(50) UNIQUE NOT NULL, "
    "nombre VARCHAR(50) NOT NULL, "
    "apellido VARCHAR(50) NOT NULL, "
    "institucion VARCHAR(100) NOT NULL, "
    "contraseña VARCHAR(150), "
    "rol TEXT DEFAULT 'usuario', "
    "borrado VARCHAR(5) DEFAULT 'N');"
    )

    # Tabla de juegos
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos "
        "(id SERIAL PRIMARY KEY, "
        "nombre_juego VARCHAR(100), "
        "descripcion TEXT, "
        "idioma VARCHAR(100), "
        "enlace VARCHAR(200), "
        "puntuacion NUMERIC(2,1), "

        "disciplina VARCHAR(100), "
        "naturaleza VARCHAR(100), "
        "precio VARCHAR(100), "
        "instrucciones VARCHAR(100), "
        "notas_instructor VARCHAR(100), "

        "objetivos TEXT, "
        "espacio_control TEXT, "

        "objetivos_principales TEXT, "
        "objetivos_secundarios TEXT, "

        "estructura_sesiones TEXT, "
        "aspectos_adicionales TEXT, "

        "entretenimiento VARCHAR(100), "
        "aprendizaje VARCHAR(100), "
        "complejidad_alumno VARCHAR(100), "
        "complejidad_instructores VARCHAR(100), "
        "youtube_url VARCHAR(150), "

        "id_usuario_creacion INTEGER REFERENCES schema_juegos_docentes.usuarios(id), "
        "fecha_creacion TIMESTAMP DEFAULT NOW(), "
        
        "id_usuario_modificacion INTEGER REFERENCES schema_juegos_docentes.usuarios(id), "
        "fecha_modificacion TIMESTAMP DEFAULT NOW(), "

        "puntuacion_media_usuario NUMERIC(2,1), "
        "estrellas_general INTEGER, "
    
        "archivo_instrucciones_jugador VARCHAR(50), "
        "archivo_instrucciones_instructor VARCHAR(50), "
        "archivo_juego VARCHAR(50), "

        "borrado VARCHAR(5) DEFAULT 'N');"
    )

    # Tabla de solicitudes para obtener el rol de profesor
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.solicitudes "
    "(id SERIAL PRIMARY KEY, "
    "estado VARCHAR(50) NOT NULL, "
    "id_usuario_solicitud INTEGER REFERENCES schema_juegos_docentes.usuarios(id), "
    "fecha_solicitud TIMESTAMP DEFAULT NOW());"
    )

    # Tabla de puntuaciones
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.valoraciones "
    "(id SERIAL PRIMARY KEY, "
    "puntuacion NUMERIC(2,1), "
    "estrellas_individual INTEGER, "
    "comentario TEXT, "
    "fecha_valoracion TIMESTAMP DEFAULT NOW(), "
    "id_usuario_valoracion INTEGER REFERENCES schema_juegos_docentes.usuarios(id), "
    "id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id)); "
    )

    # passhash = generate_password_hash('12345')
    # Insertar usuario de prueba
    # cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (usuario, nombre, apellido, institucion, edad, genero, contraseña, rol) VALUES ('usuarioPrueba', 'este', 'este', 'este', '21','Femenino', %s, 'administrador');", (passhash,))
    # cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (usuario, contraseña) VALUES ('usuarioPrueba', '12345');")
    # Eliminar usuario de prueba
    # cursor.execute("DELETE FROM schema_juegos_docentes.usuarios WHERE usuario = 'usuarioPrueba';")
    
    # Confirmar cambios y cerrar cursor
    db.commit()
    cursor.close()
    
    # Cerrar conexión
    db.close()

import psycopg2
import os
import logging

# Conexión con la base de datos.
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
        logging.error("Error al establecer la conexión: %s", str(e))

def crear_tablas():
    try:
        db = conectar()
        cursor = db.cursor()

        # Tabla de usuarios
        cursor.execute(
        "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.usuarios "
        "(id SERIAL PRIMARY KEY, "
        "usuario VARCHAR(50) UNIQUE NOT NULL, "
        "nombre VARCHAR(50) NOT NULL, "
        "apellido VARCHAR(50) NOT NULL, "
        "institucion VARCHAR(50) NOT NULL, "
        "contraseña VARCHAR(50), "
        "rol TEXT DEFAULT 'usuario', "
        "borrado VARCHAR(5) DEFAULT 'N');"
        )

        # Tabla de juegos
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos "
            "(id SERIAL PRIMARY KEY, "
            "nombre_juego VARCHAR(50), "
            "descripcion TEXT, "
            "idioma VARCHAR(50), "
            "enlace TEXT, "
            "puntuacion NUMERIC(2,1), "

            "disciplina VARCHAR(50), "
            "naturaleza VARCHAR(50), "
            "precio VARCHAR(50), "
            "instrucciones VARCHAR(50), "
            "notas_instructor VARCHAR(50), "

            "objetivos TEXT, "
            "espacio_control TEXT, "

            "objetivos_principales TEXT, "
            "objetivos_secundarios TEXT, "

            "estructura_sesiones TEXT, "
            "aspectos_adicionales TEXT, "

            "entretenimiento VARCHAR(50), "
            "aprendizaje VARCHAR(50), "
            "complejidad_alumno VARCHAR(50), "
            "complejidad_instructores VARCHAR(50), "
            "youtube_url TEXT, "

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

        # Tabla de valoraciones
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
    except Exception as e:
        logging.error("Ocurrió un error en la función crear_tablas: %s", str(e))
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
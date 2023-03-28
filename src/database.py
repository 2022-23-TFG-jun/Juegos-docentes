import psycopg2
from werkzeug.security import generate_password_hash

def tabla_usuarios_existe():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'usuarios'
            AND table_schema = 'public'
        );
    """)
    existe = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return existe

def conectar():
    conn = psycopg2.connect(
        host="localhost",
        database="juegos_docentes",
        user="admin",
        password="1234"
    )
    return conn

def crear_tablas():
    # Configuración de la conexión
    conn = psycopg2.connect(database="juegos_docentes", user="admin", password="1234", host="localhost", port="5432")
    
    # Crear tabla
    cursor = conn.cursor()
    
    # Crear el tipo de datos ENUM
    # cursor.execute("DROP TYPE IF EXISTS schema_juegos_docentes.genero_enum;")
    # cursor.execute("DROP TABLE schema_juegos_docentes.usuarios CASCADE;")
    # cursor.execute("DROP TYPE IF EXISTS schema_juegos_docentes.genero_enum;")
    # cursor.execute("CREATE TYPE schema_juegos_docentes.genero_enum AS ENUM ('Masculino', 'Femenino', 'Prefiero no contestar');")

    # Tabla de usuarios
    # cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.usuarios (id SERIAL PRIMARY KEY, usuario VARCHAR(50), contraseña VARCHAR(150), rol VARCHAR(20));")
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.usuarios "
    "(id SERIAL PRIMARY KEY, "
    " usuario VARCHAR(50) UNIQUE NOT NULL, "
    " nombre VARCHAR(50) NOT NULL, "
    "apellido VARCHAR(50) NOT NULL, "
    "institucion VARCHAR(100) NOT NULL, "
    "contraseña VARCHAR(150), "
    "rol TEXT DEFAULT 'usuario'); "
    )

    # Tabla de juegos
    # cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos (id SERIAL PRIMARY KEY, nombre_juego VARCHAR(100), enlace VARCHAR(200), id_usuario INTEGER REFERENCES schema_juegos_docentes.usuarios(id), fecha TIMESTAMP);")
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos "
    "(id SERIAL PRIMARY KEY, "
    "nombre_juego VARCHAR(100), "
    "enlace VARCHAR(200), "
    "fecha TIMESTAMP DEFAULT NOW(), "
    "id_usuario INTEGER REFERENCES schema_juegos_docentes.usuarios(id)); "
    )

    # Tabla de la categorización de los juegos
    # cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_categorizacion (id SERIAL PRIMARY KEY, disciplina VARCHAR(100), naturaleza VARCHAR(100), idioma VARCHAR(100), precio VARCHAR(100); instrucciones VARCHAR(100), notas_instructor VARCHAR(100), id_juego INTEGER REFERENCES juegos(id));")
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_categorizacion "
    "(id SERIAL PRIMARY KEY, "
    "disciplina VARCHAR(100), "
    "naturaleza VARCHAR(100), "
    "idioma VARCHAR(100), "
    "precio VARCHAR(100), "
    "instrucciones VARCHAR(100), "
    "notas_instructor VARCHAR(100), "
    "id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id)); "
    )

    # Tabla de la descripción de los juegos
    # cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_descripcion (id SERIAL PRIMARY KEY, contexto VARCHAR(200), objetivos VARCHAR(100), espacio_control VARCHAR(100), id_juego INTEGER REFERENCES juegos(id));")
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_descripcion "
    "(id SERIAL PRIMARY KEY, "
    "contexto VARCHAR(200), "
    "objetivos VARCHAR(100), "
    "espacio_control VARCHAR(100), "
    "id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id)); "
    )

    # Tabla del aprendizaje de los juegos
    # cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_aprendizaje (id SERIAL PRIMARY KEY, objetivos_principales VARCHAR(100), objetivos_secundarios VARCHAR(100), id_juego INTEGER REFERENCES juegos(id));")
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_aprendizaje "
    "(id SERIAL PRIMARY KEY, "
    "objetivos_principales VARCHAR(100), "
    "objetivos_secundarios VARCHAR(100), "
    "id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id)); "
    )

    # Tabla de la organización de los juegos
    # cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_organización (id SERIAL PRIMARY KEY, estructura_sesiones VARCHAR(100), aspectos_adicionales VARCHAR(100), id_juego INTEGER REFERENCES juegos(id));")
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_organización "
    "(id SERIAL PRIMARY KEY, "
    "estructura_sesiones VARCHAR(100), "
    "aspectos_adicionales VARCHAR(100), "
    "id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id)); "
    )

    # Tabla de la valoración del profesor de los juegos
    # cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_valoracion_profesor (id SERIAL PRIMARY KEY, entretenimiento VARCHAR(100), aprendizaje VARCHAR(100), complejidad_alumno VARCHAR(100), complejidad_instructores VARCHAR(100), id_juego INTEGER REFERENCES juegos(id));")
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_valoracion_profesor "
    "(id SERIAL PRIMARY KEY, "
    "entretenimiento VARCHAR(100), "
    "aprendizaje VARCHAR(100), "
    "complejidad_alumno VARCHAR(100), "
    "complejidad_instructores VARCHAR(100), "
    "id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id)); "
    )

    # Tabla de puntuaciones
    # cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_puntuaciones (id SERIAL PRIMARY KEY,id_usuario INTEGER REFERENCES schema_juegos_docentes.usuarios(id), id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id), puntuacion INTEGER,fecha TIMESTAMP DEFAULT NOW());")
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_puntuaciones "
    "(id SERIAL PRIMARY KEY, "
    "puntuacion INTEGER, "
    "fecha TIMESTAMP DEFAULT NOW(), "
    "id_usuario INTEGER REFERENCES schema_juegos_docentes.usuarios(id), "
    "id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id)); "
    )

    # Tabla de comentarios
    # cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_comentarios (id SERIAL PRIMARY KEY, id_usuario INTEGER REFERENCES schema_juegos_docentes.usuarios(id), id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id),comentario TEXT,fecha TIMESTAMP));")
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS schema_juegos_docentes.juegos_comentarios "
    "(id SERIAL PRIMARY KEY, "
    "comentario TEXT, "
    "fecha TIMESTAMP DEFAULT NOW(), "
    "id_usuario INTEGER REFERENCES schema_juegos_docentes.usuarios(id), "
    "id_juego INTEGER REFERENCES schema_juegos_docentes.juegos(id)); "
    )

    # passhash = generate_password_hash('12345')
    # Insertar usuario de prueba
    # cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (usuario, nombre, apellido, institucion, edad, genero, contraseña, rol) VALUES ('usuarioPrueba', 'este', 'este', 'este', '21','Femenino', %s, 'administrador');", (passhash,))
    # cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (usuario, contraseña) VALUES ('usuarioPrueba', '12345');")
    # Eliminar usuario de prueba
    # cursor.execute("DELETE FROM schema_juegos_docentes.usuarios WHERE usuario = 'usuarioPrueba';")
    
    # Confirmar cambios y cerrar cursor
    conn.commit()
    cursor.close()
    
    # Cerrar conexión
    conn.close()

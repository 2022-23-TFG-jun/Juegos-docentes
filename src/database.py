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
    # Código de configuración de la conexión
    conn = psycopg2.connect(database="juegos_docentes", user="admin", password="1234", host="localhost", port="5432")
    
    # Crear tabla
    cursor = conn.cursor()
    #cursor.execute("DROP TABLE schema_juegos_docentes.usuarios CASCADE;")
    cursor.execute("CREATE TABLE IF NOT EXISTS schema_juegos_docentes.usuarios (id SERIAL PRIMARY KEY, usuario VARCHAR(50), contraseña VARCHAR(150), rol VARCHAR(20));")
    

    #passhash = generate_password_hash('12345')
    # Insertar usuario de prueba
    #cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (usuario, contraseña, rol) VALUES ('usuarioPrueba', %s, 'usuario');", (passhash,))
    #cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (usuario, contraseña) VALUES ('usuarioPrueba', '12345');")
    
    # Eliminar usuario de prueba
    # cursor.execute("DELETE FROM schema_juegos_docentes.usuarios WHERE usuario = 'usuarioPrueba';")
    
    # Confirmar cambios y cerrar cursor
    conn.commit()
    cursor.close()
    
    # Cerrar conexión
    conn.close()

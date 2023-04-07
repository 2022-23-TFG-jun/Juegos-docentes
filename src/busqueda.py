from src.database import conectar
# Convertir cadenas de texto Unicode a cadenas ASCII
from unidecode import unidecode

def obtener_resultados_busqueda(busqueda, idioma, puntuacion):
    # Convertir contenido de busqueda e idioma en minúsculas y normalizarla
    busqueda = unidecode(busqueda.lower())
    idioma = unidecode(idioma.lower())

    # Establecer la conexión a la base de datos
    conn = conectar()

    # Crear un cursor para ejecutar la consulta
    cur = conn.cursor()

    # Extensión PostgreSQL. Función que quita los acentos de las letras en una cadena
    cur.execute("CREATE EXTENSION IF NOT EXISTS unaccent")

    # Si búsqueda tiene un valor se asigna a sí misma, si no se le asigna cualquier cadena de caracteres
    busqueda = busqueda if busqueda else '%'

    # Si idioma tiene un valor se asigna a sí mismo, si no se le asigna cualquier cadena de caracteres
    idioma = idioma if idioma else '%'

    # Si puntuación tiene un valor se asigna a sí misma, si no se le asigna un número decimal
    puntuacion = puntuacion if puntuacion else '[0-5].[0-9]'

    cur.execute("SELECT nombre_juego, descripcion, idioma, enlace, puntuacion "
            "FROM schema_juegos_docentes.juegos "
            "WHERE (unaccent(lower(nombre_juego)) LIKE %s "
            "OR unaccent(lower(descripcion)) LIKE %s "
            "OR unaccent(lower(idioma)) LIKE %s) "
            "AND (unaccent(lower(idioma)) LIKE %s "
            "AND (CAST(puntuacion as VARCHAR) SIMILAR TO %s))",
            (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", idioma, puntuacion))

    # Obtener el resultado de la consulta
    resultados_busqueda = cur.fetchall()
    
    # Cerrar el cursor y la conexión a la base de datos
    cur.close()
    conn.close()
    
    return resultados_busqueda

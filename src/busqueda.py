from src.database import conectar
# Convertir cadenas de texto Unicode a cadenas ASCII
from unidecode import unidecode
import logging

def obtener_resultados_busqueda(busqueda, idiomaF, puntuacion, juegos_por_pagina, desplazamiento):
        try:
                # Convertir contenido de busqueda e idioma en minúsculas y normalizarla
                busqueda = unidecode(busqueda.lower())
                idiomaF = unidecode(idiomaF.lower())
                
                # Establecer la conexión a la base de datos
                conn = conectar()

                # Crear un cursor para ejecutar la consulta
                cur = conn.cursor()

                # Extensión PostgreSQL. Función que quita los acentos de las letras en una cadena
                cur.execute("CREATE EXTENSION IF NOT EXISTS unaccent")

                # Si búsqueda tiene un valor se asigna a sí misma, si no se le asigna cualquier cadena de caracteres
                busqueda = busqueda if busqueda else '%'

                # Si idioma tiene un valor se asigna a sí mismo, si no se le asigna cualquier cadena de caracteres
                idiomaF = idiomaF if idiomaF else '%'

                # Si puntuación tiene un valor se asigna a sí misma, si no se le asigna un número decimal
                puntuacion = puntuacion if puntuacion else '[0-5].[0-9]'
                
                cur.execute("SELECT id, nombre_juego, descripcion, idioma, enlace, puntuacion, puntuacion_media_usuario, estrellas_general "
                        "FROM schema_juegos_docentes.juegos "
                        "WHERE (unaccent(lower(nombre_juego)) LIKE %s "
                        "OR unaccent(lower(descripcion)) LIKE %s "
                        "OR unaccent(lower(idioma)) LIKE %s) "
                        "AND (unaccent(lower(idioma)) LIKE %s "
                        "AND (CAST(puntuacion as VARCHAR) SIMILAR TO %s)) "
                        "AND borrado='N'"
                        "ORDER BY nombre_juego "
                        "LIMIT %s OFFSET %s ",

                        (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", idiomaF, puntuacion, juegos_por_pagina, desplazamiento))

                # Obtener el resultado de la consulta de todos los juegos (4 por página)
                resultados_busqueda = cur.fetchall()

                cur.execute("SELECT nombre_juego, descripcion, idioma, enlace, puntuacion, puntuacion_media_usuario, estrellas_general "
                        "FROM schema_juegos_docentes.juegos "
                        "WHERE (unaccent(lower(nombre_juego)) LIKE %s "
                        "OR unaccent(lower(descripcion)) LIKE %s "
                        "OR unaccent(lower(idioma)) LIKE %s) "
                        "AND (unaccent(lower(idioma)) LIKE %s "
                        "AND (CAST(puntuacion as VARCHAR) SIMILAR TO %s)) "
                        "AND borrado='N'"
                        "ORDER BY nombre_juego",

                        (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", idiomaF, puntuacion))
                
                # Obtener el resultado de la consulta del número total de juegos de la búsqueda
                total_juegos =  len(cur.fetchall())

                # Cerrar el cursor y la conexión a la base de datos
                cur.close()
                conn.close()

                return resultados_busqueda, total_juegos

        except Exception as e:
                logging.error("Ocurrió un error en la función obtener_resultados_busqueda: %s", str(e))
                return None, None

"""
from src.database import conectar
# Convertir cadenas de texto Unicode a cadenas ASCII
from unidecode import unidecode

def obtener_resultados_busqueda(busqueda, idiomaF, puntuacion, juegos_por_pagina, desplazamiento):
    # Convertir contenido de busqueda e idioma en minúsculas y normalizarla
    busqueda = unidecode(busqueda.lower())
    idiomaF = unidecode(idiomaF.lower())
 
    # Establecer la conexión a la base de datos
    conn = conectar()

    # Crear un cursor para ejecutar la consulta
    cur = conn.cursor()

    # Extensión PostgreSQL. Función que quita los acentos de las letras en una cadena
    cur.execute("CREATE EXTENSION IF NOT EXISTS unaccent")

    # Si búsqueda tiene un valor se asigna a sí misma, si no se le asigna cualquier cadena de caracteres
    busqueda = busqueda if busqueda else '%'

    # Si idioma tiene un valor se asigna a sí mismo, si no se le asigna cualquier cadena de caracteres
    idiomaF = idiomaF if idiomaF else '%'

    # Si puntuación tiene un valor se asigna a sí misma, si no se le asigna un número decimal
    puntuacion = puntuacion if puntuacion else '[0-5].[0-9]'
 
    cur.execute("SELECT id, nombre_juego, descripcion, idioma, enlace, puntuacion, puntuacion_media_usuario, estrellas_general "
            "FROM schema_juegos_docentes.juegos "
            "WHERE (unaccent(lower(nombre_juego)) LIKE %s "
            "OR unaccent(lower(descripcion)) LIKE %s "
            "OR unaccent(lower(idioma)) LIKE %s) "
            "AND (unaccent(lower(idioma)) LIKE %s "
            "AND (CAST(puntuacion as VARCHAR) SIMILAR TO %s)) "
            "ORDER BY nombre_juego "
            "LIMIT %s OFFSET %s ",

            (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", idiomaF, puntuacion, juegos_por_pagina, desplazamiento))

    # Obtener el resultado de la consulta de todos los juegos (4 por página)
    resultados_busqueda = cur.fetchall()

    cur.execute("SELECT nombre_juego, descripcion, idioma, enlace, puntuacion, puntuacion_media_usuario, estrellas_general "
            "FROM schema_juegos_docentes.juegos "
            "WHERE (unaccent(lower(nombre_juego)) LIKE %s "
            "OR unaccent(lower(descripcion)) LIKE %s "
            "OR unaccent(lower(idioma)) LIKE %s) "
            "AND (unaccent(lower(idioma)) LIKE %s "
            "AND (CAST(puntuacion as VARCHAR) SIMILAR TO %s)) "
            "ORDER BY nombre_juego",

            (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", idiomaF, puntuacion))
    
    # Obtener el resultado de la consulta del número total de juegos de la búsqueda
    total_juegos =  len(cur.fetchall())

    # Cerrar el cursor y la conexión a la base de datos
    cur.close()
    conn.close()

    return resultados_busqueda, total_juegos
"""
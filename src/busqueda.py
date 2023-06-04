from src.database import conectar
from unidecode import unidecode # Convertir cadenas de texto Unicode a cadenas ASCII
import logging

def obtener_resultados_busqueda(busqueda, idiomaF, puntuacion, juegos_por_pagina, desplazamiento):
        try:
                # Convertir contenido de busqueda e idioma en minúsculas y normalizarla
                busqueda = unidecode(busqueda.lower())
                idiomaF = unidecode(idiomaF.lower())
                
                # Establecer la conexión a la base de datos
                db = conectar()

                # Crear un cursor para ejecutar la consulta
                cursor = db.cursor()

                # Extensión PostgreSQL. Función para quitar acentos de una cadena
                cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent")

                # Si búsqueda tiene un valor se asigna a sí misma, si no se le asigna cualquier cadena de caracteres
                busqueda = busqueda if busqueda else '%'

                # Si idioma tiene un valor se asigna a sí mismo, si no se le asigna cualquier cadena de caracteres
                idiomaF = idiomaF if idiomaF else '%'

                # Si puntuación tiene un valor se asigna a sí misma, si no se le asigna un número decimal
                puntuacion = puntuacion if puntuacion else '[0-5].[0-9]'

                idioma2 = idiomaF
                if idiomaF == "espanol":
                        idioma2 = "spanish"
                elif idiomaF == "ingles":
                        idioma2 = "english"    
                elif idiomaF == "spanish":
                        idioma2 = "espanol"
                elif idiomaF == "english":
                        idioma2 = "ingles"
                elif idiomaF == "espanol o ingles":
                        idioma2 = "spanish or english"
                elif idiomaF == "spanish or english":
                        idioma2 = "espanol o ingles"

                cursor.execute("SELECT id, nombre_juego, descripcion, idioma, enlace, puntuacion, puntuacion_media_usuario, estrellas_general "
                        "FROM schema_juegos_docentes.juegos "
                        "WHERE (unaccent(lower(nombre_juego)) LIKE %s "
                        "OR unaccent(lower(descripcion)) LIKE %s "
                        "OR unaccent(lower(idioma)) LIKE %s) "

                        "AND ((unaccent(lower(idioma)) LIKE %s "
                        "OR unaccent(lower(idioma)) LIKE %s) "
                        "AND (CAST(puntuacion as VARCHAR) SIMILAR TO %s)) "
                        "AND borrado='N' "
                        "ORDER BY nombre_juego "
                        "LIMIT %s OFFSET %s ",

                        (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", idiomaF, idioma2, puntuacion, juegos_por_pagina, desplazamiento))

                # Obtener el resultado de la consulta de todos los juegos (3 por página)
                resultados_busqueda = cursor.fetchall()

                cursor.execute("SELECT nombre_juego, descripcion, idioma, enlace, puntuacion, puntuacion_media_usuario, estrellas_general "
                        "FROM schema_juegos_docentes.juegos "
                        "WHERE (unaccent(lower(nombre_juego)) LIKE %s "
                        "OR unaccent(lower(descripcion)) LIKE %s "
                        "OR unaccent(lower(idioma)) LIKE %s) "

                        "AND ((unaccent(lower(idioma)) LIKE %s "
                        "OR unaccent(lower(idioma)) LIKE %s) "
                        "AND (CAST(puntuacion as VARCHAR) SIMILAR TO %s)) "
                        "AND borrado='N' "
                        "ORDER BY nombre_juego",

                        (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", idiomaF, idioma2, puntuacion))
                
                # Obtener el resultado de la consulta del número total de juegos de la búsqueda
                total_juegos =  len(cursor.fetchall())

                # Cerrar el cursor y la conexión a la base de datos
                cursor.close()
                db.close()

                return resultados_busqueda, total_juegos
        except Exception as e:
                logging.error("Ocurrió un error en la función obtener_resultados_busqueda: %s", str(e))
                return None, None   
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
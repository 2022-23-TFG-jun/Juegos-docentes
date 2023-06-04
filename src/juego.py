from src.database import conectar
import logging

class Juego():
    def crear_juego(nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, 
                    instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, 
                    estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, 
                    youtube_url, fecha_creacion, id_usuario_creacion):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("INSERT INTO schema_juegos_docentes.juegos (nombre_juego, descripcion, idioma, enlace, puntuacion, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, youtube_url, fecha_creacion, id_usuario_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, youtube_url, fecha_creacion, id_usuario_creacion))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al crear un juego nuevo: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def añadir_instrucciones_jugador(archivo_instrucciones_jugador, id_juego):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("UPDATE schema_juegos_docentes.juegos SET archivo_instrucciones_jugador = %s WHERE id = %s", (archivo_instrucciones_jugador, id_juego))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al añadir el archivo de las instrucciones del jugador: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def añadir_instrucciones_instructor(archivo_instrucciones_instructor, id_juego):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("UPDATE schema_juegos_docentes.juegos SET archivo_instrucciones_instructor = %s WHERE id = %s", (archivo_instrucciones_instructor, id_juego))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al añadir el archivo de las instrucciones del instructor: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def añadir_archivo_juego(archivo_juego, id_juego):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("UPDATE schema_juegos_docentes.juegos SET archivo_juego = %s WHERE id = %s", (archivo_juego, id_juego))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al añadir el archivo del juego: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def modificar_juego(nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, 
                    instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, 
                    estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, 
                    youtube_url, fecha_modificacion, id_usuario_modificacion, id_juego):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("UPDATE schema_juegos_docentes.juegos SET nombre_juego=%s, descripcion=%s, idioma=%s, enlace=%s, puntuacion=%s, disciplina=%s, naturaleza=%s, precio=%s, instrucciones=%s, notas_instructor=%s, objetivos=%s, espacio_control=%s, objetivos_principales=%s, objetivos_secundarios=%s, estructura_sesiones=%s, aspectos_adicionales=%s, entretenimiento=%s, aprendizaje=%s, complejidad_alumno=%s, complejidad_instructores=%s, youtube_url=%s, fecha_modificacion=%s, id_usuario_modificacion=%s WHERE id=%s", (nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, youtube_url, fecha_modificacion, id_usuario_modificacion, id_juego))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al modificar un juego: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def eliminar_juego(id_juego):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("UPDATE schema_juegos_docentes.juegos SET borrado='S' WHERE id = %s", (id_juego,))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al eliminar un juego: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def obtener_juegos():
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT id, nombre_juego, idioma FROM schema_juegos_docentes.juegos WHERE borrado='N' ORDER BY id")
            juegos = cursor.fetchall()
            return juegos
        except Exception as e:
            logging.error("Ocurrió un error al obtener los juegos: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def obtener_juego_modificacion(id_juego):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM schema_juegos_docentes.juegos WHERE id = %s", (id_juego,))
            informacion_juego = cursor.fetchone()
            return informacion_juego
        except Exception as e:
            logging.error("Ocurrió un error al obtener el juego que se quiere modificar: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def obtener_juego_visualizacion(id_juego):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM schema_juegos_docentes.juegos WHERE id = %s", (id_juego,))
            informacion_juego = cursor.fetchone()
            return informacion_juego
        except Exception as e:
            logging.error("Ocurrió un error al obtener el juego que se quiere visualizar: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def obtener_juegos_menu(juegos_por_pagina, desplazamiento):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT id, nombre_juego, descripcion, idioma, enlace, puntuacion, puntuacion_media_usuario, estrellas_general FROM schema_juegos_docentes.juegos WHERE borrado='N' ORDER BY nombre_juego LIMIT %s OFFSET %s", (juegos_por_pagina, desplazamiento))
            juegos = cursor.fetchall()
            return juegos
        except Exception as e:
            logging.error("Ocurrió un error al obtener los juegos del menú: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def obtener_total_juegos():
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM schema_juegos_docentes.juegos WHERE borrado='N'")
            total_juegos = cursor.fetchone()[0]
            return total_juegos
        except Exception as e:
            logging.error("Ocurrió un error al obtener el número total de juegos: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
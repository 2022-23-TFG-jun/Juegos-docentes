from src.database import conectar
import logging

class Valoracion():
    def obtener_juegos_valorados(usuario_actual):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT id_juego FROM schema_juegos_docentes.valoraciones WHERE id_usuario_valoracion=%s", (usuario_actual,))
            juegos_valorados_actual = cursor.fetchall()
            return juegos_valorados_actual
        except Exception as e:
            logging.error("Ocurrió un error al obtener los juegos valorados: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def añadir_valoraciones(puntuacion, comentario, fecha_valoracion, id_usuario_valoracion, id_juego):
            try:
                db = conectar()
                cursor = db.cursor()
                cursor.execute("INSERT INTO schema_juegos_docentes.valoraciones (puntuacion, comentario, fecha_valoracion, id_usuario_valoracion, id_juego) VALUES (%s, %s, %s, %s, %s)", (puntuacion, comentario, fecha_valoracion, id_usuario_valoracion, id_juego))
                db.commit()
            except Exception as e:
                logging.error("Ocurrió un error al añadir las valoraciones: %s", str(e))
            finally:
                if cursor:
                    cursor.close()
                if db:
                    db.close()

    def actualizar_valoraciones(id_juego):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("UPDATE schema_juegos_docentes.juegos SET puntuacion_media_usuario = ROUND((SELECT AVG(puntuacion) FROM schema_juegos_docentes.valoraciones WHERE id_juego = schema_juegos_docentes.juegos.id), 0)")
            cursor.execute("UPDATE schema_juegos_docentes.juegos SET estrellas_general = CAST(puntuacion_media_usuario AS INTEGER) WHERE id = %s", (id_juego,))
            cursor.execute("UPDATE schema_juegos_docentes.valoraciones SET estrellas_individual = CAST(puntuacion AS INTEGER) WHERE id_juego = %s", (id_juego,))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al actualizar las valoraciones: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def obtener_valoraciones(id_juego):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT v.puntuacion, v.comentario, v.fecha_valoracion, u.usuario, v.estrellas_individual FROM schema_juegos_docentes.valoraciones v INNER JOIN schema_juegos_docentes.usuarios u ON v.id_usuario_valoracion = u.id WHERE v.id_juego = %s", (id_juego,))
            valoraciones = cursor.fetchall()
            return valoraciones
        except Exception as e:
            logging.error("Ocurrió un error al obtener las valoraciones: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
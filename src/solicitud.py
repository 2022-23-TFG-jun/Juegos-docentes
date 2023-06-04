from src.database import conectar
import logging

class Solicitud():
    def rol_profesor(id_usuario_solicitud, fecha_solicitud):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("INSERT INTO schema_juegos_docentes.solicitudes (estado, id_usuario_solicitud, fecha_solicitud) VALUES (%s, %s, %s)", ("PENDIENTE", id_usuario_solicitud, fecha_solicitud))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al añadir una petición de rol de profesor: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def rechazar_solicitud(id_usuario_solicitud):
        try:
            db = conectar()
            cursor = db.cursor()
            # Actualizar el estado de la solicitud a rechazada
            cursor.execute("UPDATE schema_juegos_docentes.solicitudes SET estado=%s WHERE id_usuario_solicitud=%s", ("RECHAZADA", id_usuario_solicitud))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al rechazar una solicitud: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def aceptar_solicitud(id_usuario_solicitud):
        try:
            db = conectar()
            cursor = db.cursor()
            # Actualizar el estado de la solicitud a aceptada
            cursor.execute("UPDATE schema_juegos_docentes.solicitudes SET estado=%s WHERE id_usuario_solicitud=%s", ("ACEPTADA", id_usuario_solicitud))

            # Actualizar rol del usuario a profesor.
            cursor.execute("UPDATE schema_juegos_docentes.usuarios SET rol=%s WHERE id=%s", ("profesor", id_usuario_solicitud))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al aceptar una solicitud: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def obtener_solicitudes():
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM schema_juegos_docentes.solicitudes s INNER JOIN schema_juegos_docentes.usuarios u ON s.id_usuario_solicitud = u.id WHERE u.borrado = 'N' AND s.estado='PENDIENTE' ORDER BY s.id")
            solicitudes = cursor.fetchall()
            return solicitudes
        except Exception as e:
            logging.error("Ocurrió un error al obtener las solicitudes: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def obtener_solicitud_pendiente(id_usuario_solicitud):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM schema_juegos_docentes.solicitudes WHERE id_usuario_solicitud = %s AND estado = 'PENDIENTE'", (id_usuario_solicitud,))
            solicitud = cursor.fetchone()
            return solicitud
        except Exception as e:
            logging.error("Ocurrió un error al obtener las solicitudes pendientes: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
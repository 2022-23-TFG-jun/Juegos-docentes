from src.database import conectar

class Solicitud():
    def __init__(self, id, estado, mensaje_solicitud, id_usuario_solicitud, fecha_solicitud):
        self.id = id
        self.estado = estado
        self.mensaje_solicitud = mensaje_solicitud
        self.id_usuario_solicitud = id_usuario_solicitud
        self.fecha_solicitud = fecha_solicitud
    
    @staticmethod
    def rol_profesor(id_usuario_solicitud, fecha_solicitud):
        # Establecer la conexión a la base de datos
        conn = conectar()

        # Crear un cursor para ejecutar la consulta
        cur = conn.cursor()
        
        # Insertar solicitud
        cur.execute("INSERT INTO schema_juegos_docentes.solicitudes (estado, id_usuario_solicitud, fecha_solicitud) VALUES (%s, %s, %s)", ("PENDIENTE", id_usuario_solicitud, fecha_solicitud))

        conn.commit()

    @staticmethod
    def rechazar_solicitud(id_usuario_solicitud):
        # Establecer la conexión a la base de datos
        conn = conectar()

        # Crear un cursor para ejecutar la consulta
        cur = conn.cursor()
        
        # Actualizar el estado de la solicitud a rechazada
        cur.execute("UPDATE schema_juegos_docentes.solicitudes SET estado=%s WHERE id=%s", ("RECHAZADA", id_usuario_solicitud))

        conn.commit()

    @staticmethod
    def aceptar_solicitud(id_usuario_solicitud):
        # Establecer la conexión a la base de datos
        conn = conectar()

        # Crear un cursor para ejecutar la consulta
        cur = conn.cursor()
        
        # Actualizar el estado de la solicitud a aceptada
        cur.execute("UPDATE schema_juegos_docentes.solicitudes SET estado=%s WHERE id=%s", ("ACEPTADA", id_usuario_solicitud))

        # Actualizar rol del usuario a profesor.
        cur.execute("UPDATE schema_juegos_docentes.usuarios SET rol=%s WHERE id=%s", ("profesor", id_usuario_solicitud))
        
        conn.commit()

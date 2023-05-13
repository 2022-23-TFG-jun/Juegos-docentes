from src.database import conectar

class Juego():
    def __init__(self, id_juego, nombre_juego, descripcion, idiomaN, enlace, puntuacion,
                 disciplina, naturaleza, precio, instrucciones, notas_instructor,
                 objetivos, espacio_control,
                 objetivos_principales, objetivos_secundarios,
                 estructura_sesiones, aspectos_adicionales,
                 entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores,
                youtube_url, fecha_creacion, id_usuario_creacion, fecha_modificacion, id_usuario_modificacion, nombre_archivo):

        self.id_juego = id_juego
        self.nombre_juego = nombre_juego
        self.descripcion = descripcion
        self.idiomaN = idiomaN
        self.enlace = enlace
        self.puntuacion = puntuacion

        self.disciplina = disciplina
        self.naturaleza = naturaleza
        self.precio = precio
        self.instrucciones = instrucciones
        self.notas_instructor = notas_instructor
    
        self.objetivos = objetivos
        self.espacio_control = espacio_control

        self.objetivos_principales = objetivos_principales
        self.objetivos_secundarios = objetivos_secundarios

        self.estructura_sesiones = estructura_sesiones
        self.aspectos_adicionales = aspectos_adicionales

        self.entretenimiento = entretenimiento
        self.aprendizaje = aprendizaje
        self.complejidad_alumno = complejidad_alumno
        self.complejidad_instructores = complejidad_instructores

        self.youtube_url = youtube_url

        self.fecha_creacion = fecha_creacion
        self.id_usuario_creacion = id_usuario_creacion

        self.fecha_modificacion = fecha_modificacion
        self.id_usuario_modificacion = id_usuario_modificacion

        self.nombre_archivo = nombre_archivo

    @staticmethod
    def crear_juego(nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, 
                    instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, 
                    estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, 
                    youtube_url, fecha_creacion, id_usuario_creacion):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("INSERT INTO schema_juegos_docentes.juegos (nombre_juego, descripcion, idioma, enlace, puntuacion, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, youtube_url, fecha_creacion, id_usuario_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, youtube_url, fecha_creacion, id_usuario_creacion))
        db.commit()
    
    @staticmethod
    def añadir_instrucciones(archivo_instrucciones_jugador, id_juego):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("UPDATE schema_juegos_docentes.juegos SET archivo_instrucciones_jugador = %s WHERE id = %s", (archivo_instrucciones_jugador, id_juego))
        db.commit()

    @staticmethod
    def modificar_juego(nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, 
                    instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, 
                    estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, 
                    youtube_url, fecha_modificacion, id_usuario_modificacion, id_juego):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("UPDATE schema_juegos_docentes.juegos SET nombre_juego=%s, descripcion=%s, idioma=%s, enlace=%s, puntuacion=%s, disciplina=%s, naturaleza=%s, precio=%s, instrucciones=%s, notas_instructor=%s, objetivos=%s, espacio_control=%s, objetivos_principales=%s, objetivos_secundarios=%s, estructura_sesiones=%s, aspectos_adicionales=%s, entretenimiento=%s, aprendizaje=%s, complejidad_alumno=%s, complejidad_instructores=%s, youtube_url=%s, fecha_modificacion=%s, id_usuario_modificacion=%s WHERE id=%s", (nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, youtube_url, fecha_modificacion, id_usuario_modificacion, id_juego))
        db.commit()

    @staticmethod
    def eliminar_juego(id_juego):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("DELETE FROM schema_juegos_docentes.juegos WHERE id = %s", (id_juego,))
        db.commit()

    @staticmethod
    def añadir_valoraciones(puntuacion, comentario, fecha_valoracion, id_usuario_valoracion, id_juego):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("INSERT INTO schema_juegos_docentes.valoraciones (puntuacion, comentario, fecha_valoracion, id_usuario_valoracion, id_juego) VALUES (%s, %s, %s, %s, %s)", (puntuacion, comentario, fecha_valoracion, id_usuario_valoracion, id_juego))
        db.commit()

    @staticmethod
    def actualizar_valoraciones(id_juego):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("UPDATE schema_juegos_docentes.juegos SET puntuacion_media_usuario = ROUND((SELECT AVG(puntuacion) FROM schema_juegos_docentes.valoraciones WHERE id_juego = schema_juegos_docentes.juegos.id), 0)")
        cursor.execute("UPDATE schema_juegos_docentes.juegos SET estrellas_general = CAST(puntuacion_media_usuario AS INTEGER) WHERE id = %s", (id_juego))
        cursor.execute("UPDATE schema_juegos_docentes.valoraciones SET estrellas_individual = CAST(puntuacion AS INTEGER) WHERE id_juego = %s", (id_juego))
        db.commit()

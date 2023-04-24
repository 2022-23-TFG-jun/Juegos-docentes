from src.database import conectar

class Juego():
    def __init__(self, id, nombre_juego, descripcion, idioma, enlace, puntuacion, fecha, id_usuario,
                 disciplina, naturaleza, precio, instrucciones, notas_instructor,
                 objetivos, espacio_control,
                 objetivos_principales, objetivos_secundarios,
                 estructura_sesiones, aspectos_adicionales,
                 entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores):

        self.id = id
        self.nombre_juego = nombre_juego
        self.descripcion = descripcion
        self.idioma = idioma
        self.enlace = enlace
        self.puntuacion = puntuacion
        self.fecha = fecha
        self.id_usuario = id_usuario

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
    
    @staticmethod
    def crear_juego(nombre_juego, descripcion, idioma, enlace, puntuacion, fecha, id_usuario, disciplina, naturaleza, precio, 
                    instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, 
                    estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("INSERT INTO schema_juegos_docentes.juegos (nombre_juego, descripcion, idioma, enlace, puntuacion, fecha, id_usuario, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre_juego, descripcion, idioma, enlace, puntuacion, fecha, id_usuario, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores))
        db.commit()

from src.database import conectar

class Valoracion():

    @staticmethod
    def obtener_juegos_valorados(usuario_actual):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT id_juego FROM schema_juegos_docentes.valoraciones WHERE id_usuario_valoracion=%s", (usuario_actual,))
        juegos_valorados_actual = cursor.fetchall()
        cursor.close()
        db.close()
        return juegos_valorados_actual
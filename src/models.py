import psycopg2
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import conectar

class Usuario(UserMixin):
    def __init__(self, id, nombreUsuario, contraseña, rol):
        self.id = id
        self.nombreUsuario = nombreUsuario
        self.contraseña = contraseña
        self.rol = rol

    @staticmethod
    def get(usuario_id):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE id=%s", (usuario_id,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(usuario[0], usuario[1], usuario[2], usuario[3])
        else:
            return None

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE nombreUsuario=%s", (nombreUsuario,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(usuario[0], usuario[1], usuario[2],  usuario[3])
        else:
            return None

    @staticmethod
    def crear(nombreUsuario, contraseña):
        db = conectar()
        cursor = db.cursor()
        password_hash = generate_password_hash(contraseña)
        cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (nombreUsuario, contraseña) VALUES (%s, %s)", (nombreUsuario, password_hash))
        db.commit()

    def comprobar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

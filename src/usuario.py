import psycopg2
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import conectar

class Usuario(UserMixin):
    def __init__(self, id, usuario, nombre, apellido, universidad, edad, genero, contraseña, rol):
        self.id = id
        self.usuario = usuario
        self.nombre = nombre
        self.apellido = apellido
        self.universidad = universidad
        self.edad = edad
        self.genero = genero
        self.contraseña = contraseña
        self.rol = rol

    @staticmethod
    def get(usuario_id):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE id=%s", (usuario_id,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(usuario[0], usuario[1], usuario[2],  usuario[3], usuario[4], usuario[5], usuario[6], usuario[7], usuario[8])
        else:
            return None

    @staticmethod
    def get_by_nombreUsuario(usuario):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE nombreUsuario=%s", (usuario,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(usuario[0], usuario[1], usuario[2],  usuario[3], usuario[4], usuario[5], usuario[6], usuario[7], usuario[8])
        else:
            return None

    @staticmethod
    def crear(usuario, nombre, apellido, universidad, edad, genero, contraseña):
        db = conectar()
        cursor = db.cursor()
        password_hash = generate_password_hash(contraseña)
        cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (usuario, nombre, apellido, universidad, edad, genero, contraseña) VALUES (%s, %s, %s, %s, %s, %s, %s)", (usuario, nombre, apellido, universidad, edad, genero, password_hash,))
        db.commit()

    def comprobar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

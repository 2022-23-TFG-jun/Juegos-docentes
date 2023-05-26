import psycopg2
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from src.database import conectar
import logging

class Usuario(UserMixin):
    def __init__(self, id, usuario, nombre, apellido, institucion, contraseña, rol):
        self.id = id
        self.usuario = usuario
        self.nombre = nombre
        self.apellido = apellido
        self.institucion = institucion
        self.contraseña = contraseña
        self.rol = rol

    def get(usuario_id):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE id=%s", (usuario_id,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(usuario[0], usuario[1], usuario[2],  usuario[3], usuario[4], usuario[5], usuario[6])
        else:
            return None

    """
    def get_by_nombreUsuario(usuario):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE nombreUsuario=%s", (usuario,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(usuario[0], usuario[1], usuario[2],  usuario[3], usuario[4], usuario[5], usuario[6])
        else:
            return None
    """

    def crear(usuario, nombre, apellido, institucion, contraseña):
        try:
            db = conectar()
            cursor = db.cursor()
            password_hash = generate_password_hash(contraseña)
            cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (usuario, nombre, apellido, institucion, contraseña) VALUES (%s, %s, %s, %s, %s)", (usuario, nombre, apellido, institucion, password_hash,))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al crear un usuario: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    """
    def comprobar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)
    """
    def obtener_usuarios():
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT id, usuario, nombre, apellido, institucion, rol FROM schema_juegos_docentes.usuarios WHERE borrado='N'")
            usuarios = cursor.fetchall()
            return usuarios
        except Exception as e:
            logging.error("Ocurrió un error al obtener a los usuarios: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def obtener_usuario_existe(usuario):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE usuario = %s", (usuario,))
            usuario_existe = cursor.fetchone()
            return usuario_existe
        except Exception as e:
            logging.error("Ocurrió un error al obtener al usuario que existe: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def obtener_usuario_db(usuario):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE usuario = %s", (usuario,))
            usuario_db = cursor.fetchone()
            return usuario_db
        except Exception as e:
            logging.error("Ocurrió un error al obtener al usuario: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def eliminar_usuario(id_usuario):
        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute("UPDATE schema_juegos_docentes.usuarios SET borrado='S' WHERE id = %s", (id_usuario,))
            db.commit()
        except Exception as e:
            logging.error("Ocurrió un error al eliminar a un usuario: %s", str(e))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

"""
import psycopg2
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import conectar

class Usuario(UserMixin):
    def __init__(self, id, usuario, nombre, apellido, institucion, contraseña, rol):
        self.id = id
        self.usuario = usuario
        self.nombre = nombre
        self.apellido = apellido
        self.institucion = institucion
        self.contraseña = contraseña
        self.rol = rol

    @staticmethod
    def get(usuario_id):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE id=%s", (usuario_id,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(usuario[0], usuario[1], usuario[2],  usuario[3], usuario[4], usuario[5], usuario[6])
        else:
            return None

    @staticmethod
    def get_by_nombreUsuario(usuario):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE nombreUsuario=%s", (usuario,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(usuario[0], usuario[1], usuario[2],  usuario[3], usuario[4], usuario[5], usuario[6])
        else:
            return None

    @staticmethod
    def crear(usuario, nombre, apellido, institucion, contraseña):
        db = conectar()
        cursor = db.cursor()
        password_hash = generate_password_hash(contraseña)
        cursor.execute("INSERT INTO schema_juegos_docentes.usuarios (usuario, nombre, apellido, institucion, contraseña) VALUES (%s, %s, %s, %s, %s)", (usuario, nombre, apellido, institucion, password_hash,))
        db.commit()

    def comprobar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

    @staticmethod
    def eliminar_usuario(id_usuario):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("DELETE FROM schema_juegos_docentes.usuarios WHERE id = %s", (id_usuario,))
        db.commit()

    @staticmethod
    def obtener_usuarios():
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT id, usuario, nombre, apellido, institucion, rol FROM schema_juegos_docentes.usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        db.close()
        return usuarios
    
    @staticmethod
    def obtener_usuario_existe(usuario):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE usuario = %s", (usuario,))
        usuario_existe = cursor.fetchone()
        cursor.close()
        db.close()
        return usuario_existe
    
    @staticmethod
    def obtener_usuario_db(usuario):
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE usuario = %s", (usuario,))
        usuario_db = cursor.fetchone()
        cursor.close()
        db.close()
        return usuario_db
"""






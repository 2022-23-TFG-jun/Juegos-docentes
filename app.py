import psycopg2
from flask import Flask, request, redirect, render_template, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash
from src.database import conectar, crear_tablas, tabla_usuarios_existe
from src.usuario import Usuario
from src.juego import Juego
from src.busqueda import obtener_resultados_busqueda
from datetime import datetime, timedelta
from unidecode import unidecode
import math

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Configuración de la conexión a la base de datos
with app.app_context():
    if not tabla_usuarios_existe():
        crear_tablas()
    conectar()

app.config['MAX_LOGIN_ATTEMPTS'] = 3 # Número máximo de intentos de login
app.config['LOGIN_BLOCK_DURATION'] = 60  # Bloqueo de 1 minuto
intentos_login = {}  # Diccionario para llevar el registro de intentos de inicio de sesión
usuarios_bloqueados = {} # Diccionario para llevar el registro de usuarios y el tiempo de inicio del bloqueo de cuenta

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_get' # Vista para usuarios no autenticados

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.get(usuario_id)

@app.route('/', methods=['GET'])
def inicio_get():
    return render_template("inicio.html")

#@app.route('/', methods=['POST'])
#def inicio_post():
 #   return render_template("inicio.html")

@app.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('menu_juegos_get'))
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']

    # Si se cumple la sanción de tiempo se desbloquea la cuenta del usuario y tiene un intento más de inicio de sesión
    if usuario in usuarios_bloqueados and usuarios_bloqueados[usuario] < datetime.now():
        intentos_login[usuario] = 2
        del usuarios_bloqueados[usuario]

    # Si un usuario con cuenta bloqueada intenta iniciar sesión se le muestra el tiempo restante del bloqueo
    if usuario in usuarios_bloqueados and usuarios_bloqueados[usuario] > datetime.now():
        time_remaining = (usuarios_bloqueados[usuario] - datetime.now()).seconds
        error = f"Tu cuenta ha sido bloqueada por {time_remaining} segundos."
        return render_template('login.html', error=error)

    # Establecer la conexión a la base de datos
    conn = conectar()

    # Crear un cursor para ejecutar la consulta
    cur = conn.cursor()

    # Consultar un registro que coincida con el nombre del usuario especificado
    cur.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE usuario = %s", (usuario,))
    usuario_db = cur.fetchone()

    # Cerrar el cursor y la conexión a la base de datos
    cur.close()
    conn.close()

    # Verificar si se encontró un usuario y si la contraseña es correcta
    if not usuario_db or not check_password_hash(usuario_db[5], contraseña):
        error = "Nombre de usuario o contraseña incorrectos"

        # Si el login falla, incrementamos el contador de intentos fallidos
        if usuario not in intentos_login:
            intentos_login[usuario] = 0
        intentos_login[usuario] += 1

        # Si se supera el número máximo de intentos fallidos, bloqueamos al usuario
        if intentos_login[usuario] >= app.config['MAX_LOGIN_ATTEMPTS']:
            usuarios_bloqueados[usuario] = datetime.now() + timedelta(seconds=app.config['LOGIN_BLOCK_DURATION'])

        if intentos_login[usuario] > 2:
            error = "Nombre de usuario o contraseña incorrectos. Varios intentos consecutivos fallidos. Cuenta bloqueada durante 60 segundos."
            return render_template('login.html', error=error)
        
        return render_template('login.html', error=error) 

    # Si son correctos, reseteamos el contador de intentos fallidos
    if usuario in intentos_login:
        del intentos_login[usuario]

    # Crear un objeto de usuario a partir de los datos de la base de datos y autenticar al usuario
    usuario = Usuario(usuario_db[0], usuario_db[1], usuario_db[2],  usuario_db[3], usuario_db[4], usuario_db[5], usuario_db[6])    
    login_user(usuario)

    return redirect(url_for('menu_juegos_get'))

@app.route('/registro', methods=['GET'])
def registro_get():
    return render_template("registro.html")

@app.route('/registro', methods=['POST'])
def registro_post():
    # Obtener los datos del formulario
    usuario = request.form['usuario']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    institucion = request.form['institucion']
    contraseña = request.form['contraseña']
    confirmar_contraseña = request.form['confirmar_contraseña']

    # Establecer la conexión a la base de datos
    conn = conectar()

    # Crear un cursor para ejecutar la consulta
    cur = conn.cursor()

    # Consultar si el nombre de usuario ya existe en la tabla de usuarios
    cur.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE usuario = %s", (usuario,))

    # Obtener el resultado de la consulta
    usuario_existe = cur.fetchone()

    # Cerrar el cursor y la conexión a la base de datos
    cur.close()
    conn.close()

    # Si el resultado no es None, significa que el nombre de usuario ya existe
    if usuario_existe is not None:
        error = "El nombre de usuario ya existe"
        return render_template('registro.html', error=error)
    
    # Validar longitud y complejidad de contraseña
    if not (
    any(char.isupper() for char in contraseña) 
    and any(char.isdigit() for char in contraseña) 
    and any(char in "!@#$%^&*()-+?_=,<>/" for char in contraseña) 
    and len(contraseña) >= 8
    ):
        error = "La contraseña debe tener al menos 8 caracteres, un número, una mayúscula y un símbolo"
        return render_template('registro.html', error=error)

    # Comprobar que la contraseña y la confirmación coinciden
    if contraseña != confirmar_contraseña:
        error = "Las contraseñas no coinciden"
        return render_template('registro.html', error=error)

    Usuario.crear(usuario, nombre, apellido, institucion, contraseña)    
    
    # Redirigir a la página de inicio de sesión
    return redirect('/login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('inicio_get'))

@app.route('/menu_juegos', methods=['GET'])
@login_required
def menu_juegos_get():
    
    # Establecer la conexión a la base de datos
    conn = conectar()

    # Crear un cursor para ejecutar la consulta
    cur = conn.cursor()

    # Obtener el número de página actual de la consulta de la cadena de consulta
    pagina_actual = request.args.get('pagina', 1, type=int)

    # Número máximo de juegos por página
    juegos_por_pagina = 4

    # Calcular el número de juegos que se deben omitir antes de devolver el resultado
    desplazamiento = (pagina_actual - 1) * juegos_por_pagina

    # Consultar datos de los juegos
    cur.execute("SELECT id, nombre_juego, descripcion, idioma, enlace, puntuacion FROM schema_juegos_docentes.juegos ORDER BY nombre_juego LIMIT %s OFFSET %s", (juegos_por_pagina, desplazamiento))
    
    # Obtener el resultado de la consulta
    juegos = cur.fetchall()

    # Contar el número total de juegos
    cur.execute("SELECT COUNT(*) FROM schema_juegos_docentes.juegos")
    total_juegos = cur.fetchone()[0]

    # Calcular el número total de páginas
    total_paginas = math.ceil(total_juegos / juegos_por_pagina)

    # Cerrar el cursor y la conexión a la base de datos
    cur.close()
    conn.close()
    
    return render_template('menu_juegos.html', juegos=juegos, pagina_actual=pagina_actual, total_paginas=total_paginas)

@app.route('/menu_juegos', methods=['POST'])
@login_required
def menu_juegos_post():
    busqueda = request.form['busqueda']
    idioma = request.form['idioma']
    puntuacion = request.form['puntuacion']

    if busqueda == "" and idioma == "" and puntuacion == "":
        if(request.args.get('busqueda')):
            busqueda = request.args.get('busqueda')
        if(request.args.get('idioma')):
            idioma = request.args.get('idioma')
        if(request.args.get('puntuacion')):
            puntuacion = request.args.get('puntuacion')

    # Obtener el número de página actual de la consulta de la cadena de consulta
    pagina_actual = request.args.get('pagina', 1, type=int)

    # Número máximo de juegos por página
    juegos_por_pagina = 4

    # Calcular el número de juegos que se deben omitir antes de devolver el resultado
    desplazamiento = (pagina_actual - 1) * juegos_por_pagina

    # Procesar la consulta y obtener los resultados
    resultados_busqueda, total_juegos = obtener_resultados_busqueda(busqueda, idioma, puntuacion, juegos_por_pagina, desplazamiento)

    # Calcular el número total de páginas
    total_paginas = math.ceil(total_juegos / juegos_por_pagina)
    if resultados_busqueda:
        return render_template('menu_juegos.html', resultados_busqueda=resultados_busqueda, pagina_actual=pagina_actual, total_paginas=total_paginas, busqueda=busqueda, idioma=idioma, puntuacion=puntuacion)
    else:
        error = "No se encontraron resultados de la búsqueda"
        return render_template('menu_juegos.html', error=error, pagina_actual=pagina_actual, total_paginas=total_paginas)

@app.route('/añadir_juego', methods=['GET'])
@login_required
def añadir_juego_get():
    return render_template("añadir_juego.html")

@app.route('/añadir_juego', methods=['POST'])
@login_required
def añadir_juego_post():
    # Obtener los datos del formulario
    nombre_juego = request.form['nombre_juego']
    descripcion = request.form['descripcion']
    idioma = request.form['idioma']
    enlace = request.form['enlace']
    puntuacion = request.form['puntuacion']
    fecha = datetime.now()
    id_usuario = current_user.id

    disciplina = request.form['disciplina']
    naturaleza = request.form['naturaleza']
    precio = request.form['precio']
    instrucciones = request.form['instrucciones']
    notas_instructor = request.form['notas_instructor']

    objetivos = request.form['objetivos']
    espacio_control = request.form['espacio_control']

    objetivos_principales = request.form['objetivos_principales']
    objetivos_secundarios = request.form['objetivos_secundarios']

    estructura_sesiones = request.form['estructura_sesiones']
    aspectos_adicionales = request.form['aspectos_adicionales']

    entretenimiento = request.form['entretenimiento']
    aprendizaje = request.form['aprendizaje']
    complejidad_alumno = request.form['complejidad_alumno']
    complejidad_instructores = request.form['complejidad_instructores']
    
    youtube_url = request.form['youtube_url']

    Juego.crear_juego(nombre_juego, descripcion, idioma, enlace, puntuacion, fecha, id_usuario, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, youtube_url)
    
    return redirect('/menu_juegos')

@app.route('/visualizar_juego', methods=['GET'])
@login_required
def visualizar_juego_get():

    id_juego = request.args.get('id')

    # Establecer la conexión a la base de datos
    conn = conectar()

    # Crear un cursor para ejecutar la consulta
    cur = conn.cursor()

    # Consultar datos del juego
    cur.execute("SELECT * FROM schema_juegos_docentes.juegos WHERE id = %s", (id_juego,))
    
    # Obtener el resultado de la consulta
    informacion_juego = cur.fetchone()
    
    # Cerrar el cursor y la conexión a la base de datos
    cur.close()
    conn.close()
    
    return render_template("visualizar_juego.html", informacion_juego=informacion_juego)

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run()


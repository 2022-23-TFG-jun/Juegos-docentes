import psycopg2
from flask import Flask, request, redirect, render_template, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash
from src.database import conectar , crear_tablas  
from src.usuario import Usuario
from src.juego import Juego
from src.solicitud import Solicitud
from src.valoracion import Valoracion
from src.busqueda import obtener_resultados_busqueda
from datetime import datetime, timedelta
#from unidecode import unidecode
import math
from translations.translations import (
    cargar_traducciones_inicio, 
    cargar_traducciones_login, 
    cargar_traducciones_registro, 
    cargar_traducciones_menu_juegos, 
    cargar_traducciones_añadir_juego, 
    cargar_traducciones_visualizar_juego, 
    cargar_traducciones_errores, 
    cargar_traducciones_modificar_juego, 
    cargar_traducciones_administrar_solicitudes, 
    cargar_traducciones_añadir_archivos, 
    cargar_traducciones_administracion, 
    cargar_traducciones_administrar_usuarios, 
    cargar_traducciones_administrar_juegos, 
    cargar_traducciones_contacto,
    cargar_traducciones_visualizar_valoracion,
    cargar_traducciones_añadir_valoracion
)

from flask import session
import os
from werkzeug.utils import secure_filename
from flask import send_file
import logging

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Carpeta para guardar archivos subidos
app.config['UPLOAD_FOLDER'] = './uploads'

"""
# Configuración de la conexión a la base de datos
with app.app_context():
    if not tabla_usuarios_existe():
        crear_tablas()
    conectar()
"""


crear_tablas()

# Configurar el registro de errores
logging.basicConfig(
    filename='errores.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    # Obtener idioma elegido y sus traducciones
    idioma = request.args.get('idioma', 'es')
    traducciones = cargar_traducciones_inicio(idioma)

    return render_template('inicio.html', traducciones=traducciones, idioma=idioma)

@app.route('/login', methods=['GET'])
def login_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_login(idioma)

        if current_user.is_authenticated:
            return redirect(url_for('menu_juegos_get', idioma=idioma))
    
        return render_template('login.html', traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función login_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)

@app.route('/login', methods=['POST'])
def login_post():
    try:
        # Obtener los datos del formulario
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_login(idioma)

        # Si se cumple la sanción de tiempo se desbloquea la cuenta del usuario y tiene un intento más de inicio de sesión
        if usuario in usuarios_bloqueados and usuarios_bloqueados[usuario] < datetime.now():
            intentos_login[usuario] = 2
            del usuarios_bloqueados[usuario]

        # Si un usuario con cuenta bloqueada intenta iniciar sesión se le muestra el tiempo restante del bloqueo
        if usuario in usuarios_bloqueados and usuarios_bloqueados[usuario] > datetime.now():
            time_remaining = (usuarios_bloqueados[usuario] - datetime.now()).seconds
            error_cuenta_bloqueada = f"{time_remaining} s"
            return render_template('login.html', error_cuenta_bloqueada=error_cuenta_bloqueada, idioma=idioma, traducciones=traducciones)

        # Consultar un registro que coincida con el nombre del usuario especificado
        usuario_db = Usuario.obtener_usuario_db(usuario)

        # Verificar si se encontró un usuario y si la contraseña es correcta
        if not usuario_db or not check_password_hash(usuario_db[5], contraseña):
            #Obtener traducciones de errores para el idioma específico
            error_login_incorrecto = cargar_traducciones_errores(idioma)
            
            # Si el login falla, incrementamos el contador de intentos fallidos
            if usuario not in intentos_login:
                intentos_login[usuario] = 0
            intentos_login[usuario] += 1

            # Si se supera el número máximo de intentos fallidos, bloqueamos al usuario
            if intentos_login[usuario] >= app.config['MAX_LOGIN_ATTEMPTS']:
                usuarios_bloqueados[usuario] = datetime.now() + timedelta(seconds=app.config['LOGIN_BLOCK_DURATION'])

            if intentos_login[usuario] > 2:
                #Obtener traducciones de errores para el idioma específico
                error_login_repetido = cargar_traducciones_errores(idioma)
                return render_template('login.html', error_login_repetido=error_login_repetido, idioma=idioma, traducciones=traducciones)
            
            return render_template('login.html', error_login_incorrecto=error_login_incorrecto, idioma=idioma, traducciones=traducciones)

        # Si son correctos, reseteamos el contador de intentos fallidos
        if usuario in intentos_login:
            del intentos_login[usuario]

        # Crear un objeto de usuario a partir de los datos de la base de datos y autenticar al usuario
        usuario = Usuario(usuario_db[0], usuario_db[1], usuario_db[2],  usuario_db[3], usuario_db[4], usuario_db[5], usuario_db[6])    
        login_user(usuario)

        rol_usuario_autenticado = usuario_db[6]

        # Almacenar el rol del usuario autenticado en la sesión
        session['rol_usuario'] = rol_usuario_autenticado

        return redirect(url_for('menu_juegos_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la función login_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)

@app.route('/registro', methods=['GET'])
def registro_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_registro(idioma)
        
        return render_template('registro.html', traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función registro_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)

@app.route('/registro', methods=['POST'])
def registro_post():
    try:
        # Obtener los datos del formulario
        usuario = request.form['usuario']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        institucion = request.form['institucion']
        contraseña = request.form['contraseña']
        confirmar_contraseña = request.form['confirmar_contraseña']

        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_registro(idioma)

        usuario_existe = Usuario.obtener_usuario_existe(usuario)  
    
        # Si el resultado no es None, significa que el nombre de usuario ya existe
        if usuario_existe is not None:
            #Obtener traducciones de errores para el idioma específico
            error_usuario_existe = cargar_traducciones_errores(idioma)
            return render_template('registro.html', error_usuario_existe=error_usuario_existe, idioma=idioma, traducciones=traducciones)
        
        # Validar longitud y complejidad de contraseña
        if not (
        any(char.isupper() for char in contraseña) 
        and any(char.isdigit() for char in contraseña) 
        and any(char in "!@#$%^&*()-+?_=,<>/" for char in contraseña) 
        and len(contraseña) >= 8
        ):
            #Obtener traducciones de errores para el idioma específico
            error_contraseña_condiciones = cargar_traducciones_errores(idioma)
            return render_template('registro.html', error_contraseña_condiciones=error_contraseña_condiciones, idioma=idioma, traducciones=traducciones)

        # Comprobar que la contraseña y la confirmación coinciden
        if contraseña != confirmar_contraseña:
            #Obtener traducciones de errores para el idioma específico
            error_contraseñas_no_coinciden = cargar_traducciones_errores(idioma)
            return render_template('registro.html', error_contraseñas_no_coinciden=error_contraseñas_no_coinciden, idioma=idioma, traducciones=traducciones)
        
        Usuario.crear(usuario, nombre, apellido, institucion, contraseña)    
        
        # Redirigir a la página de inicio de sesión
        return redirect('/login')
    except Exception as e:
        logging.error("Ocurrió un error en la función registro_post: %s", str(e))
        return redirect(url_for('inicio_get'))
    
@app.route('/menu_juegos', methods=['GET'])
@login_required
def menu_juegos_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_menu_juegos(idioma)

        # Obtener el número de página actual de la consulta de la cadena de consulta
        pagina_actual = request.args.get('pagina', 1, type=int)

        # Número máximo de juegos por página
        juegos_por_pagina = 3

        # Calcular el número de juegos que se deben omitir antes de devolver el resultado
        desplazamiento = (pagina_actual - 1) * juegos_por_pagina

        # Consultar id de los usuarios que valoraron un juego
        usuario_actual = current_user.id 
        juegos_valorados_actual = Valoracion.obtener_juegos_valorados(usuario_actual)

        # Consultar datos de los juegos
        juegos = Juego.obtener_juegos_menu(juegos_por_pagina, desplazamiento)

        # Contar el número total de juegos
        total_juegos = Juego.obtener_total_juegos()

        # Calcular el número total de páginas
        total_paginas = math.ceil(total_juegos / juegos_por_pagina)

        # Obtener el rol del usuario autenticado desde la sesión
        rol_usuario_autenticado = session['rol_usuario']

        #Comprueba rol de usuario autenticado para obtener funciones específicas
        if rol_usuario_autenticado == 'usuario':
            return render_template('menu_juegos_usuario.html', juegos=juegos, pagina_actual=pagina_actual, total_paginas=total_paginas, traducciones=traducciones, idioma=idioma, juegos_valorados_actual=juegos_valorados_actual)
        elif rol_usuario_autenticado == 'administrador':
                return render_template('menu_juegos_administrador.html', juegos=juegos, pagina_actual=pagina_actual, total_paginas=total_paginas, traducciones=traducciones, idioma=idioma)
        else:
            return render_template('menu_juegos_profesor.html', juegos=juegos, pagina_actual=pagina_actual, total_paginas=total_paginas, traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función menu_juegos_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
      
@app.route('/menu_juegos', methods=['POST'])
@login_required
def menu_juegos_post():
    try:
        # Obtener los datos del formulario
        busqueda = request.form['busqueda']
        idiomaF = request.form['idiomaF']
        puntuacion = request.form['puntuacion']

        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')

        #Obtener traducciones para el idioma específico
        traducciones = cargar_traducciones_menu_juegos(idioma)

        if busqueda == "" and idiomaF == "" and puntuacion == "":
            if(request.args.get('busqueda')):
                busqueda = request.args.get('busqueda')
            if(request.args.get('idiomaF')):
                idiomaF = request.args.get('idiomaF')
            if(request.args.get('puntuacion')):
                puntuacion = request.args.get('puntuacion')

        # Obtener el número de página actual de la consulta de la cadena de consulta
        pagina_actual = request.args.get('pagina', 1, type=int)

        # Número máximo de juegos por página
        juegos_por_pagina = 3

        # Calcular el número de juegos que se deben omitir antes de devolver el resultado
        desplazamiento = (pagina_actual - 1) * juegos_por_pagina

        # Consultar id de los usuarios que valoraron un juego
        usuario_actual = current_user.id 
        juegos_valorados_actual = Valoracion.obtener_juegos_valorados(usuario_actual)

        # Procesar la consulta y obtener los resultados
        resultados_busqueda, total_juegos = obtener_resultados_busqueda(busqueda, idiomaF, puntuacion, juegos_por_pagina, desplazamiento)

        # Calcular el número total de páginas
        total_paginas = math.ceil(total_juegos / juegos_por_pagina)

        # Obtener el rol del usuario autenticado desde la sesión
        rol_usuario_autenticado = session['rol_usuario']

        if resultados_busqueda:
            #Comprueba rol de usuario autenticado para obtener funciones específicas
            if rol_usuario_autenticado == 'usuario':
                return render_template('menu_juegos_usuario.html', resultados_busqueda=resultados_busqueda, pagina_actual=pagina_actual, total_paginas=total_paginas, busqueda=busqueda, idiomaF=idiomaF, puntuacion=puntuacion, traducciones=traducciones, idioma=idioma, juegos_valorados_actual=juegos_valorados_actual)
            elif rol_usuario_autenticado == 'administrador':
                return render_template('menu_juegos_administrador.html', resultados_busqueda=resultados_busqueda, pagina_actual=pagina_actual, total_paginas=total_paginas, busqueda=busqueda, idiomaF=idiomaF, puntuacion=puntuacion, traducciones=traducciones, idioma=idioma)
            else:
                return render_template('menu_juegos_profesor.html', resultados_busqueda=resultados_busqueda, pagina_actual=pagina_actual, total_paginas=total_paginas, busqueda=busqueda, idiomaF=idiomaF, puntuacion=puntuacion, traducciones=traducciones, idioma=idioma)
        else:
            #Obtener traducciones de errores para el idioma específico
            error_busqueda = cargar_traducciones_errores(idioma)
        
            #Comprueba rol de usuario autenticado para obtener funciones específicas
            if rol_usuario_autenticado == 'usuario':
                return render_template('menu_juegos_usuario.html', error_busqueda=error_busqueda, pagina_actual=pagina_actual, total_paginas=total_paginas, idioma=idioma, traducciones=traducciones)
            elif rol_usuario_autenticado == 'administrador':
                return render_template('menu_juegos_administrador.html', error_busqueda=error_busqueda, pagina_actual=pagina_actual, total_paginas=total_paginas, idioma=idioma, traducciones=traducciones)
            else:
                return render_template('menu_juegos_profesor.html', error_busqueda=error_busqueda, pagina_actual=pagina_actual, total_paginas=total_paginas, idioma=idioma, traducciones=traducciones)
    except Exception as e:
        logging.error("Ocurrió un error en la función menu_juegos_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/añadir_juego', methods=['GET'])
@login_required
def añadir_juego_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_añadir_juego(idioma)

        return render_template('añadir_juego.html', traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función añadir_juego_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma) 
    
@app.route('/añadir_juego', methods=['POST'])
@login_required
def añadir_juego_post():
    try:
        # Obtener los datos del formulario
        nombre_juego = request.form['nombre_juego']
        descripcion = request.form['descripcion']
        idiomaN = request.form['idiomaN']
        enlace = request.form['enlace']
        puntuacion = request.form['puntuacion']

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

        fecha_creacion = datetime.now()
        id_usuario_creacion = current_user.id

        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')

        Juego.crear_juego(nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, youtube_url, fecha_creacion, id_usuario_creacion)

        return redirect(url_for('menu_juegos_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la función añadir_juego_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)

@app.route('/añadir_instrucciones_jugador', methods=['GET'])
def instrucciones_juego_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_añadir_archivos(idioma)

        return render_template('añadir_archivos.html', traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función instrucciones_juego_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)

@app.route('/añadir_instrucciones_jugador', methods=['POST'])
def instrucciones_juego_post():
    try:
        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')

        # Obtener el archivo cargado
        f = request.files['instrucciones_jugador']
        
        # Obtener id del juego elegido
        id_juego = request.args.get('id')
        
        filename = secure_filename(f.filename)

        # Guardar el archivo cargado en la carpeta de carga
        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(ruta_archivo)

        Juego.añadir_instrucciones_jugador(filename, id_juego)

        return redirect(url_for('menu_juegos_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la función instrucciones_juego_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)

@app.route('/añadir_instrucciones_instructor', methods=['POST'])
def instrucciones_instructor_post():
    try:
        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')

        # Obtener el archivo cargado
        f = request.files['instrucciones_instructor']
        
        # Obtener id del juego elegido
        id_juego = request.args.get('id')
        
        filename = secure_filename(f.filename)

        # Guardar el archivo cargado en la carpeta de carga
        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(ruta_archivo)

        Juego.añadir_instrucciones_instructor(filename, id_juego)

        return redirect(url_for('menu_juegos_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la instrucciones_instructor_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)

@app.route('/añadir_archivo_juego', methods=['POST'])
def archivo_juego_post():
    try:
        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')

        # Obtener el archivo cargado
        f = request.files['archivo_juego']
        
        # Obtener id del juego elegido
        id_juego = request.args.get('id')
        
        filename = secure_filename(f.filename)

        # Guardar el archivo cargado en la carpeta de carga
        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(ruta_archivo)

        Juego.añadir_archivo_juego(filename, id_juego)

        return redirect(url_for('menu_juegos_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la función archivo_juego_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)

@app.route('/descargar_instrucciones')
def descargar_instrucciones():
    try:
        filename = request.args.get('filename')
        PATH = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        return send_file(PATH, as_attachment=True)
    except Exception as e:
        logging.error("Ocurrió un error en la función descargar_instrucciones: %s", str(e))
        return redirect(url_for('inicio_get'))

@app.route('/visualizar_juego', methods=['GET'])
@login_required
def visualizar_juego_get():
    try:
        # Obtener id del juego elegido
        id_juego = request.args.get('id')

        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_visualizar_juego(idioma)

        # Obtener el resultado de la consulta
        informacion_juego = Juego.obtener_juego_visualizacion(id_juego)

        return render_template('visualizar_juego.html', informacion_juego=informacion_juego, traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función visualizar_juego_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/modificar_juego', methods=['GET'])
@login_required
def modificar_juego_get():
    try:
        # Obtener id del juego elegido
        id_juego = request.args.get('id')

        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_modificar_juego(idioma)

        # Obtener información del juego a modificar
        informacion_juego = Juego.obtener_juego_modificacion(id_juego)
        
        return render_template('modificar_juego.html', informacion_juego=informacion_juego, traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función modificar_juego_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/modificar_juego', methods=['POST'])
@login_required
def modificar_juego_post():
    try:
        # Obtener los datos del formulario
        nombre_juego = request.form['nombre_juego']
        descripcion = request.form['descripcion']
        idiomaN = request.form['idiomaN']
        enlace = request.form['enlace']
        puntuacion = request.form['puntuacion']

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

        # Obtener id del juego elegido
        id_juego = request.args.get('id')

        fecha_modificacion = datetime.now()
        id_usuario_modificacion = current_user.id

        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')
        
        Juego.modificar_juego(nombre_juego, descripcion, idiomaN, enlace, puntuacion, disciplina, naturaleza, precio, instrucciones, notas_instructor, objetivos, espacio_control, objetivos_principales, objetivos_secundarios, estructura_sesiones, aspectos_adicionales, entretenimiento, aprendizaje, complejidad_alumno, complejidad_instructores, youtube_url, fecha_modificacion, id_usuario_modificacion, id_juego)

        return redirect(url_for('menu_juegos_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la función modificar_juego_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/solicitud_profesor', methods=['GET'])
@login_required
def solicitud_profesor_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_contacto(idioma)

        # Obtener datos del usuario que realiza la solicitud
        id_usuario_solicitud = current_user.id

        # Obtener solicitud pendiente
        solicitud = Solicitud.obtener_solicitud_pendiente(id_usuario_solicitud)

        # Si el usuario no tiene una solicitud pendiente, muestra el botón para la solicitud
        if solicitud is None: 
            return render_template('contacto.html', idioma=idioma, traducciones=traducciones)
        
        # Si el usuario tiene una solicitud pendiente ya no puede solicitar otra vez la solcitud y muestra el mensaje
        mensaje_solicitud = cargar_traducciones_contacto(idioma)
        return render_template('contacto.html', mensaje_solicitud=mensaje_solicitud, idioma=idioma, traducciones=traducciones)
    except Exception as e:
        logging.error("Ocurrió un error en la función solicitud_profesor_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/solicitud_profesor', methods=['POST'])
@login_required
def solicitud_profesor_post():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_contacto(idioma)
        
        # Obtener datos de la fecha-hora y del usuario que realiza la psolicitud
        fecha_solicitud = datetime.now()
        id_usuario_solicitud = current_user.id

        # Crear solicitud
        Solicitud.rol_profesor(id_usuario_solicitud, fecha_solicitud)

        # Mensaje de solicitud exitosa
        mensaje_solicitud = cargar_traducciones_contacto(idioma)
        
        return render_template('contacto.html', mensaje_solicitud=mensaje_solicitud, idioma=idioma, traducciones=traducciones)
    except Exception as e:
        logging.error("Ocurrió un error en la función solicitud_profesor_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/administracion', methods=['GET'])
@login_required
def administracion_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_administracion(idioma)

        return render_template('administracion.html', idioma=idioma, traducciones=traducciones)
    except Exception as e:
        logging.error("Ocurrió un error en la función administracion_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/administrar_solicitudes', methods=['GET'])
@login_required
def administrar_solicitudes_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_administrar_solicitudes(idioma)

        # Consultar solicitudes
        solicitudes = Solicitud.obtener_solicitudes()
        
        return render_template('administrar_solicitudes.html', solicitudes=solicitudes, traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función administrr_solicitudes_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
       
@app.route('/administrar_solicitudes', methods=['POST'])
@login_required
def administrar_solicitudes_post():
    try:
        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')

        # Obtener id del usuario que realizó la solicitud 
        id_usuario_solicitud = request.form['id_usuario_solicitud']

        # Obtener acción que realizó el administrador
        accion = request.form['accion']

        if accion == 'aceptar':
            Solicitud.aceptar_solicitud(id_usuario_solicitud)
        elif accion == 'rechazar':
            Solicitud.rechazar_solicitud(id_usuario_solicitud)
        
        # return render_template('administrar_solicitudes.html') #, traducciones=traducciones, idioma=idioma)
        return redirect(url_for('administrar_solicitudes_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la función administrar_solicitudes_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/administrar_usuarios', methods=['GET'])
@login_required
def administrar_usuarios_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_administrar_usuarios(idioma)
    
        # Obtener usuarios
        usuarios = Usuario.obtener_usuarios()
        
        return render_template('administrar_usuarios.html', usuarios=usuarios, traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función administrar_usuarios_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/administrar_usuarios', methods=['POST'])
@login_required
def administrar_usuarios_post():
    try:
        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')

        # Obtener id del usuario a eliminar
        id_usuario = request.form['id_usuario']

        Usuario.eliminar_usuario(id_usuario)

        return redirect(url_for('administrar_usuarios_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la función administrar_usuarios_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/administrar_juegos', methods=['GET'])
@login_required
def administrar_juegos_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_administrar_juegos(idioma)

        # Obtener juegos
        juegos = Juego.obtener_juegos()
        
        return render_template('administrar_juegos.html', juegos=juegos, traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función administrar_juegos_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)

@app.route('/administrar_juegos', methods=['POST'])
@login_required
def administrar_juegos_post():
    try:
        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')

        # Obtener id del usuario a eliminar
        id_juego = request.form['id_juego']

        Juego.eliminar_juego(id_juego)

        return redirect(url_for('administrar_juegos_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la función administrar_juegos_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/añadir_valoracion', methods=['GET'])
@login_required
def añadir_valoracion_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_añadir_valoracion(idioma)

        return render_template('añadir_valoracion.html', traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función añadir_valoracion_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/añadir_valoracion', methods=['POST'])
@login_required
def añadir_valoracion_post():
    try:
        # Obtener idioma elegido
        idioma = request.args.get('idioma', 'es')

        # Obtener los datos del formulario
        puntuacion = request.form['puntuacion']
        comentario = request.form['comentario']

        # Obtener datos de la fecha-hora y del usuario que realiza la valoración
        fecha_valoracion = datetime.now()
        id_usuario_valoracion = current_user.id

        # Obtener id del juego elegido
        id_juego = request.args.get('id')

        # Agregar la valoración a la base de datos
        Valoracion.añadir_valoraciones(puntuacion, comentario, fecha_valoracion, id_usuario_valoracion, id_juego)

        # Actualizar la puntuación media del juego
        Valoracion.actualizar_valoraciones(id_juego)

        return redirect(url_for('menu_juegos_get', idioma=idioma))
    except Exception as e:
        logging.error("Ocurrió un error en la función añadir_valoracion_post: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/visualizar_valoracion', methods=['GET'])
@login_required
def visualizar_valoracion_get():
    try:
        # Obtener id del juego elegido
        id_juego = request.args.get('id')

        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_visualizar_valoracion(idioma)

        # Obtener valoraciones del juego
        valoraciones = Valoracion.obtener_valoraciones(id_juego)

        return render_template('visualizar_valoracion.html', valoraciones=valoraciones, traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función visualizar_valoracion_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/acerca_de', methods=['GET'])
def acerca_de_get():
    try:
        # Obtener idioma elegido y sus traducciones
        idioma = request.args.get('idioma', 'es')
        traducciones = cargar_traducciones_inicio(idioma)

        return render_template('acerca_de.html', traducciones=traducciones, idioma=idioma)
    except Exception as e:
        logging.error("Ocurrió un error en la función acerca_de_get: %s", str(e))
        return redirect(url_for('inicio_get'), idioma=idioma)
    
@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('inicio_get'))
    except Exception as e:
        logging.error("Ocurrió un error en la función logout: %s", str(e))
        return redirect(url_for('inicio_get'))

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run()


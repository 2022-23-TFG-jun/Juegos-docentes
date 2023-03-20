import psycopg2
from flask import Flask, request, redirect, render_template, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash
from src.database import conectar, crear_tablas, tabla_usuarios_existe
from src.models import Usuario
from datetime import datetime, timedelta

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
def home_get():
    return render_template("home.html")

#@app.route('/', methods=['POST'])
#def home_post():
 #   return render_template("home.html")

@app.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']

    # Si se cumple la sanción de tiempo se desbloquea la cuenta del usuario y tiene un intentos más de inicio de sesión
    if usuario in usuarios_bloqueados and usuarios_bloqueados[usuario] < datetime.now():
        intentos_login[usuario] = 2
        del usuarios_bloqueados[usuario]

    # Si un usuario con cuenta bloqueada intenta iniciar sesión se le muestra el tiempo restante del bloqueo
    if usuario in usuarios_bloqueados and usuarios_bloqueados[usuario] > datetime.now():
        time_remaining = (usuarios_bloqueados[usuario] - datetime.now()).seconds
        error = f"Tu cuenta ha sido bloqueada por {time_remaining} segundos."
        return render_template('login.html', error=error)

    # Abrir la conexión a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="juegos_docentes",
        user="admin",
        password="1234"
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM schema_juegos_docentes.usuarios WHERE usuario = %s", (usuario,))
    usuario_db = cur.fetchone()

    # Cerrar la conexión a la base de datos
    cur.close()
    conn.close()

    # Verificar si se encontró un usuario y si la contraseña es correcta
    if not usuario_db or not check_password_hash(usuario_db[2], contraseña):
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
    usuario = Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3])    
    login_user(usuario)

    return redirect(url_for('inicio'))

@app.route('/registro', methods=['GET'])
def registro_get():
    return render_template("registro.html")




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_get'))

# Definir una ruta para la página de éxito
@app.route('/inicio')
@login_required
def inicio():
    return render_template('inicio.html')

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run()




"""
import psycopg2 
from flask import Flask, request, redirect, render_template, url_for
from src.database import conectar, crear_tablas

app = Flask(__name__)

# Llamada a la función create_tables en la inicialización de la aplicación
with app.app_context():
    crear_tablas()

@app.route('/', methods=['GET'])
def home():
    return "hola mundo"
    #return render_template("inicio.html")

@app.route('/login', methods=['GET'])
def login_get():
    return render_template("login.html")

def validar_credenciales(usuario, contraseña):
    conn = psycopg2.connect("dbname=juegos_docentes user=admin password=1234")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM schema_juegos_docentes.usuarios WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] == 1

def contar_usuarios():
    conn = psycopg2.connect("dbname=juegos_docentes user=admin password=1234")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM schema_juegos_docentes.usuarios;")
    num_usuarios = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(f"Hay {num_usuarios} usuarios en la tabla.")
    return "Conteo de usuarios completado."

@app.route('/login', methods=['POST'])
def login_post():
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']
    contar_usuarios()
    if validar_credenciales(usuario, contraseña):
        # Inicio de sesión correcto, redirigir al usuario a una página de éxito
        return redirect(url_for('inicio'))
    else:
        # Usuario o contraseña incorrectos, mostrar un mensaje de error
        error = "Usuario o contraseña incorrectos"
        return render_template('login.html', error=error)

# Definir una ruta para la página de éxito
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run()

"""
from flask import Flask, jsonify, request, render_template, flash
from requests import status_codes
import requests
import json
import random
from requests.sessions import Request

app = Flask(__name__)

app.config['SECRET_KEY'] = 'qoNhFeWiVWO4u602pAIb'

# Pagina index


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Pagina de login a la plataforma de administracion de restaurantes


@app.route('/login-restaurante', methods=['GET', 'POST'])
def login_restaurante():
    return render_template('login-restaurante.html')

# Pagina donde se buscan las cartas por ID de restaurante


@app.route('/buscar-restaurante', methods=['GET', 'POST'])
def buscar_restaurante():
    return render_template('buscar-restaurante.html')

# Pagina para crear nuevas cuentas de restaurantes


@app.route('/crear-cuenta', methods=['GET', 'POST'])
def crear_cuenta():
    if (request.method == 'GET'):
        return render_template('crear-cuenta.html')
    elif(request.method == 'POST'):
        try:
            id_restaurante = random.randint(10000, 99999)
            restaurante = {
                "id_restaurante":id_restaurante,
                "nombre_restaurante": request.form['nombre-restaurante'],
                "especialidad": request.form['especialidad'],
                "chef": request.form['chef'],
                "color": request.form['colores'],
                "logo": request.form['logo']
            }
            usuario = {
                "id_restaurante": id_restaurante,
                "password": request.form['contraseña']
            }
            request_microservicio_usuarios = requests.post(
                'http://localhost:7071/api/HttpTrigger1', json=usuario)
            request_microservicio_restaurante = requests.post('http://localhost:7070/api/HttpTrigger1', json=restaurante)
            if (request_microservicio_usuarios.status_code == 200
                    and request_microservicio_restaurante.status_code == 200):
                flash(f'Cuenta creada con exito. Su ID de restaurante es {id_restaurante}, guardelo.')
                context = {'status_code':200}
                return render_template('crear-cuenta.html', **context)
            else:
                flash(f'Lo sentimos algo fallo, vuelvelo a intentar')
                context = {'status_code':500}
                return render_template('crear-cuenta.html', **context)
        except Exception as e:
            flash(f'Lo sentimos algo fallo, vuelvelo a intentar')
            context = {'status_code':500}
            return render_template('crear-cuenta.html', **context)


# Pagina inicio de administracion de los restaurantes

@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    return render_template('admin-page.html')

# Pagina inicio de administracion de los restaurantes


@app.route('/cambiar-informacion', methods=['GET', 'POST'])
def cambiar_informacion():
    if (request.method == 'GET'):
        data = {
            "id": 13456,
            "nombre_restaurante": "El Baluarte",
            "Color": "#FFC300",
            "logo": "https://baluartesfj.com/wp-content/uploads/2018/05/logo_home_2.png",
            "chef_principal": "Maria Fernandez",
            "especialidad": "Comida Caribeña"
        }
        context = {'restaurante': data}
        return render_template('cambiar-informacion-restaurante.html', **context)

# Pagina de administracion de los platos y la carta


@app.route('/administrar-carta', methods=['GET', 'POST'])
def administrar_carta():
    return render_template('administrar-carta.html')

# Pagina de cambio de contraseña


@app.route('/cambiar-contraseña', methods=['GET', 'POST'])
def cambiar_password():
    return render_template('cambiar-password.html')

# Configuraciones basicas


if __name__ == '__main__':
    app.run(debug=True, port=4000)

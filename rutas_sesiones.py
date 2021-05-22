from flask import Blueprint, render_template, request, flash
import requests
import random

rutas_sesiones = Blueprint('rutas_sesiones', __name__, template_folder='templates', static_folder='static')


# Pagina de login a la plataforma de administracion de restaurantes

@rutas_sesiones.route('/login-restaurante', methods=['GET', 'POST'])
def login_restaurante():
    return render_template('login-restaurante.html')

# Pagina para crear nuevas cuentas de restaurantes

@rutas_sesiones.route('/crear-cuenta', methods=['GET', 'POST'])
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
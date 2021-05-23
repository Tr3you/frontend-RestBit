from flask import Blueprint, render_template, request, flash, redirect, sessions, url_for, session
import requests
import random

rutas_sesiones = Blueprint('rutas_sesiones', __name__,
                           template_folder='templates', static_folder='static')

# Pagina de login a la plataforma de administracion de restaurantes


@rutas_sesiones.route('/login-restaurante', methods=['GET', 'POST'])
def login_restaurante():
    if not 'user_logged' in session:
        if (request.method == 'GET'):
            return render_template('login-restaurante.html')
        elif(request.method == 'POST'):
            try:
                id_restaurante = request.form['id-restaurante']
                user = {
                    'id_restaurante': id_restaurante,
                    'password': request.form['contraseña']
                }
                request_microservicio_usuarios = requests.get(
                    'https://microservicio-usuarios.azurewebsites.net/api/httptrigger2', json=user)
                if (request_microservicio_usuarios.status_code == 200):
                    session['user_logged'] = id_restaurante
                    return redirect(url_for('rutas_restaurante.admin_page'))
                else:
                    flash(f'Usuario o contraseña incorrecta, vuelvalo a intentar')
                    context = {'status_code': 500}
                    return render_template('login-restaurante.html', **context)
            except Exception as e:
                flash(f'Lo sentimos algo fallo, vuelvelo a intentar')
                context = {'status_code': 500}
                return render_template('login-restaurante.html', **context)
    return redirect(url_for('rutas_restaurante.admin_page'))


# Boton loggout

@rutas_sesiones.route('/logout', methods=['GET', 'POST'])
def loggout():
    session.pop('user_logged', None)
    return redirect(url_for('rutas_sesiones.login_restaurante'))


# Pagina para crear nuevas cuentas de restaurantes

@rutas_sesiones.route('/crear-cuenta', methods=['GET', 'POST'])
def crear_cuenta():
    if (request.method == 'GET'):
        return render_template('crear-cuenta.html')
    elif(request.method == 'POST'):
        try:
            id_restaurante = random.randint(10000, 99999)
            restaurante = {
                "id_restaurante": id_restaurante,
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
                'https://microservicio-usuarios.azurewebsites.net/api/httptrigger1', json=usuario)
            request_microservicio_restaurante = requests.post(
                'https://microservicio-restaurante.azurewebsites.net/api/httptrigger1', json=restaurante)
            if (request_microservicio_usuarios.status_code == 200
                    and request_microservicio_restaurante.status_code == 200):
                flash(
                    f'Cuenta creada con exito. Su ID de restaurante es {id_restaurante}, guardelo.')
                context = {'status_code': 200}
                return render_template('crear-cuenta.html', **context)
            else:
                flash(f'Lo sentimos algo fallo, vuelvelo a intentar')
                context = {'status_code': 500}
                return render_template('crear-cuenta.html', **context)
        except Exception as e:
            flash(f'Lo sentimos algo fallo, vuelvelo a intentar')
            context = {'status_code': 500}
            return render_template('crear-cuenta.html', **context)

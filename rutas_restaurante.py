from flask import Blueprint, render_template, request, session, sessions, redirect, url_for
from flask.helpers import flash
import requests
import json


rutas_restaurante = Blueprint('rutas_restaurante', __name__, template_folder='templates', static_folder='static')


# Pagina inicio de administracion de los restaurantes

@rutas_restaurante.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if 'user_logged' in session:
        return render_template('admin-page.html')
    return redirect (url_for('rutas_sesiones.login_restaurante'))


# Pagina inicio de administracion de los restaurantes

@rutas_restaurante.route('/cambiar-informacion', methods=['GET', 'POST'])
def cambiar_informacion():
    if 'user_logged' in session:
        if (request.method == 'GET'):
            restaurante = {'id_restaurante': session['user_logged']}
            request_microservicio_restaurante = requests.get('http://localhost:7070/api/HttpTrigger3', json=restaurante)
            context = {'restaurante': json.loads(request_microservicio_restaurante.text)}
            return render_template('cambiar-informacion-restaurante.html', **context)
        if (request.method == 'POST'):
            try:
                restaurante ={
                "id_restaurante": session['user_logged'],
                "nombre_restaurante": request.form['nombre-restaurante'],
                "color": request.form['colores'],
                "logo": request.form['logo'],
                "chef_principal": request.form['chef'],
                "especialidad": request.form['especialidad']
                }
                request_microservicio_restaurante = requests.put('http://localhost:7070/api/HttpTrigger2', json=restaurante)
                if(request_microservicio_restaurante.status_code==200):
                    flash('Informacion actualizada con exito')
                    context = {'status_code': 200}
                    return redirect(url_for('rutas_restaurante.cambiar_informacion'))
                else:
                    flash('Algo salio mal o los datos no estan completos, vuelva a intentarlo')
                    context = {'status_code': 500}
                    return redirect(url_for('rutas_restaurante.cambiar_informacion'))
            except:
                flash('Algo salio mal, vuelvalo a intentar')
                context = {'status_code': 500}
                return render_template('cambiar-informacion-restaurante.html', **context)
    return redirect (url_for('rutas_sesiones.login_restaurante'))


# Pagina de administracion de los platos y la carta

@rutas_restaurante.route('/administrar-carta', methods=['GET', 'POST'])
def administrar_carta():
    if 'user_logged' in session:
        return render_template('administrar-carta.html')
    return redirect (url_for('rutas_sesiones.login_restaurante'))


# Pagina de cambio de contraseña

@rutas_restaurante.route('/cambiar-contraseña', methods=['GET', 'POST'])
def cambiar_password():
    if 'user_logged' in session:
        if(request.method=='GET'):
            return render_template('cambiar-password.html')
        elif(request.method=='POST'):
            try:
                change_password = {
                    'old_password': request.form['password1'],
                    'new_password': request.form['password2'],
                    'id_restaurante': session['user_logged']
                }
                request_microservicio_usuarios = requests.put('http://localhost:7071/api/HttpTrigger3', json=change_password)
                if(request_microservicio_usuarios.status_code==200):
                    flash('Su contraseña a sido actualizada exitosamente')
                    context = {'status_code': 200}
                    return render_template('cambiar-password.html', **context)
                else:
                    flash('Algo salio mal o las contraseñas no coinciden, vuelvalo a intentar')
                    context = {'status_code': 500}
                    return render_template('cambiar-password.html', **context)
            except:
                flash('Algo salio mal o las contraseñas no coinciden, vuelvalo a intentar')
                context = {'status_code': 500}
                return render_template('cambiar-password.html', **context)

    return redirect (url_for('rutas_sesiones.login_restaurante'))
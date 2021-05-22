from flask import Blueprint, render_template, request

rutas_restaurante = Blueprint('rutas_restaurante', __name__, template_folder='templates', static_folder='static')


# Pagina inicio de administracion de los restaurantes

@rutas_restaurante.route('/admin', methods=['GET', 'POST'])
def admin_page():
    return render_template('admin-page.html')


# Pagina inicio de administracion de los restaurantes

@rutas_restaurante.route('/cambiar-informacion', methods=['GET', 'POST'])
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

@rutas_restaurante.route('/administrar-carta', methods=['GET', 'POST'])
def administrar_carta():
    return render_template('administrar-carta.html')


# Pagina de cambio de contraseña

@rutas_restaurante.route('/cambiar-contraseña', methods=['GET', 'POST'])
def cambiar_password():
    return render_template('cambiar-password.html')
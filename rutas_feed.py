from flask import Blueprint, render_template, request, flash, redirect,  url_for, session
import requests
import json

rutas_feed = Blueprint('rutas_feed', __name__,
                           template_folder='templates', static_folder='static')

# Pagina donde se buscan las cartas por ID de restaurante

@rutas_feed.route('/buscar-restaurante', methods=['GET', 'POST'])
def buscar_restaurante():
        return render_template('buscar-restaurante.html')

@rutas_feed.route('/feed_restaurante', methods=['GET', 'POST'])
def feed_restaurante():
    if(request.method=='GET'):
        return redirect(url_for('rutas_feed.buscar_restaurante'))
    elif(request.method=='POST'):
        try:
            id_restaurante = request.form['id-restaurante']
            numero_mesa = request.form['numero-mesa']
            restaurante = {'id_restaurante': id_restaurante}
            request_microservicio_restaurante = requests.get('https://microservicio-restaurante.azurewebsites.net/api/httptrigger3', json=restaurante)
            context = {'restaurante': json.loads(request_microservicio_restaurante.text)}
            return render_template('feed-restaurante.html', **context)
        except:
            flash('El ID ingresado no corresponde con ningun restaurante o algo salio mal, vuelvalo a intentar')
            return redirect(url_for('rutas_feed.buscar_restaurante'))

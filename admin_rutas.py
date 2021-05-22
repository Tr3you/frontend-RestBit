from flask import Flask, render_template
from rutas_restaurante import rutas_restaurante
from rutas_sesiones import rutas_sesiones

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qoNhFeWiVWO4u602pAIb'
app.register_blueprint(rutas_sesiones)
app.register_blueprint(rutas_restaurante)

# Pagina index

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Pagina donde se buscan las cartas por ID de restaurante

@app.route('/buscar-restaurante', methods=['GET', 'POST'])
def buscar_restaurante():
    return render_template('buscar-restaurante.html')


# Configuraciones basicas

if __name__ == '__main__':
    app.run(debug=True, port=4000)

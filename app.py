import requests
from flask import Flask, render_template

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Definición de las rutas
@app.route('/', methods=['GET'])
def index():
    # Realizar una solicitud GET a la ruta de la API que devuelve los productos
    response = requests.get('http://localhost:5000/tools')
    
    # Extraer los datos JSON de la respuesta
    products = response.json()
    
    # Pasar los productos a la plantilla HTML y renderizarla
    return render_template('catalogo.html', products=products)

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    # Ejecutar la aplicación Flask en modo de depuración en la dirección 0.0.0.0 y el puerto 8080
    app.run(host='0.0.0.0', port=8080, debug=True)

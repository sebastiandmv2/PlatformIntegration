import requests
from flask import Flask, render_template, request, jsonify

# Lista para almacenar los productos en el carrito
carrito = []

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Definición de las rutas
@app.route('/', methods=['GET'])

def catalogo():
    # Realizar una solicitud GET a la ruta de la API que devuelve los productos
    response = requests.get('http://localhost:5000/tools')
    
    # Extraer los datos JSON de la respuesta
    products = response.json()
    
    # Pasar los productos a la plantilla HTML y renderizarla
    return render_template('catalogo.html', products=products)

@app.route('/carrito', methods=['GET'])
def mostrar_carrito():
    return render_template('carrito.html', products=carrito)



@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Obtain product id and quantity from the request
    data = request.get_json()
    product_id = data['productId']
    quantity = data['quantity']

    # Fetch product details using the product_id from your API
    response = requests.get(f'http://localhost:5000/tools/{product_id}')
    product = response.json()

    # Add the product to the cart with quantity
    cart_item = {'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': quantity}
    carrito.append(cart_item)

    return jsonify({'message': 'Producto agregado al carrito', 'product': cart_item})

    
# Ejecutar la aplicación Flask
if __name__ == '__main__':
    # Ejecutar la aplicación Flask en modo de depuración en la dirección 0.0.0.0 y el puerto 8080
    app.run(host='0.0.0.0', port=8080, debug=True)

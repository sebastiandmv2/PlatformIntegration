import requests
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta



# Lista para almacenar los productos en el carrito
carrito = []

# Inicialización de la aplicación Flask
app = Flask(__name__)


# Establece la clave secreta de la aplicación
app.config['SECRET_KEY'] = os.urandom(32)

def obtener_valor_dolar(usuario, contrasena, serie):
    # URL de la API
    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    
    # Parámetros de la solicitud
    params = {
        "user": usuario,
        "pass": contrasena,
        "function": "GetSeries",
        "timeseries": serie
    }
    
    # Realizar la solicitud GET
    response = requests.get(url, params=params)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()
        
        # Obtener la fecha de ayer en formato DD-MM-YYYY
        fecha_ayer = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')
        
        # Filtrar los resultados para encontrar la entrada correspondiente a la fecha de ayer
        for item in data['Series']['Obs']:
            if item['indexDateString'] == fecha_ayer:
                # Devolver el valor del dólar para ayer
                return item['value']
        
        # Si no se encuentra ninguna entrada para la fecha de ayer, imprimir un mensaje de error
        print("No se encontraron datos para la fecha de ayer.")
        return None
        
    else:
        print("Error en la solicitud:", response.status_code)
        return None







# Definición de las rutas
@app.route('/', methods=['GET'])
def catalogo():
    # Realizar una solicitud GET a la ruta de la API que devuelve los productos
    response = requests.get('http://localhost:5000/tools')

    # Extraer los datos JSON de la respuesta
    products = response.json()

    valor_dolar_ayer = obtener_valor_dolar("ast.gonzalez@duocuc.cl", "V25713451.2", "F073.TCO.PRE.Z.D")

    # Calcular el precio de cada producto en dólares
    for product in products:
        product['price_usd'] = round(float(product['price']) / float(valor_dolar_ayer), 2)


    # Pasar los productos a la plantilla HTML y renderizarla
    return render_template('catalogo.html', products=products, valor_dolar=valor_dolar_ayer)

@app.route('/carrito', methods=['GET'])
def mostrar_carrito():
    # Define la función calcular_total dentro de la ruta
    def calcular_total(carrito):
        total = 0
        for product in carrito:
            try:
                total += float(product['price']) * int(product['quantity'])
            except (ValueError, TypeError):
                print("Error: Los valores de precio y cantidad deben ser números.")
        return total

    total_clp = calcular_total(carrito)  # Llama a la función calcular_total y pasa el carrito como argumento
    
    # Obtener el valor del dólar dentro de la función mostrar_carrito()
    valor_dolar_ayer = obtener_valor_dolar("ast.gonzalez@duocuc.cl", "V25713451.2", "F073.TCO.PRE.Z.D")

    # Calcular price_usd para cada producto en el carrito
    for product in carrito:
        response = requests.get(f'http://localhost:5000/tools/{product["id"]}')
        product_details = response.json()
        product['price_usd'] = round(float(product_details['price']) / float(valor_dolar_ayer), 2)

    # Calcular el total del carrito en USD
    total_usd = sum(product['price_usd'] * int(product['quantity']) for product in carrito)

    return render_template('carrito.html', products=carrito, total_clp=total_clp, total_usd=total_usd)


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


#actualizar carrito

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    # Obtén el ID del producto y la nueva cantidad desde la solicitud JSON
    data = request.get_json()
    product_id = data['productId']
    new_quantity = data['quantity']

    # Encuentra el producto en el carrito por su ID y actualiza la cantidad
    for item in carrito:
        if item['id'] == product_id:
            item['quantity'] = new_quantity
            break

    # Devuelve una respuesta exitosa
    return jsonify({'message': 'Cantidad del producto actualizada exitosamente en el carrito'})


#eliminar producto
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Obtener el ID del producto a eliminar del cuerpo de la solicitud
    data = request.get_json()
    product_id = data['productId']

    # Iterar sobre los productos en el carrito y eliminar el que coincida con el ID proporcionado
    for product in carrito:
        if product['id'] == product_id:
            carrito.remove(product)
            return jsonify({'message': 'Producto eliminado del carrito', 'product': product})

    # Si no se encuentra el producto en el carrito, devolver un mensaje de error
    return jsonify({'error': 'Producto no encontrado en el carrito'}), 404

## Login Routes

# Función para manejar el login en la aplicación principal
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hace una solicitud a la API para autenticar al usuario
        response = requests.post('http://localhost:5000/api/login', json={'username': username, 'password': password})
        
        if response.status_code == 200:
            # Genera la sesión del usuario si la autenticación es exitosa
            session['username'] = username
            return redirect(url_for('catalogo'))  # Redirecciona al usuario a la página principal
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')  # Renderiza el formulario de inicio de sesión

@app.route('/logout')
def logout():
    # Elimina el nombre de usuario de la sesión si está presente
    session.pop('username', None)
    # Redirecciona al usuario a la página de inicio después de cerrar sesión
    return redirect(url_for('catalogo'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Hacer una solicitud a la API para crear un nuevo usuario
        response = requests.post('http://localhost:5000/api/register', json={'username': username, 'password': password, 'email': email})
        
        if response.status_code == 201:
            # Si el usuario se crea con éxito, redirigir a la página de inicio de sesión
            return redirect(url_for('login'))
        else:
            # Si hay un error al crear el usuario, mostrar un mensaje de error
            return render_template('register.html', message='Error al registrar el usuario')

    # Si es un método GET, simplemente renderiza el formulario de registro
    return render_template('register.html')

## Profile Routes

# Ruta para ver el perfil del usuario
@app.route('/profile/<username>', methods=['GET'])
def user_profile(username):
    # Realizar una solicitud a la API para obtener la información del usuario
    response = requests.get(f'http://localhost:5000/api/profile?username={username}')

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        user_info = response.json()
        return render_template('profile.html', user=user_info)
    else:
        message = response.json().get('message', 'Error al obtener información del usuario')
        return render_template('profile.html', message=message)

@app.route('/edit_profile')
def edit_user_profile():
    message = request.args.get('message')
    return render_template('edit_profile.html', message=message)

# Ruta para modificar el correo electrónico del usuario en la API
@app.route('/modify_email', methods=['POST'])
def modify_email():
    # Obtener los datos del formulario
    username = session['username']
    new_email = request.form['new_email']

    # Realizar la solicitud a la API para modificar el correo electrónico
    response = requests.put('http://localhost:5000/api/profile/email', json={'username': username, 'new_email': new_email})

    # Capturar el mensaje de respuesta de la API
    if response.status_code == 200:
        message = response.json().get('message', 'Correo electrónico modificado exitosamente')
    else:
        message = response.json().get('message', 'Error al modificar el correo electrónico')
    
    # Redirigir a la página del perfil del usuario con el mensaje de la API
    return redirect(url_for('edit_user_profile', message=message))

# Ruta para modificar la contraseña del usuario en la API
@app.route('/modify_password', methods=['POST'])
def modify_password():
    # Obtener los datos del formulario
    username = session['username']
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    # Realizar la solicitud a la API para modificar la contraseña
    response = requests.put('http://localhost:5000/api/profile/password', json={'username': username, 'current_password': current_password, 'new_password': new_password, 'confirm_password': confirm_password})

    if response.status_code == 200:
        message = 'Contraseña modificada exitosamente'
    else:
        message = response.json()['message']
    return redirect(url_for('edit_user_profile', message=message))
 
# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


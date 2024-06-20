import requests
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from utils import *

import stripe

# Configura tus claves de prueba de Stripe
stripe.api_key = "sk_test_51PIEHJFngB2pMcgsTQQWyq4VWfSKzxgXHJHKjPGQiLehQyZ7EaPrHQqTBEFMjFpPcxn76UR5HRNeHwtAedsBDwKM00LGzeSh7D"


# Lista para almacenar los productos en el carrito
carrito = []

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Establece la clave secreta de la aplicación
app.config['SECRET_KEY'] = 'a9a0f946b0e54dff85d1b7484c31b7d0'



@app.route('/', methods=['GET'])
def catalogo():
    tools_type_id = request.args.get('tools_type_id')
    url = 'http://localhost:5000/tools'
    
    if tools_type_id:
        url += f'?tools_type_id={tools_type_id}'
    
    # Realizar una solicitud GET a la ruta de la API que devuelve los productos
    response = requests.get(url)

    # Extraer los datos JSON de la respuesta
    products = response.json()

    valor_dolar_ayer = obtener_valor_dolar("ast.gonzalez@duocuc.cl", "V25713451.2")

    # Calcular el precio de cada producto en dólares
    for product in products:
        product['price_usd'] = round(float(product['price']) / float(valor_dolar_ayer), 2)

    # Pasar los productos a la plantilla HTML y renderizarla
    return render_template('catalogo.html', products=products, valor_dolar=valor_dolar_ayer)

##Mostrar las categorias

@app.route('/categorias', methods=['GET'])
def show_categorias():
    response = requests.get('http://localhost:5000/tools_types')
    tools_types = response.json()
    return render_template('categorias.html', tools_types=tools_types)

# Función para obtener métodos de pago
def obtener_metodos_pago():
    response = requests.get('http://localhost:5000/api/pago')
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Función para obtener métodos de envío
def obtener_metodos_envio():
    response = requests.get('http://localhost:5000/api/shipping')
    if response.status_code == 200:
        return response.json()
    else:
        return []



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
    
    # Obtener métodos de pago y envío
    metodos_pago = obtener_metodos_pago()
    metodos_envio = obtener_metodos_envio()    
    
    # Obtener el valor del dólar dentro de la función mostrar_carrito()
    valor_dolar_ayer = obtener_valor_dolar("ast.gonzalez@duocuc.cl", "V25713451.2")

    # Calcular price_usd para cada producto en el carrito
    for product in carrito:
        response = requests.get(f'http://localhost:5000/tools/{product["id"]}')
        product_details = response.json()
        product['price_usd'] = round(float(product_details['price']) / float(valor_dolar_ayer), 2)

    # Calcular el total del carrito en USD
    total_usd = sum(product['price_usd'] * int(product['quantity']) for product in carrito)

    # Verificar si hay un usuario en la sesión
    if 'username' in session:
        username = session['username']
        # Traer informacion de Subcripción del Usuario
        response = requests.get(f'http://localhost:5000/api/profile?username={username}')
        if response.status_code == 200:
            # La solicitud fue exitosa, obtenemos el estado de suscripción del usuario
            user_info = response.json()
            subscribed_value = user_info.get('subscribed')
            subscribed = True if subscribed_value == 1 else False
        else:
        # Si la solicitud no fue exitosa, asignamos False a subscribed
            subscribed = False
    else:
        username = None
        subscribed = False  # Manejar el caso donde no hay usuario

    # Calcular los precios con descuento si el usuario está suscrito
    if subscribed:
        total_clp_con_descuento = total_clp * 0.9
        total_usd_con_descuento = total_usd * 0.9
    else:
        total_clp_con_descuento = total_clp
        total_usd_con_descuento = total_usd
    
    # Agregar Variables a la sesion
    session['total_clp_con_descuento'] = total_clp_con_descuento

    return render_template('carrito.html', products=carrito, total_clp=total_clp, total_usd=total_usd,
                           total_clp_con_descuento=total_clp_con_descuento, total_usd_con_descuento=total_usd_con_descuento,
                           subscribed=subscribed,payment_methods=metodos_pago, shipping_methods=metodos_envio)

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

## PLATAFORMA DE PAGO

@app.route('/success')
def success():
    total_clp_con_descuento = session.pop('total_clp_con_descuento', None)
    if total_clp_con_descuento is None:
        total_clp_con_descuento = sum([producto['subtotal'] for producto in carrito])
        return redirect(url_for('error', message='No se encontró el total con descuento en la sesión'))

    # Calcular el subtotal para cada producto en el carrito
    for product in carrito:
        product['subtotal'] = float(product['price']) * int(product['quantity'])

    for producto in carrito:
        id_producto = producto['id']
        quantity_producto = producto['quantity']

        response = requests.put('http://localhost:5000/api/update_stock', json={'id': id_producto, 'new_stock': quantity_producto})

        if response.status_code == 201:
            message = response.json().get('message', 'Stock actualizado exitosamente')  # Obtener el mensaje si existe, de lo contrario, usar uno predeterminado
        else:
            message = 'Error al actualizar el stock del producto: {}'.format(response.text)  # Utilizar el contenido de la respuesta como mensaje de error

            return redirect(url_for('error', message=message))
        
        
    # Obtener los métodos de envío y pago seleccionados del formulario en carrito.html
    selectedShippingMethod = request.form.get('shipping-method')
    selectedPaymentMethod = request.form.get('payment-method')


    # Crear la nueva orden
    order_data = {
        'id_users': session.get('user_id'),  # Suponiendo que guardas el ID de usuario en la sesión
        'orders_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Fecha y hora actual
        'Total': total_clp_con_descuento,  # Total con descuento
        'cantidad_productos': sum([producto['quantity'] for producto in carrito]),  # Cantidad total de productos en el carrito
        'status': 'completado',  # Estado inicial de la orden
        'id_shipping_detail': selectedShippingMethod,  # Método de envío seleccionado
        'id_pago': selectedPaymentMethod,  # Método de pago seleccionado
        'order_details': [{'id_tools': producto['id'], 'cantidad': producto['quantity'], 'subtotal': producto['subtotal']} for producto in carrito]  # Detalles de los productos en el carrito
    }

    response = requests.post('http://localhost:5000/api/orders', json=order_data)

    if response.status_code == 201:
        order_id = response.json().get('order_id')
        carrito.clear()  # Vaciar el carrito solo si la orden se crea correctamente
        return render_template('success.html', order_id=order_id)
    else:
        message = 'Error al crear la orden: {}'.format(response.text)
        return redirect(url_for('error', message=message))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        total_payment = session.get('total_clp_con_descuento', None)
        if total_payment is not None:
            total_payment = int(total_payment)  # Convertir a entero

        user = session.get('username', None)

        stripe_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'clp',
                    'product_data': {
                        'name': f'Carrito de {user}',
                    },
                    'unit_amount': total_payment,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8080/success',
            cancel_url='http://127.0.0.1:8080/cancel',
        )
        return jsonify({'id': stripe_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

## SUSCRIPCIONES

@app.route('/suscripcion_exitosa')
def suscripcion_exitosa():
    if 'username' not in session:
        return render_template('cancel.html', message='No estás autenticado'), 401

    username = session['username']
    response = requests.post('http://localhost:5000/api/subscribe', json={'username': username})
    subscription_successful = False

    if response.status_code == 200:
        message = 'Suscripción actualizada correctamente'
        subscription_successful = True
    else:
        message = response.json().get('message', 'Error en la suscripción')
        subscription_successful = False
    return render_template('suscripcion_exitosa.html', message=message, subscription_successful=subscription_successful)
 
# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)





class Product:
    def __init__(self, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.name = name
        self.price = price

    def apply_discount(self, discount):
        if not (0 <= discount <= 1):
            raise ValueError("Discount must be between 0 and 1")
        self.price *= (1 - discount)

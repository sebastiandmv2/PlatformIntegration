import requests
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pymysql
pymysql.install_as_MySQLdb()
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

# Configuración de MySQL
app.config['MYSQL_USER'] = 'tuusuario'
app.config['MYSQL_PASSWORD'] = 'tucontraseña'
app.config['MYSQL_DB'] = 'tubasededatos'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def catalogo():
    tools_type_id = request.args.get('tools_type_id')
    url = 'http://localhost:5000/tools'
    
    if tools_type_id:
        url += f'?tools_type_id={tools_type_id}'
    
    response = requests.get(url)
    products = response.json()
    valor_dolar_ayer = obtener_valor_dolar("ast.gonzalez@duocuc.cl", "V25713451.2")

    for product in products:
        product['price_usd'] = round(float(product['price']) / float(valor_dolar_ayer), 2)

    return render_template('catalogo.html', products=products, valor_dolar=valor_dolar_ayer)

@app.route('/categorias', methods=['GET'])
def show_categorias():
    response = requests.get('http://localhost:5000/tools_types')
    tools_types = response.json()
    return render_template('categorias.html', tools_types=tools_types)

@app.route('/carrito', methods=['GET'])
def mostrar_carrito():
    def calcular_total(carrito):
        total = 0
        for product in carrito:
            try:
                total += float(product['price']) * int(product['quantity'])
            except (ValueError, TypeError):
                print("Error: Los valores de precio y cantidad deben ser números.")
        return total

    total_clp = calcular_total(carrito)
    valor_dolar_ayer = obtener_valor_dolar("ast.gonzalez@duocuc.cl", "V25713451.2")

    for product in carrito:
        response = requests.get(f'http://localhost:5000/tools/{product["id"]}')
        product_details = response.json()
        product['price_usd'] = round(float(product_details['price']) / float(valor_dolar_ayer), 2)

    total_usd = sum(product['price_usd'] * int(product['quantity']) for product in carrito)
    session['total_clp'] = total_clp

    return render_template('carrito.html', products=carrito, total_clp=total_clp, total_usd=total_usd)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data['productId']
    quantity = data['quantity']

    response = requests.get(f'http://localhost:5000/tools/{product_id}')
    product = response.json()

    cart_item = {'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': quantity}
    carrito.append(cart_item)

    return jsonify({'message': 'Producto agregado al carrito', 'product': cart_item})

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    data = request.get_json()
    product_id = data['productId']
    new_quantity = data['quantity']

    for item in carrito:
        if item['id'] == product_id:
            item['quantity'] = new_quantity
            break

    return jsonify({'message': 'Cantidad del producto actualizada exitosamente en el carrito'})

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    product_id = data['productId']

    for product in carrito:
        if product['id'] == product_id:
            carrito.remove(product)
            return jsonify({'message': 'Producto eliminado del carrito', 'product': product})

    return jsonify({'error': 'Producto no encontrado en el carrito'}), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        response = requests.post('http://localhost:5000/api/login', json={'username': username, 'password': password})
        
        if response.status_code == 200:
            session['username'] = username
            return redirect(url_for('catalogo'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('catalogo'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        response = requests.post('http://localhost:5000/api/register', json={'username': username, 'password': password, 'email': email})
        
        if response.status_code == 201:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', message='Error al registrar el usuario')

    return render_template('register.html')

@app.route('/profile/<username>', methods=['GET'])
def user_profile(username):
    response = requests.get(f'http://localhost:5000/api/profile?username={username}')

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

@app.route('/modify_email', methods=['POST'])
def modify_email():
    username = session['username']
    new_email = request.form['new_email']

    response = requests.put('http://localhost:5000/api/profile/email', json={'username': username, 'new_email': new_email})

    if response.status_code == 200:
        message = response.json().get('message', 'Correo electrónico modificado exitosamente')
    else:
        message = response.json().get('message', 'Error al modificar el correo electrónico')
    
    return redirect(url_for('edit_user_profile', message=message))

@app.route('/modify_password', methods=['POST'])
def modify_password():
    username = session['username']
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    response = requests.put('http://localhost:5000/api/profile/password', json={'username': username, 'current_password': current_password, 'new_password': new_password, 'confirm_password': confirm_password})

    if response.status_code == 200:
        message = 'Contraseña modificada exitosamente'
    else:
        message = response.json()['message']
    return redirect(url_for('edit_user_profile', message=message))

@app.route('/success')
def success():
    session.pop('total_clp', None)
    carrito.clear()
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        total_clp = session.get('total_clp', None)
        if total_clp is not None:
            total_clp = int(total_clp)

        user = session.get('username', None)

        stripe_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'clp',
                    'product_data': {
                        'name': f'Carrito de {user}',
                    },
                    'unit_amount': total_clp,
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
    
    
@app.route('/suscripcion_exitosa')
def suscripcion_exitosa():
    return render_template('suscripcion_exitosa.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)




<h1 align="center">
    <img src="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=35&center=true&vCenter=true&width=500&height=70&duration=4000&lines=Hi+There!+👋;+We+are+IT+REX!🦖;" />
</h1>

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&random=false&width=435&lines=Proyecto+Integracion+de+Palataformas)](https://git.io/typing-svg)
<hr/>


 ## 🌱 Aplicación de Carrito de Compras para Ferretería ***FERREMAS***

<hr/>


## ⚙️ Acerca de la Aplicación

Bienvenido a la aplicación de carrito de compras para la ferretería FERREMAS, diseñada para ofrecer una experiencia de compra fluida y eficiente. Esta aplicación web, construida principalmente con Python, HTML, y JavaScript utilizando Flask, proporciona una solución integral para la gestión de compras en línea.



- Inicio de sesión seguro: Accede a tu cuenta de forma rápida y segura.
- Conexión a base de datos MySQL: Gestión eficiente y robusta de los datos de productos y usuarios
- Integración con plataformas de pago: Realiza tus pagos de forma segura y conveniente.
- Actualización de precios en tiempo real: Gracias a la conexión con la API del Banco Central, maneja las transacciones en dólares de manera precisa.
- Carrito de compra intuitivo: Añade productos, modifica cantidades y revisa tu orden antes de la compra.
- Sistema de suscripción para descuentos: Suscríbete y recibe descuentos exclusivos para tus compras.



La aplicación de FERREMAS no solo facilita el proceso de compra, sino que también garantiza una experiencia de usuario excelente, manteniendo siempre la seguridad y eficiencia como prioridades. ¡Explora, compra y disfruta de nuestros servicios!

<hr/>

<h1 align="center"> 📚 Lenguajes y Tecnología </h1> 

### LENGUAJES

- HTML/CSS
- JavaScript
- Python

### TECNOLOGÍA
Base de Datos
- MySQL

  
<hr/>
<h1 align="center"> 🧱 Arquitectura </h1>

### 1. Cliente (Frontend)
 - Tecnologías utilizadas: HTML, CSS, JavaScript
 - Descripción: La parte del cliente se encarga de la interfaz de usuario y la experiencia de usuario. Incluye las páginas web que los usuarios ven e interactúan con ellas, como el catálogo de productos, el carrito de compras, y el proceso de pago.
   
###  2. Servidor (Backend)
 - Tecnologías utilizadas: Python, Flask (un micro framework para Python)
 - Descripción: El servidor maneja la lógica de negocio, las operaciones de base de datos, y la gestión de sesiones de usuario. Flask se utiliza para crear las rutas y manejar las solicitudes HTTP.
   
###  3. Base de Datos
 - Tecnología utilizada: MySQL
 - Descripción: La base de datos almacena toda la información necesaria, como los datos de los usuarios, los productos, los pedidos y los elementos de los pedidos.
   
###  4. Integración de APIs de Terceros
 - Descripción: Se integran APIs de terceros para funcionalidades como el procesamiento de pagos y la obtención de datos de tipos de cambio.
   
### 5. Despliegue y Hosting
 - Descripción: La aplicación se puede desplegar en un servidor web que soporte Python y Flask. Puede ser en un servidor local durante el desarrollo o en servicios de hosting en la nube como Heroku, AWS, Google Cloud, etc.




<hr/>
<h1 align="center"> 🔧 Detalles del Framework </h1>

###  Flask
### 1. Descripción:
- Flask es un microframework ligero y flexible que proporciona las herramientas necesarias para construir aplicaciones web robustas. Es conocido por su simplicidad y facilidad de uso, lo que lo hace ideal para proyectos pequeños y medianos.
### 3. Características:
- Enrutamiento sencillo: Define rutas y vistas de manera simple y clara.
- Compatibilidad con extensiones: Amplía la funcionalidad de Flask mediante extensiones para la autenticación, el manejo de formularios, y más.
- Soporte para pruebas: Incluye soporte integrado para la creación de pruebas unitarias y de integración.


  
<hr/>
<h1 align="center"> 💻 Pasos de Implementación </h1>

### 1. Configuracion del Entorno de Desarrollo
   - Instalar un IDE (Ej: Visual Studio Code)
   - Configurar el servidor web local (Ej: XAMPP)
   - Clonar el repositorio del proyecto
  
### 2. Pasos en Visual Studio Code   
   - Abrir el *Command Palette* en **VSCODE** (**Ctrl+Shift+P** / **Cmd+Shift+P**).
   - Buscar y seleccionar la opción ***Python: Create Environmment...***
   - Selecciona el ***Ambiente Virtual*** que deseas ocupar. En este caso seleccionaremos ***Venv***.
   - Seleccionar la versión de *Python* a ocupar. Como recomendación ocupar una version de ***Python 3.11./***
   - Antes de crear el ambiente virtual, el asistente les preguntará si desean instalar las librerias que se encuentran en el documento **requirements.txt**. En el caso que tengan el documento, es recomendable instalarlo.
   - En el caso que ya se haya creado un *Ambiente Virtual* con este medio, al seleccionar *Ambiente Virtual* apareceran las opciones ***Use Existing*** y ***Delete an Recreate***. Para ocupar un *Ambiente Virtual* ya     creado, seleccionar la opción *Use Existing*.

## ⚡ Como crear un entorno virtual (Ejecutar el siguiente comando)
```console
virtualenv venv
```
## ⚡ Como instalar las dependencias del proyecto (Ejecutar el siguiente comando)
```console
pip install -r requirements.txt
```
## ⚡ Como activar el entorno virtual (Ejecutar el siguiente comando)
```console
.\venv\Scripts\Activate
```

### 3. Configuración de la Base de Datos
- Configurar el archivo .env con los detalles de la base de datos:
```console
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=ferremas
DB_USERNAME=tu_usuario
DB_PASSWORD=tu_contraseña
```

### 4. Inicio del Servidor
- Iniciar el servidor de desarrollo de Flask:
```console
flask run
```

### 5. Pruebas
- Ejecutar las pruebas unitarias:
```console
pytest
```


<hr/>

<h1 align="center"> 🚨 Script BD en MySQL </h1>
<hr/>


<h1 align="center"> 🧨 Información de Test con Pytest </h1>


- Se realizaron pruebas exhaustivas para garantizar el funcionamiento óptimo del sistema y se generó un informe detallado sobre el rendimiento, seguridad, accesibilidad y mantenimiento del sitio.

Mejora en la Implementación de Tests
- Se desarrollaron pruebas unitarias para verificar la funcionalidad de los componentes principales del sistema, incluyendo la gestión de usuarios, catálogo de productos, carrito de compras, y opciones de pago.

<br>
<hr/>
<h1 align="center">
    <img src="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=35&center=true&vCenter=true&width=500&height=70&duration=4000&lines=Autores;" />
</h1>

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&random=false&width=435&lines=Sebastian+Millar)](https://git.io/typing-svg)
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&random=false&width=435&lines=Astrid+Gonzalez)](https://git.io/typing-svg)
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&random=false&width=435&lines=Constanza+Flores)](https://git.io/typing-svg)
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&random=false&width=435&lines=Nicolas+Silva)](https://git.io/typing-svg)
<hr/>








<h2 align="center">⚒️ Languages-Frameworks-Tools ⚒️</h2>
<br/>
<div align="center">
    <img src="https://skillicons.dev/icons?i=flask,python,html,css,javascript" />
    <img src="https://skillicons.dev/icons?i=bootstrap,github,mysql" /><br>
</div>




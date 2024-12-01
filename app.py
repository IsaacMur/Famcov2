from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify # type: ignore
from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, PasswordField, FloatField, TextAreaField, IntegerField, BooleanField, SelectField, FileField, SubmitField # type: ignore
from wtforms.validators import DataRequired, Regexp # type: ignore
from datetime import timedelta
from config_db import init_db
from config_mail import send_email

#Base de 64 para guardar archivos
import base64


# Importar módulos de Usuario y Producto
from LOGIN.MVVM.login_mvvm import UserViewModel
from PRODUCTOS.MVVM.product_viewmodel import ProductViewModel
from LOGIN.DAO.login_dao import UserDAO
from LOGIN.CQRS.login_cqrs import UserCQRS
from PRODUCTOS.DAO.product_dao import ProductDAO
from PRODUCTOS.CQRS.product_cqrs import ProductCQRS


# Configuración e inicialización de la aplicación
app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = init_db(app)


# Instancias de los modelos de usuario y producto
user_dao = UserDAO(mysql)
user_cqrs = UserCQRS(user_dao)
user_view_model = UserViewModel(user_cqrs)

product_dao = ProductDAO(mysql)
product_cqrs = ProductCQRS(product_dao)
product_view_model = ProductViewModel(product_cqrs)


# Middleware para hacer permanente la sesión
@app.before_request
def make_session_permanent():
    session.permanent = True


# Middleware para desactivar caché
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# Formulario de inicio de sesión seguro
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Regexp(r'^[\w.@+-]+$', message="El usuario solo puede contener letras, números y los caracteres . @ + - _")])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')


# Formulario para agregar productos
class ProductForm(FlaskForm):
    nombre_producto = StringField('Nombre del Producto', validators=[DataRequired()])
    descripcion_producto = TextAreaField('Descripción', validators=[DataRequired()])
    precio_producto = FloatField('Precio', validators=[DataRequired()])
    codigo_producto = IntegerField('Código del Producto', validators=[DataRequired()])
    stock_producto = IntegerField('Stock', validators=[DataRequired()])
    informacion_adicional = TextAreaField('Información Adicional')
    imagen_producto = FileField('Imagen del Producto')
    oferta_producto = BooleanField('Producto en oferta')
    id_categoria = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar')


# Ruta de inicio para la página principal (index)
@app.route('/')
def index():
    # Metodo para mostrar los productos destacados
    productos_destacados = product_view_model.get_featured_products(limit=6)
    return render_template('index.html', productos=productos_destacados)


# Ruta para la página de productos
@app.route('/productos')
def productos():
    # Obtiene solo los productos en oferta
    productos_oferta = product_view_model.get_products_in_offer()
    return render_template('productos.html', productos=productos_oferta)




# Metodo para filtrar productos
@app.route('/filtrado')
def filtrado_de_productos():
    filtros = {
        'nombre': request.args.get('nombre'),
        'precio_min': request.args.get('precio_min', type=float),
        'precio_max': request.args.get('precio_max', type=float),
        'categoria': request.args.get('categoria')
    }
    orden = request.args.get('orden', default='nombre_producto')
    vista = request.args.get('vista', default='cuadrados')

    # Obtener productos filtrados desde la capa ViewModel
    productos_filtrados = product_view_model.get_filtered_products(filtros, orden)

    return render_template(
        'productos.html',
        productos=productos_filtrados,
        vista=vista,
        orden=orden
    )



# Ruta para la página de contacto y enviio de correos
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        try:
            # Datos del formulario
            nombre = request.form['nombre']
            correo = request.form['correo']
            asunto = request.form['asunto']
            mensaje = request.form['mensaje']
            
            # Mensaje para el contacto principal
            mensaje_contacto = f"""
            <p><strong>Nombre:</strong> {nombre}</p>
            <p><strong>Correo:</strong> {correo}</p>
            <p><strong>Asunto:</strong> {asunto}</p>
            <p><strong>Mensaje:</strong></p>
            <p>{mensaje}</p>
            """

            # Mensaje de agradecimiento para el usuario
            mensaje_usuario = f"""
            <div style="font-family: 'Arial', sans-serif; color: #333; line-height: 1.6; background-color: #f2f4f4 ; 
            padding: 20px; border-radius: 8px; border: 1px solid #ddd;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h1 style="color: #03A65A; margin: 0;">🔬 ¡Gracias por contactarnos, {nombre}! 🩺</h1>
                    <p style="font-size: 1.2em; color: #555;">Nos encanta saber de profesionales como tú. 😊</p>
                </div>
                <p style="color: #555;">
                    Hola <strong>{nombre}</strong>,<br>
                    Hemos recibido tu mensaje y queremos agradecerte por confiar en Famco. 
                    Estamos comprometidos a ofrecerte soluciones médicas especializadas y de la más alta calidad. 
                    Nuestro equipo ya está revisando tu solicitud y nos pondremos en contacto contigo lo más pronto posible.
                </p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                <footer style="text-align: center; color: #777; font-size: 0.9em;">
                    <p>Este es un mensaje automático. Por favor, no respondas a este correo.</p>
                    <p style="font-size: 0.8em;">Famco - Artículos Médicos Especializados</p>
                </footer>
            </div>
            """

            # Enviar correo al contacto principal
            resultado_contacto = send_email(
                to_email='contacto@edgecloud.com.mx',
                subject=f"Contacto - Pagina web",
                message=mensaje_contacto,
                is_html=True 
            )

            # Enviar correo de agradecimiento al usuario
            resultado_usuario = send_email(
                to_email=correo,
                subject="Famco - Gracias por contactarnos",
                message=mensaje_usuario,
                is_html=True  # Habilitamos HTML
            )
        except Exception as e:
            flash(f"Error al procesar el formulario: {str(e)}")
        return redirect('/contacto')
    return render_template('contacto.html')


# Ruta para pagina de detalle del producto
@app.route('/detalle_producto')
def detalle_producto():
    return render_template('detalle_producto.html')


# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        if user_view_model.login_user(username, password):
            session['username'] = username  # Guarda el nombre de usuario en la sesión
            return jsonify(success=True)  # Respuesta en JSON para indicar éxito
        else:
            return jsonify(success=False, message="Credenciales inválidas. Inténtalo de nuevo.")
    return render_template('login.html', form=form)


# Ruta para cerrar sesión
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


# Ruta para la página de productos (Administrador)
@app.route('/administrador', methods=['GET', 'POST'])
def administrador():
    if 'username' not in session:
        flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
        return redirect(url_for('login'))
    
    form = ProductForm()
    form.id_categoria.choices = [(c['id_categoria'], c['nombre_categoria']) for c in product_view_model.get_all_categories()]

    if form.validate_on_submit():
        product_view_model.insert_product(
            form.nombre_producto.data,
            form.precio_producto.data,
            form.descripcion_producto.data,
            form.codigo_producto.data,
            form.stock_producto.data,
            form.informacion_adicional.data,
            form.imagen_producto.data.read() if form.imagen_producto.data else None,
            form.oferta_producto.data,
            form.id_categoria.data
        )
        flash("Producto agregado correctamente", "success")
        return redirect(url_for('administrador'))

    search_query = request.args.get('search', '') 
    productos = product_view_model.search_products(search_query) if search_query else product_view_model.get_all_products()
    
    return render_template('Administrador.html', form=form, productos=productos)


#Ruta para eliminar producto
@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    if 'username' not in session:
        flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
        return redirect(url_for('login'))

    product_id = request.form.get('product_id')
    if product_id:
        product_view_model.delete_product(int(product_id))
        flash('Producto eliminado correctamente.', 'success')
    else:
        flash('No se pudo eliminar el producto.', 'danger')
    
    return redirect(url_for('administrador'))


# Ruta para editar producto
@app.route('/editar_producto/<int:product_id>', methods=['POST'])
def editar_producto(product_id):
    nombre_producto = request.form['nombre_producto']
    descripcion_producto = request.form['descripcion_producto']
    precio_producto = request.form['precio_producto']
    codigo_producto = request.form['codigo_producto']
    stock_producto = request.form['stock_producto']
    informacion_adicional = request.form['informacion_adicional']
    oferta_producto = 'oferta_producto' in request.form
    id_categoria = request.form['id_categoria']
    
    if 'imagen_producto' in request.files and request.files['imagen_producto'].filename != '':
        imagen_producto = request.files['imagen_producto'].read()
    else:
        producto_actual = product_view_model.get_product_by_id(product_id)
        imagen_producto = producto_actual['imagen_producto'] if producto_actual else None

    product_view_model.update_product(
        product_id, nombre_producto, precio_producto, descripcion_producto, codigo_producto,
        stock_producto, informacion_adicional, imagen_producto, oferta_producto, id_categoria
    )
    
    flash("Producto actualizado correctamente", "success")
    return redirect(url_for('administrador'))


# Ruta para obtner producto por id
@app.route('/obtener_producto/<int:product_id>', methods=['GET'])
def obtener_producto(product_id):
    producto = product_view_model.get_product_by_id(product_id)
    if producto:
        imagen_base64 = base64.b64encode(producto["imagen_producto"]).decode('utf-8') if producto["imagen_producto"] else None
        
        return jsonify({
            "id_producto": producto["id_producto"],
            "nombre_producto": producto["nombre_producto"],
            "precio_producto": producto["precio_producto"],
            "descripcion_producto": producto["descripcion_producto"],
            "codigo_producto": producto["codigo_producto"],
            "stock_producto": producto["stock_producto"],
            "informacion_adicional": producto["informacion_adicional"],
            "imagen_producto": imagen_base64,
            "oferta_producto": producto["oferta_producto"],
            "id_categoria": producto["id_categoria"]
        })
    return jsonify({"error": "Producto no encontrado"}), 404


@app.route('/productos')
def ver_productos():
    productos = product_view_model.get_all_products()
    return render_template('productos.html', productos=productos)



# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=8080)

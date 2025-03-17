from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from datetime import datetime
import os
from dotenv import load_dotenv
import qrcode
from io import BytesIO
import base64

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///pidamo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Importar modelos y blueprint de autenticación
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'mozo', 'cocina'
    
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return str(self.id)
    
class Mesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    qr_code = db.Column(db.String(200))
    estado = db.Column(db.String(20), default='libre')  # libre, ocupada, pidiendo
    
    def generar_qr(self, request_base_url):
        """Genera un código QR para la mesa"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # URL que se codificará en el QR
        url = f"{request_base_url}/menu?mesa={self.numero}"
        qr.add_data(url)
        qr.make(fit=True)

        # Crear imagen QR
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir imagen a base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    imagen_url = db.Column(db.String(200))
    disponible = db.Column(db.Boolean, default=True)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, en_preparacion, listo, entregado
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, default=0.0)
    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)

class DetallePedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    notas = db.Column(db.Text)
    producto = db.relationship('Producto', backref='detalles_pedido', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas básicas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    mesa_id = request.args.get('mesa')
    productos = Producto.query.filter_by(disponible=True).all()
    return render_template('menu.html', productos=productos, mesa_id=mesa_id)

@app.route('/cocina')
@login_required
def cocina():
    if current_user.role not in ['admin', 'cocina']:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('index'))
    pedidos = Pedido.query.filter_by(estado='pendiente').all()
    return render_template('cocina.html', pedidos=pedidos)

@app.route('/mozos')
@login_required
def mozos():
    if current_user.role not in ['admin', 'mozo']:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('index'))
    mesas = Mesa.query.all()
    return render_template('mozos.html', mesas=mesas)

@app.route('/boss')
@login_required
def boss():
    if current_user.role != 'admin':
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('index'))
    pedidos = Pedido.query.all()
    mesas = Mesa.query.all()
    return render_template('boss.html', pedidos=pedidos, mesas=mesas)

# API endpoints
@app.route('/api/pedido', methods=['POST'])
def crear_pedido():
    data = request.get_json()
    
    if not data or 'items' not in data or 'mesa_id' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
        
    try:
        mesa = Mesa.query.filter_by(numero=int(data['mesa_id'])).first()
        if not mesa:
            return jsonify({'error': 'Mesa no encontrada'}), 404
            
        pedido = Pedido(
            mesa_id=mesa.id,
            total=float(data['total'])
        )
        db.session.add(pedido)
        
        for item in data['items']:
            producto = Producto.query.get(item['id'])
            if not producto:
                continue
                
            detalle = DetallePedido(
                pedido=pedido,
                producto_id=producto.id,
                cantidad=item['quantity'],
                precio_unitario=producto.precio,
                notas=item.get('notas', '')
            )
            db.session.add(detalle)
            
        mesa.estado = 'pidiendo'
        db.session.commit()
        
        return jsonify({'message': 'Pedido creado exitosamente', 'pedido_id': pedido.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/mesa/<int:mesa_id>/estado', methods=['PUT'])
@login_required
def actualizar_estado_mesa(mesa_id):
    if current_user.role not in ['admin', 'mozo']:
        return jsonify({'error': 'No autorizado'}), 403
        
    data = request.get_json()
    if not data or 'estado' not in data:
        return jsonify({'error': 'Estado no especificado'}), 400
        
    try:
        mesa = Mesa.query.get(mesa_id)
        if not mesa:
            return jsonify({'error': 'Mesa no encontrada'}), 404
            
        mesa.estado = data['estado']
        db.session.commit()
        
        return jsonify({'message': 'Estado actualizado exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/pedido/<int:pedido_id>/estado', methods=['PUT'])
@login_required
def actualizar_estado_pedido(pedido_id):
    if current_user.role not in ['admin', 'cocina', 'mozo']:
        return jsonify({'error': 'No autorizado'}), 403
        
    data = request.get_json()
    if not data or 'estado' not in data:
        return jsonify({'error': 'Estado no especificado'}), 400
        
    try:
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            return jsonify({'error': 'Pedido no encontrado'}), 404
            
        pedido.estado = data['estado']
        db.session.commit()
        
        return jsonify({'message': 'Estado actualizado exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear tablas de la base de datos
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
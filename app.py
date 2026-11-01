from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///marketplace.db')
# Convertir postgres:// a postgresql:// y luego a postgresql+psycopg:// para usar psycopg3
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql+psycopg://', 1)
elif app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgresql://', 'postgresql+psycopg://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Crear carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='cliente')  # admin, emprendedora, cliente
    
    # Información de contacto
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    
    # Redes sociales
    facebook = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    whatsapp = db.Column(db.String(20))
    
    # Información adicional
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(300))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con productos
    products = db.relationship('Product', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(300))
    is_service = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Inicializar base de datos automáticamente
def init_db():
    """Inicializa la base de datos y crea usuario admin si no existe"""
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Crear usuario admin por defecto si no existe
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@marketplace.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('✓ Usuario admin creado: admin / admin123')

# Ejecutar inicialización al importar el módulo
try:
    init_db()
except Exception as e:
    print(f'Error al inicializar base de datos: {e}')

# Rutas principales
@app.route('/')
def index():
    products = Product.query.filter_by(active=True).order_by(Product.created_at.desc()).all()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'cliente')
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado', 'error')
            return redirect(url_for('register'))
        
        if role == 'admin' and (not current_user.is_authenticated or current_user.role != 'admin'):
            role = 'cliente'
        
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('¡Registro exitoso! Por favor inicia sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'¡Bienvenida, {user.username}!', 'success')
            
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'emprendedora':
                return redirect(url_for('emprendedora_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

# Panel de Administración
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    products = Product.query.all()
    stats = {
        'total_users': User.query.count(),
        'total_emprendedoras': User.query.filter_by(role='emprendedora').count(),
        'total_products': Product.query.count(),
        'active_products': Product.query.filter_by(active=True).count()
    }
    
    return render_template('admin_dashboard.html', users=users, products=products, stats=stats)

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'error': 'No puedes eliminar tu propia cuenta'}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Actualizar información básica
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        
        # Verificar si el username ya existe (excepto el actual)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user.id:
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('admin_edit_user', user_id=user_id))
        
        # Verificar si el email ya existe (excepto el actual)
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != user.id:
            flash('El correo electrónico ya está registrado', 'error')
            return redirect(url_for('admin_edit_user', user_id=user_id))
        
        user.username = username
        user.email = email
        user.role = role
        
        # Actualizar información de contacto
        user.phone = request.form.get('phone', '')
        user.address = request.form.get('address', '')
        user.bio = request.form.get('bio', '')
        
        # Actualizar redes sociales
        user.facebook = request.form.get('facebook', '')
        user.instagram = request.form.get('instagram', '')
        user.twitter = request.form.get('twitter', '')
        user.whatsapp = request.form.get('whatsapp', '')
        
        # Cambiar contraseña si se proporciona
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        db.session.commit()
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_edit_user.html', user=user)

@app.route('/admin/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_product(product_id):
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price', 0))
        product.category = request.form.get('category')
        product.is_service = request.form.get('is_service') == 'on'
        product.active = request.form.get('active') == 'on'
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                product.image = f"uploads/{filename}"
        
        db.session.commit()
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_edit_product.html', product=product)

@app.route('/admin/product/<int:product_id>/delete', methods=['POST'])
@login_required
def admin_delete_product(product_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/product/<int:product_id>/toggle', methods=['POST'])
@login_required
def admin_toggle_product(product_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    product = Product.query.get_or_404(product_id)
    product.active = not product.active
    db.session.commit()
    return jsonify({'success': True, 'active': product.active})

# Panel de Emprendedora
@app.route('/emprendedora/dashboard')
@login_required
def emprendedora_dashboard():
    if current_user.role not in ['emprendedora', 'admin']:
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.filter_by(user_id=current_user.id).order_by(Product.created_at.desc()).all()
    return render_template('emprendedora_dashboard.html', products=products)

@app.route('/emprendedora/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if current_user.role not in ['emprendedora', 'admin']:
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        category = request.form.get('category')
        is_service = request.form.get('is_service') == 'on'
        
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_path = f"uploads/{filename}"
        
        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            is_service=is_service,
            image=image_path,
            user_id=current_user.id
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('¡Producto creado exitosamente!', 'success')
        return redirect(url_for('emprendedora_dashboard'))
    
    return render_template('product_form.html', product=None)

@app.route('/emprendedora/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.user_id != current_user.id and current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price', 0))
        product.category = request.form.get('category')
        product.is_service = request.form.get('is_service') == 'on'
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                product.image = f"uploads/{filename}"
        
        db.session.commit()
        flash('¡Producto actualizado exitosamente!', 'success')
        return redirect(url_for('emprendedora_dashboard'))
    
    return render_template('product_form.html', product=product)

@app.route('/emprendedora/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/emprendedora/product/<int:product_id>/toggle', methods=['POST'])
@login_required
def toggle_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    product.active = not product.active
    db.session.commit()
    return jsonify({'success': True, 'active': product.active})

@app.route('/product/<int:product_id>')
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    product_type = request.args.get('type', '')
    
    products = Product.query.filter_by(active=True)
    
    if query:
        products = products.filter(
            db.or_(
                Product.name.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%')
            )
        )
    
    if category:
        products = products.filter_by(category=category)
    
    if product_type == 'product':
        products = products.filter_by(is_service=False)
    elif product_type == 'service':
        products = products.filter_by(is_service=True)
    
    products = products.order_by(Product.created_at.desc()).all()
    return render_template('search.html', products=products, query=query, category=category, product_type=product_type)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

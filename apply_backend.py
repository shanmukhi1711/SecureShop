import os
import shutil

base_dir = "c:/Users/Sree/SecureShopy"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

app_py = """import os
from flask import Flask, render_template
from config import config_by_name
from models.models import db, User, Product, Cart, CartItem, Order, OrderItem
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_name='secure'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    db.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from security_lab.routes import lab_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(lab_bp, url_prefix='/lab')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    mode = os.environ.get('LAB_MODE', 'secure')
    app = create_app(mode)
    
    with app.app_context():
        db.create_all()
        # Admin User
        if not User.query.filter_by(username='admin').first():
            admin = User(name='Administrator', email='admin@secureshop.local', username='admin', role='admin')
            admin.set_password('Admin@123')
            db.session.add(admin)
            
        # Customer User
        if not User.query.filter_by(username='customer').first():
            customer = User(name='Customer User', email='customer@secureshop.local', username='customer', role='customer')
            customer.set_password('Customer@123')
            db.session.add(customer)
            
        # Sample Products
        if not Product.query.first():
            products = [
                Product(name='Wireless Headphones', description='High-quality wireless headphones with noise cancellation.', price=199.99, category='Electronics', stock=50, rating=4.8),
                Product(name='Mechanical Keyboard', description='RGB mechanical keyboard with tactile switches.', price=129.99, category='Accessories', stock=30, rating=4.7),
                Product(name='Smart Watch', description='Fitness and health tracking smart watch.', price=249.99, category='Electronics', stock=40, rating=4.6),
                Product(name='USB-C Hub', description='7-in-1 USB-C hub with HDMI and card reader.', price=45.99, category='Accessories', stock=100, rating=4.5),
                Product(name='Laptop Stand', description='Ergonomic aluminum laptop stand.', price=35.99, category='Accessories', stock=80, rating=4.4),
                Product(name='Bluetooth Speaker', description='Portable waterproof bluetooth speaker.', price=79.99, category='Electronics', stock=60, rating=4.3),
                Product(name='Gaming Mouse', description='High precision wireless gaming mouse.', price=89.99, category='Accessories', stock=45, rating=4.7),
                Product(name='Premium Backpack', description='Water-resistant laptop backpack.', price=65.99, category='Accessories', stock=70, rating=4.6),
                Product(name='Desk Lamp', description='LED desk lamp with adjustable brightness.', price=29.99, category='Home', stock=120, rating=4.2),
                Product(name='HD Webcam', description='1080p HD webcam with built-in microphone.', price=55.99, category='Electronics', stock=55, rating=4.5),
                Product(name='Power Bank', description='20000mAh high capacity fast charging power bank.', price=49.99, category='Electronics', stock=90, rating=4.8),
                Product(name='Python Programming Book', description='Comprehensive guide to Python programming.', price=39.99, category='Books', stock=150, rating=4.9)
            ]
            db.session.add_all(products)
            
        db.session.commit()
    
    app.run(host='127.0.0.1', port=5000)
"""

auth_py = """from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.models import User, db, Cart

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
            
        new_user = User(name=name, email=email, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # Create cart for user
        new_cart = Cart(user_id=new_user.id)
        db.session.add(new_cart)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
"""

main_py = """from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models.models import Product, db, Cart, CartItem, Order, OrderItem, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    products = Product.query.limit(4).all()
    return render_template('index.html', products=products)

@main_bp.route('/products')
def products():
    search = request.args.get('search')
    category = request.args.get('category')
    sort = request.args.get('sort')
    
    query = Product.query
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
        
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.id.desc())
        
    all_products = query.all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    return render_template('products.html', products=all_products, categories=categories, search=search)

@main_bp.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

@main_bp.route('/cart')
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    items = CartItem.query.filter_by(cart_id=cart.id).all()
    total = sum(item.product.price * item.quantity for item in items)
    return render_template('cart.html', items=items, total=total)

@main_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if product.stock < quantity:
        flash('Not enough stock available', 'error')
        return redirect(request.referrer or url_for('main.products'))
        
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
        
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity + quantity > product.stock:
            flash('Cannot add more than available stock', 'error')
        else:
            cart_item.quantity += quantity
            flash('Cart updated', 'success')
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        flash('Product added to cart', 'success')
        
    db.session.commit()
    return redirect(request.referrer or url_for('main.products'))

@main_bp.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.cart.user_id != current_user.id:
        return render_template('403.html'), 403
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart', 'success')
    return redirect(url_for('main.cart'))

@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    items = CartItem.query.filter_by(cart_id=cart.id).all() if cart else []
    
    if not items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('main.cart'))
        
    total = sum(item.product.price * item.quantity for item in items)
    
    if request.method == 'POST':
        # Create order
        order = Order(user_id=current_user.id, total=total, status='Processing')
        db.session.add(order)
        db.session.commit()
        
        for item in items:
            if item.product.stock < item.quantity:
                flash(f'Sorry, {item.product.name} does not have enough stock.', 'error')
                db.session.delete(order)
                db.session.commit()
                return redirect(url_for('main.cart'))
            
            item.product.stock -= item.quantity
            order_item = OrderItem(order_id=order.id, product_id=item.product.id, quantity=item.quantity, price=item.product.price)
            db.session.add(order_item)
            db.session.delete(item)
            
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main.order_confirmation', order_id=order.id))
        
    return render_template('checkout.html', items=items, total=total)

@main_bp.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return render_template('403.html'), 403
    return render_template('order_confirmation.html', order=order)

@main_bp.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        user = User.query.get(current_user.id)
        user.name = name
        user.email = email
        db.session.commit()
        flash('Profile updated successfully', 'success')
        
    return render_template('profile.html', user=current_user)
"""

admin_py = """from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models.models import Product, User, Order, db
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return render_template('403.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'users': User.query.count(),
        'products': Product.query.count(),
        'orders': Order.query.count(),
        'revenue': sum(o.total for o in Order.query.all())
    }
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)

@admin_bp.route('/products')
@admin_required
def products():
    all_products = Product.query.all()
    return render_template('admin/products.html', products=all_products)

@admin_bp.route('/product/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        p = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category=request.form.get('category'),
            stock=int(request.form.get('stock')),
            rating=float(request.form.get('rating', 0))
        )
        db.session.add(p)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', product=None)

@admin_bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.category = request.form.get('category')
        product.stock = int(request.form.get('stock'))
        product.rating = float(request.form.get('rating', 0))
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', product=product)

@admin_bp.route('/product/delete/<int:id>')
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin.products'))
    
@admin_bp.route('/orders')
@admin_required
def orders():
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=all_orders)
    
@admin_bp.route('/order/<int:id>/status', methods=['POST'])
@admin_required
def update_order_status(id):
    order = Order.query.get_or_404(id)
    order.status = request.form.get('status')
    db.session.commit()
    flash('Order status updated', 'success')
    return redirect(url_for('admin.orders'))
"""

write_file(f"{base_dir}/app.py", app_py)
write_file(f"{base_dir}/routes/auth.py", auth_py)
write_file(f"{base_dir}/routes/main.py", main_py)
write_file(f"{base_dir}/routes/admin.py", admin_py)
print("Backend py files injected successfully")

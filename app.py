import os
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

    @app.template_filter('inr')
    def format_inr(value):
        try:
            return f"₹{float(value):,.2f}"
        except (ValueError, TypeError):
            return f"₹{value}"

    @app.context_processor
    def inject_global_data():
        cart_count = 0
        from flask_login import current_user
        if current_user.is_authenticated:
            user_cart = Cart.query.filter_by(user_id=current_user.id).first()
            if user_cart and user_cart.items:
                cart_count = sum(item.quantity for item in user_cart.items)
        return dict(cart_item_count=cart_count)

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
                Product(name='Wireless Headphones', description='High-quality wireless headphones with active noise cancellation and 40h battery.', price=4999.00, category='Audio', stock=50, image_url='headphones.jpg', rating=4.8),
                Product(name='Mechanical Keyboard', description='Tactile RGB mechanical keyboard with customizable backlight and hot-swappable switches.', price=3499.00, category='Accessories', stock=30, image_url='keyboard.jpg', rating=4.7),
                Product(name='Smart Watch', description='Advanced fitness and health tracking smartwatch with AMOLED display and ECG monitor.', price=14999.00, category='Wearables', stock=40, image_url='smartwatch.jpg', rating=4.6),
                Product(name='USB-C Hub', description='7-in-1 multi-port aluminum USB-C hub with 4K HDMI, 100W PD charging, and SD reader.', price=1899.00, category='Accessories', stock=100, image_url='usbc_hub.jpg', rating=4.5),
                Product(name='Laptop Stand', description='Ergonomic anodized aluminum laptop stand with heat dissipation and height adjustment.', price=1299.00, category='Accessories', stock=80, image_url='laptop_stand.jpg', rating=4.4),
                Product(name='Bluetooth Speaker', description='Portable IPX7 waterproof Bluetooth speaker with 360-degree sound and 24-hour playtime.', price=2999.00, category='Audio', stock=60, image_url='speaker.jpg', rating=4.3),
                Product(name='Gaming Mouse', description='Ultra-lightweight wireless gaming mouse with 26K DPI optical sensor and PTFE feet.', price=2499.00, category='Accessories', stock=45, image_url='mouse.jpg', rating=4.7),
                Product(name='Premium Backpack', description='Water-resistant tech commuter backpack with padded laptop sleeve and anti-theft design.', price=2199.00, category='Accessories', stock=70, image_url='backpack.jpg', rating=4.6),
                Product(name='Desk Lamp', description='Smart LED desk lamp with adjustable color temperature, dimmer, and wireless charging pad.', price=1499.00, category='Accessories', stock=120, image_url='lamp.jpg', rating=4.2),
                Product(name='HD Webcam', description='1080p Full HD streaming webcam with dual noise-reduction microphones and privacy shutter.', price=3299.00, category='Accessories', stock=55, image_url='webcam.jpg', rating=4.5),
                Product(name='Power Bank', description='20000mAh ultra-fast charging power bank with 65W Power Delivery and digital battery display.', price=1999.00, category='Accessories', stock=90, image_url='powerbank.jpg', rating=4.8),
                Product(name='Python Programming Book', description='Comprehensive guide to Python programming, systems architecture, and web development.', price=899.00, category='Accessories', stock=150, image_url='python_book.jpg', rating=4.9),
                Product(name='UltraBook Pro 15', description='High-performance 15.6-inch aluminum ultrabook with 16-core processor, 16GB RAM, and 1TB SSD.', price=89999.00, category='Laptops', stock=25, image_url='laptop.jpg', rating=4.9),
                Product(name='Galaxy S24 Ultra Smartphone', description='Next-generation AI flagship smartphone with titanium frame, 200MP camera, and Dynamic AMOLED 2X.', price=119999.00, category='Mobiles', stock=35, image_url='smartphone.jpg', rating=4.9),
                Product(name='Pro True Wireless Earbuds', description='Active Noise Cancellation earbuds with personalized spatial audio, transparency mode, and wireless case.', price=8999.00, category='Audio', stock=45, image_url='earbuds.jpg', rating=4.8),
                Product(name='UltraWide 4K Gaming Monitor 34"', description='34-inch curved ultra-wide gaming monitor with 144Hz refresh rate, 1ms response time, and HDR 400.', price=42999.00, category='Monitors', stock=20, image_url='monitor.jpg', rating=4.8),
                Product(name='Pro Mirrorless 4K Camera', description='Compact mirrorless camera with 24.2MP full-frame sensor, 4K60p video recording, and real-time subject tracking.', price=64999.00, category='Accessories', stock=15, image_url='camera.jpg', rating=4.9),
                Product(name='UltraPad Pro 11-inch Tablet', description='Liquid Retina display tablet with high-speed octa-core chip, stylus support, and all-day battery life.', price=54999.00, category='Mobiles', stock=30, image_url='tablet.jpg', rating=4.8),
                Product(name='RGB Gaming Headset & Stand', description='Immersive 7.1 surround sound gaming headset with noise-canceling microphone and matching RGB headset stand.', price=5499.00, category='Accessories', stock=40, image_url='gaming_accessories.jpg', rating=4.7),
                Product(name='Apple MacBook Air 15" M3', description='Incredibly thin and fast laptop with Apple M3 chip, Liquid Retina display, and 18 hours of battery life.', price=124990.00, category='Laptops', stock=18, image_url='macbook.jpg', rating=5.0)
            ]
            db.session.add_all(products)
            
        db.session.commit()
    
    app.run(host='127.0.0.1', port=5000)

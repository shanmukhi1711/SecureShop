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

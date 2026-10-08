import os

files = {
    'routes/__init__.py': '',
    'routes/auth.py': '''
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
            
        user = User(username=username, email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')
''',
    'routes/main.py': '''
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models.models import Product, db, Cart, CartItem, Order, OrderItem

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    products = Product.query.limit(4).all()
    return render_template('index.html', products=products)

@main_bp.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)
''',
    'routes/admin.py': '''
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models.models import User, Product, Order, db
from functools import wraps
from werkzeug.exceptions import Forbidden

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            raise Forbidden("Admin access required")
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'users': User.query.count(),
        'products': Product.query.count(),
        'orders': Order.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)
''',
    'security_lab/__init__.py': '',
    'security_lab/routes.py': '''
from flask import Blueprint, render_template

lab_bp = Blueprint('lab', __name__)

@lab_bp.route('/')
def index():
    return render_template('lab/index.html')
''',
    'templates/base.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureShop - Smart Shopping. Secure by Design.</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('main.index') }}">SecureShop</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="{{ url_for('main.products') }}">Products</a></li>
                    {% if current_user.is_authenticated %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.logout') }}">Logout</a></li>
                        {% if current_user.role == 'admin' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.dashboard') }}">Admin</a></li>
                        {% endif %}
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.login') }}">Login</a></li>
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.register') }}">Register</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
''',
    'templates/index.html': '''
{% extends "base.html" %}
{% block content %}
<div class="p-5 mb-4 bg-light rounded-3 text-center">
    <h1 class="display-4 fw-bold">Welcome to SecureShop</h1>
    <p class="fs-4">Smart Shopping. Secure by Design.</p>
    <a href="{{ url_for('main.products') }}" class="btn btn-primary btn-lg">Shop Now</a>
</div>
{% endblock %}
''',
    'templates/login.html': '''
{% extends "base.html" %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-body p-5">
                <h2 class="text-center mb-4">Login</h2>
                <form method="POST">
                    <div class="mb-3">
                        <label>Username</label>
                        <input type="text" name="username" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label>Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
                <div class="mt-3 text-center text-muted">Demo: alice / Password123! | admin / Admin123!</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
''',
    'templates/register.html': '''
{% extends "base.html" %}
{% block content %}
<h2>Register</h2>
<form method="POST">
    <div class="mb-3"><label>Name</label><input type="text" name="name" class="form-control" required></div>
    <div class="mb-3"><label>Email</label><input type="email" name="email" class="form-control" required></div>
    <div class="mb-3"><label>Username</label><input type="text" name="username" class="form-control" required></div>
    <div class="mb-3"><label>Password</label><input type="password" name="password" class="form-control" required></div>
    <button type="submit" class="btn btn-primary">Register</button>
</form>
{% endblock %}
''',
    'templates/products.html': '''
{% extends "base.html" %}
{% block content %}
<h2>Products</h2>
<div class="row">
    {% for product in products %}
    <div class="col-md-3 mb-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text">${{ product.price }}</p>
                <a href="#" class="btn btn-primary">View</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
''',
    'templates/admin/dashboard.html': '''
{% extends "base.html" %}
{% block content %}
<h2>Admin Dashboard</h2>
<div class="row">
    <div class="col-md-4">
        <div class="card text-white bg-primary mb-3">
            <div class="card-body">
                <h5 class="card-title">Users</h5>
                <p class="card-text">{{ stats.users }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-success mb-3">
            <div class="card-body">
                <h5 class="card-title">Products</h5>
                <p class="card-text">{{ stats.products }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-info mb-3">
            <div class="card-body">
                <h5 class="card-title">Orders</h5>
                <p class="card-text">{{ stats.orders }}</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
''',
    'templates/lab/index.html': '''
{% extends "base.html" %}
{% block content %}
<h2>Security Lab</h2>
<p>Academic security laboratory module.</p>
{% endblock %}
''',
    'static/css/style.css': '''
body {
    background-color: #f8f9fa;
}
.navbar {
    margin-bottom: 20px;
}
'''
}

for path, content in files.items():
    full_path = os.path.join(r'C:\Users\Sree\SecureShopy', path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\\n')

print("Files generated successfully.")

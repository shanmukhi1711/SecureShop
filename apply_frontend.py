import os
base_dir = "c:/Users/Sree/SecureShopy"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SECURESHOP - Smart Shopping. Secure by Design.</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="{{ url_for('main.index') }}" class="brand">SECURESHOP</a>
            
            <div class="nav-links">
                <a href="{{ url_for('main.index') }}">Home</a>
                <a href="{{ url_for('main.products') }}">Products</a>
            </div>

            <div class="nav-actions">
                {% if current_user.is_authenticated %}
                    <a href="{{ url_for('main.cart') }}" class="nav-icon"><i class="fas fa-shopping-cart"></i> Cart</a>
                    <a href="{{ url_for('main.orders') }}" class="nav-icon"><i class="fas fa-box"></i> Orders</a>
                    <a href="{{ url_for('main.profile') }}" class="nav-icon"><i class="fas fa-user"></i> Profile</a>
                    {% if current_user.role == 'admin' %}
                        <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline">Admin</a>
                    {% endif %}
                    <a href="{{ url_for('auth.logout') }}" class="btn btn-primary">Logout</a>
                {% else %}
                    <a href="{{ url_for('auth.login') }}" class="btn btn-outline">Login</a>
                    <a href="{{ url_for('auth.register') }}" class="btn btn-primary">Register</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="flash-messages">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>SECURESHOP</h3>
                <p>Smart Shopping. Secure by Design.</p>
            </div>
            <div class="footer-section">
                <h4>Quick Links</h4>
                <a href="{{ url_for('main.products') }}">Products</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 SecureShop. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

error_404 = """{% extends "base.html" %}
{% block content %}
<div style="text-align: center; padding: 4rem;">
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    <a href="{{ url_for('main.index') }}" class="btn btn-primary">Back to Home</a>
</div>
{% endblock %}"""

error_403 = """{% extends "base.html" %}
{% block content %}
<div style="text-align: center; padding: 4rem;">
    <h1>403 - Forbidden</h1>
    <p>You do not have permission to access this page.</p>
    <a href="{{ url_for('main.index') }}" class="btn btn-primary">Back to Home</a>
</div>
{% endblock %}"""

error_500 = """{% extends "base.html" %}
{% block content %}
<div style="text-align: center; padding: 4rem;">
    <h1>500 - Internal Server Error</h1>
    <p>Something went wrong on our end.</p>
    <a href="{{ url_for('main.index') }}" class="btn btn-primary">Back to Home</a>
</div>
{% endblock %}"""

cart_html = """{% extends "base.html" %}
{% block content %}
<div class="page-header"><h1>Shopping Cart</h1></div>
<div class="container" style="max-width: 800px; margin: 0 auto; padding: 2rem;">
    {% if items %}
        <table style="width: 100%; text-align: left; border-collapse: collapse;">
            <tr><th>Product</th><th>Price</th><th>Quantity</th><th>Total</th><th>Action</th></tr>
            {% for item in items %}
            <tr style="border-bottom: 1px solid #ccc;">
                <td style="padding: 1rem 0;">{{ item.product.name }}</td>
                <td>${{ "%.2f"|format(item.product.price) }}</td>
                <td>{{ item.quantity }}</td>
                <td>${{ "%.2f"|format(item.product.price * item.quantity) }}</td>
                <td><a href="{{ url_for('main.remove_from_cart', item_id=item.id) }}" class="btn btn-outline btn-sm">Remove</a></td>
            </tr>
            {% endfor %}
        </table>
        <div style="text-align: right; margin-top: 2rem;">
            <h3>Total: ${{ "%.2f"|format(total) }}</h3>
            <a href="{{ url_for('main.checkout') }}" class="btn btn-primary btn-large">Proceed to Checkout</a>
        </div>
    {% else %}
        <div style="text-align: center;">
            <h2>Your cart is empty</h2>
            <a href="{{ url_for('main.products') }}" class="btn btn-primary">Continue Shopping</a>
        </div>
    {% endif %}
</div>
{% endblock %}"""

checkout_html = """{% extends "base.html" %}
{% block content %}
<div class="page-header"><h1>Checkout</h1></div>
<div class="container" style="max-width: 600px; margin: 0 auto; padding: 2rem;">
    <h3>Order Summary</h3>
    <ul>
        {% for item in items %}
        <li>{{ item.product.name }} x {{ item.quantity }} - ${{ "%.2f"|format(item.product.price * item.quantity) }}</li>
        {% endfor %}
    </ul>
    <h2>Total: ${{ "%.2f"|format(total) }}</h2>
    <hr>
    <form method="POST">
        <h3>Shipping Information</h3>
        <input type="text" placeholder="Full Name" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        <input type="text" placeholder="Address" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        <select required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
            <option value="cod">Cash on Delivery</option>
            <option value="demo">Demo Card</option>
        </select>
        <button type="submit" class="btn btn-primary btn-large" style="width: 100%;">Place Order</button>
    </form>
</div>
{% endblock %}"""

orders_html = """{% extends "base.html" %}
{% block content %}
<div class="page-header"><h1>My Orders</h1></div>
<div class="container" style="max-width: 800px; margin: 0 auto; padding: 2rem;">
    {% if orders %}
        <table style="width: 100%; text-align: left; border-collapse: collapse;">
            <tr><th>Order ID</th><th>Date</th><th>Total</th><th>Status</th></tr>
            {% for order in orders %}
            <tr style="border-bottom: 1px solid #ccc;">
                <td style="padding: 1rem 0;">#{{ order.id }}</td>
                <td>{{ order.created_at.strftime('%Y-%m-%d') }}</td>
                <td>${{ "%.2f"|format(order.total) }}</td>
                <td>{{ order.status }}</td>
            </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>You have no orders yet.</p>
    {% endif %}
</div>
{% endblock %}"""

profile_html = """{% extends "base.html" %}
{% block content %}
<div class="page-header"><h1>Profile</h1></div>
<div class="container" style="max-width: 600px; margin: 0 auto; padding: 2rem;">
    <form method="POST">
        <label>Username (cannot be changed)</label>
        <input type="text" value="{{ user.username }}" disabled style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        
        <label>Full Name</label>
        <input type="text" name="name" value="{{ user.name }}" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        
        <label>Email</label>
        <input type="email" name="email" value="{{ user.email }}" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        
        <button type="submit" class="btn btn-primary">Update Profile</button>
    </form>
</div>
{% endblock %}"""

login_html = """{% extends "base.html" %}
{% block content %}
<div style="max-width: 400px; margin: 4rem auto; text-align: center;">
    <h2>Welcome back</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        <input type="password" name="password" placeholder="Password" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        <button type="submit" class="btn btn-primary" style="width: 100%;">Login</button>
    </form>
</div>
{% endblock %}"""

register_html = """{% extends "base.html" %}
{% block content %}
<div style="max-width: 400px; margin: 4rem auto; text-align: center;">
    <h2>Create Account</h2>
    <form method="POST">
        <input type="text" name="name" placeholder="Full Name" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        <input type="email" name="email" placeholder="Email" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        <input type="text" name="username" placeholder="Username" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        <input type="password" name="password" placeholder="Password" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        <input type="password" name="confirm_password" placeholder="Confirm Password" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        <button type="submit" class="btn btn-primary" style="width: 100%;">Register</button>
    </form>
</div>
{% endblock %}"""

product_detail = """{% extends "base.html" %}
{% block content %}
<div class="container" style="max-width: 1000px; margin: 4rem auto; display: flex; gap: 4rem;">
    <div style="flex: 1; background: #f1f5f9; display: flex; align-items: center; justify-content: center; min-height: 400px; border-radius: 12px; font-size: 6rem; color: #cbd5e1;">
        <i class="fas fa-box"></i>
    </div>
    <div style="flex: 1;">
        <span style="color: var(--secondary); text-transform: uppercase; font-size: 0.8rem; font-weight: 600;">{{ product.category }}</span>
        <h1 style="margin: 0.5rem 0;">{{ product.name }}</h1>
        <div style="color: #fbbf24; margin-bottom: 1rem;"><i class="fas fa-star"></i> {{ product.rating }}</div>
        <h2 style="color: var(--primary); font-size: 2rem; margin-bottom: 1rem;">${{ "%.2f"|format(product.price) }}</h2>
        <p style="color: var(--secondary); margin-bottom: 2rem; line-height: 1.6;">{{ product.description }}</p>
        <p><strong>Stock:</strong> {{ product.stock }} available</p>
        
        <form action="{{ url_for('main.add_to_cart', product_id=product.id) }}" method="POST" style="display: flex; gap: 1rem; margin-top: 2rem;">
            <input type="number" name="quantity" value="1" min="1" max="{{ product.stock }}" style="width: 80px; padding: 0.5rem; border-radius: 6px; border: 1px solid #ccc;">
            <button type="submit" class="btn btn-primary btn-large">Add to Cart</button>
        </form>
    </div>
</div>
{% endblock %}"""

products_html = """{% extends "base.html" %}
{% block content %}
<div class="page-header">
    <h1>All Products</h1>
</div>
<div class="product-layout">
    <aside class="sidebar">
        <h3>Categories</h3>
        <ul style="list-style: none; padding: 0; margin-top: 1rem;">
            <li><a href="{{ url_for('main.products') }}" style="color: var(--secondary); text-decoration: none;">All Categories</a></li>
            {% for cat in categories %}
            <li style="margin-top: 0.5rem;"><a href="{{ url_for('main.products', category=cat) }}" style="color: var(--secondary); text-decoration: none;">{{ cat }}</a></li>
            {% endfor %}
        </ul>
    </aside>
    <div class="products-main">
        <div class="products-toolbar">
            <form class="search-bar" action="{{ url_for('main.products') }}" method="GET" style="display: flex; gap: 0.5rem;">
                <input type="text" name="search" placeholder="Search products..." value="{{ search or '' }}" style="padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;">
                <button type="submit" class="btn btn-primary"><i class="fas fa-search"></i></button>
            </form>
            <div class="sort-by">
                <form action="{{ url_for('main.products') }}" method="GET">
                    <select name="sort" onchange="this.form.submit()" style="padding: 0.5rem; border-radius: 4px;">
                        <option value="">Sort by: Newest</option>
                        <option value="price_low">Price: Low to High</option>
                        <option value="price_high">Price: High to Low</option>
                    </select>
                </form>
            </div>
        </div>
        <div class="product-grid">
            {% for product in products %}
            <div class="product-card">
                <div class="product-image-placeholder">
                    <i class="fas fa-box"></i>
                </div>
                <div class="product-info">
                    <span class="product-category">{{ product.category }}</span>
                    <h3 class="product-title">{{ product.name }}</h3>
                    <div class="product-rating">
                        <i class="fas fa-star"></i> {{ product.rating }}
                    </div>
                    <div class="product-bottom">
                        <span class="product-price">${{ "%.2f"|format(product.price) }}</span>
                        <a href="{{ url_for('main.product_detail', id=product.id) }}" class="btn btn-outline btn-sm">View</a>
                        <form action="{{ url_for('main.add_to_cart', product_id=product.id) }}" method="POST" style="display:inline;">
                            <input type="hidden" name="quantity" value="1">
                            <button type="submit" class="btn btn-primary btn-sm"><i class="fas fa-cart-plus"></i></button>
                        </form>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="empty-state">
                <h2>No products found</h2>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}"""

order_confirm = """{% extends "base.html" %}
{% block content %}
<div style="text-align: center; padding: 4rem;">
    <h1 style="color: var(--success);"><i class="fas fa-check-circle"></i> Order Confirmed!</h1>
    <h2>Order #{{ order.id }}</h2>
    <p>Thank you for shopping with SecureShop.</p>
    <div style="margin-top: 2rem;">
        <a href="{{ url_for('main.orders') }}" class="btn btn-outline">View Order</a>
        <a href="{{ url_for('main.products') }}" class="btn btn-primary">Continue Shopping</a>
    </div>
</div>
{% endblock %}"""

write_file(f"{base_dir}/templates/base.html", base_html)
write_file(f"{base_dir}/templates/404.html", error_404)
write_file(f"{base_dir}/templates/403.html", error_403)
write_file(f"{base_dir}/templates/500.html", error_500)
write_file(f"{base_dir}/templates/cart.html", cart_html)
write_file(f"{base_dir}/templates/checkout.html", checkout_html)
write_file(f"{base_dir}/templates/orders.html", orders_html)
write_file(f"{base_dir}/templates/profile.html", profile_html)
write_file(f"{base_dir}/templates/login.html", login_html)
write_file(f"{base_dir}/templates/register.html", register_html)
write_file(f"{base_dir}/templates/product_detail.html", product_detail)
write_file(f"{base_dir}/templates/products.html", products_html)
write_file(f"{base_dir}/templates/order_confirmation.html", order_confirm)
print("Frontend templates injected successfully")

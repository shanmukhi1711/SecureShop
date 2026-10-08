import os

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
                    <a href="#" class="nav-icon"><i class="fas fa-shopping-cart"></i> Cart</a>
                    <a href="#" class="nav-icon"><i class="fas fa-user"></i> Profile</a>
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

index_html = """{% extends "base.html" %}

{% block content %}
<section class="hero">
    <div class="hero-content">
        <h1>Smart Shopping. Secure by Design.</h1>
        <p>Discover premium products with industry-leading security and privacy protection.</p>
        <div class="hero-buttons">
            <a href="{{ url_for('main.products') }}" class="btn btn-primary btn-large">Shop Now</a>
            <a href="{{ url_for('main.products') }}" class="btn btn-outline btn-large">Explore Products</a>
        </div>
    </div>
</section>

<section class="featured-products">
    <div class="section-header">
        <h2>FEATURED PRODUCTS</h2>
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
                    <button class="btn btn-primary btn-sm"><i class="fas fa-cart-plus"></i></button>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</section>

<section class="features-section">
    <div class="section-header">
        <h2>WHY SECURESHOP?</h2>
    </div>
    <div class="features-grid">
        <div class="feature-card">
            <i class="fas fa-shield-alt feature-icon"></i>
            <h3>Secure Accounts</h3>
            <p>Enterprise-grade security protecting your data.</p>
        </div>
        <div class="feature-card">
            <i class="fas fa-gem feature-icon"></i>
            <h3>Quality Products</h3>
            <p>Curated selection of premium items.</p>
        </div>
        <div class="feature-card">
            <i class="fas fa-shipping-fast feature-icon"></i>
            <h3>Fast Ordering</h3>
            <p>Seamless checkout experience.</p>
        </div>
        <div class="feature-card">
            <i class="fas fa-lock feature-icon"></i>
            <h3>Security Tested</h3>
            <p>Rigorous security standards and testing.</p>
        </div>
    </div>
</section>
{% endblock %}"""

products_html = """{% extends "base.html" %}

{% block content %}
<div class="page-header">
    <h1>All Products</h1>
</div>

<div class="product-layout">
    <aside class="sidebar">
        <h3>Filters</h3>
        <div class="filter-group">
            <h4>Categories</h4>
            <ul>
                <li><a href="#">Electronics</a></li>
                <li><a href="#">Accessories</a></li>
                <li><a href="#">Books</a></li>
            </ul>
        </div>
    </aside>

    <div class="products-main">
        <div class="products-toolbar">
            <div class="search-bar">
                <input type="text" placeholder="Search products...">
                <button class="btn btn-primary"><i class="fas fa-search"></i></button>
            </div>
            <div class="sort-by">
                <select>
                    <option>Sort by: Newest</option>
                    <option>Price: Low to High</option>
                    <option>Price: High to Low</option>
                </select>
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
                        <button class="btn btn-primary btn-sm">Add to Cart</button>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="empty-state">
                <i class="fas fa-box-open empty-icon"></i>
                <h2>No products found</h2>
                <p>Check back later for new arrivals.</p>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}"""

style_css = """
:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary: #475569;
    --bg-color: #f8fafc;
    --surface: #ffffff;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --success: #10b981;
    --error: #ef4444;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
}

body {
    background-color: var(--bg-color);
    color: var(--text-main);
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    color: var(--text-main);
}

/* Navbar */
.navbar {
    background-color: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
    text-decoration: none;
    letter-spacing: -0.5px;
}

.nav-links a {
    text-decoration: none;
    color: var(--secondary);
    margin: 0 1rem;
    font-weight: 500;
    transition: color 0.2s;
}

.nav-links a:hover {
    color: var(--primary);
}

.nav-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.nav-icon {
    text-decoration: none;
    color: var(--secondary);
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.nav-icon:hover {
    color: var(--primary);
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-weight: 500;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 0.95rem;
}

.btn-large {
    padding: 0.75rem 1.5rem;
    font-size: 1.1rem;
}

.btn-sm {
    padding: 0.35rem 0.75rem;
    font-size: 0.85rem;
}

.btn-primary {
    background-color: var(--primary);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-dark);
}

.btn-outline {
    background-color: transparent;
    color: var(--primary);
    border: 1px solid var(--primary);
}

.btn-outline:hover {
    background-color: var(--primary);
    color: white;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, var(--text-main) 0%, #1e293b 100%);
    color: white;
    padding: 6rem 1.5rem;
    text-align: center;
}

.hero h1 {
    color: white;
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}

.hero p {
    font-size: 1.25rem;
    color: #cbd5e1;
    margin-bottom: 2rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.hero-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
}

/* Products Grid */
.section-header {
    text-align: center;
    margin: 4rem 0 2rem;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

.product-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    flex-direction: column;
}

.product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.05);
}

.product-image-placeholder {
    height: 200px;
    background-color: #f1f5f9;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #cbd5e1;
    font-size: 4rem;
}

.product-info {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.product-category {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--secondary);
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.product-title {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    flex-grow: 1;
}

.product-rating {
    color: #fbbf24;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.product-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
}

.product-price {
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--primary);
}

/* Features Section */
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto 4rem;
    padding: 0 1.5rem;
}

.feature-card {
    background: var(--surface);
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    border: 1px solid var(--border);
}

.feature-icon {
    font-size: 2.5rem;
    color: var(--primary);
    margin-bottom: 1rem;
}

.feature-card h3 {
    margin-bottom: 0.5rem;
}

.feature-card p {
    color: var(--secondary);
}

/* Products Page Layout */
.page-header {
    background: var(--surface);
    padding: 3rem 1.5rem;
    text-align: center;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}

.product-layout {
    display: flex;
    max-width: 1200px;
    margin: 0 auto 4rem;
    padding: 0 1.5rem;
    gap: 2rem;
}

.sidebar {
    width: 250px;
    flex-shrink: 0;
}

.products-main {
    flex-grow: 1;
}

.products-toolbar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    background: var(--surface);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
}

/* Footer */
.footer {
    background-color: var(--surface);
    border-top: 1px solid var(--border);
    margin-top: auto;
    padding: 4rem 1.5rem 2rem;
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
}

.footer-bottom {
    text-align: center;
    color: var(--secondary);
    border-top: 1px solid var(--border);
    padding-top: 2rem;
}

/* Utilities */
.flash-messages {
    max-width: 1200px;
    margin: 1rem auto;
    padding: 0 1.5rem;
}

.alert {
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.alert-success { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
.alert-info { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
.alert-error { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }

"""

base_dir = "c:/Users/Sree/SecureShopy"
write_file(f"{base_dir}/templates/base.html", base_html)
write_file(f"{base_dir}/templates/index.html", index_html)
write_file(f"{base_dir}/templates/products.html", products_html)
write_file(f"{base_dir}/static/css/style.css", style_css)
print("UI templates successfully updated!")

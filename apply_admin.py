import os
base_dir = "c:/Users/Sree/SecureShopy"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

admin_base = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - SecureShop</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <style>
        .admin-layout { display: flex; min-height: 100vh; }
        .admin-sidebar { width: 250px; background: #1e293b; color: white; padding: 2rem 1rem; }
        .admin-sidebar a { color: #cbd5e1; display: block; padding: 1rem; text-decoration: none; border-radius: 8px; margin-bottom: 0.5rem; }
        .admin-sidebar a:hover, .admin-sidebar a.active { background: #334155; color: white; }
        .admin-main { flex: 1; padding: 2rem; background: #f8fafc; overflow-y: auto; }
        .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
        .stat-card { background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center; }
        .stat-card h3 { font-size: 2rem; color: var(--primary); margin-top: 0.5rem; }
        .admin-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .admin-table th, .admin-table td { padding: 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; }
        .admin-table th { background: #f1f5f9; font-weight: 600; }
    </style>
</head>
<body>
    <div class="admin-layout">
        <aside class="admin-sidebar">
            <h2 style="padding: 0 1rem; margin-bottom: 2rem; color: white;">Admin Panel</h2>
            <nav>
                <a href="{{ url_for('admin.dashboard') }}"><i class="fas fa-chart-line"></i> Dashboard</a>
                <a href="{{ url_for('admin.products') }}"><i class="fas fa-box"></i> Products</a>
                <a href="{{ url_for('admin.orders') }}"><i class="fas fa-shopping-cart"></i> Orders</a>
                <a href="{{ url_for('main.index') }}"><i class="fas fa-home"></i> Back to Store</a>
            </nav>
        </aside>
        <main class="admin-main">
            <div class="flash-messages">
                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        {% for category, message in messages %}
                            <div class="alert alert-{{ category }}">{{ message }}</div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
            </div>
            {% block content %}{% endblock %}
        </main>
    </div>
</body>
</html>"""

dashboard_html = """{% extends "admin/admin_base.html" %}
{% block content %}
<h2>Dashboard Overview</h2>
<div class="stat-grid" style="margin-top: 1rem;">
    <div class="stat-card">
        <div>Total Users</div>
        <h3>{{ stats.users }}</h3>
    </div>
    <div class="stat-card">
        <div>Total Products</div>
        <h3>{{ stats.products }}</h3>
    </div>
    <div class="stat-card">
        <div>Total Orders</div>
        <h3>{{ stats.orders }}</h3>
    </div>
    <div class="stat-card">
        <div>Revenue</div>
        <h3>${{ "%.2f"|format(stats.revenue) }}</h3>
    </div>
</div>
<h3>Recent Orders</h3>
<table class="admin-table" style="margin-top: 1rem;">
    <tr><th>ID</th><th>Date</th><th>Total</th><th>Status</th></tr>
    {% for order in recent_orders %}
    <tr>
        <td>#{{ order.id }}</td>
        <td>{{ order.created_at.strftime('%Y-%m-%d') }}</td>
        <td>${{ "%.2f"|format(order.total) }}</td>
        <td>{{ order.status }}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}"""

products_html = """{% extends "admin/admin_base.html" %}
{% block content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
    <h2>Manage Products</h2>
    <a href="{{ url_for('admin.add_product') }}" class="btn btn-primary"><i class="fas fa-plus"></i> Add Product</a>
</div>
<table class="admin-table">
    <tr><th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Actions</th></tr>
    {% for product in products %}
    <tr>
        <td>{{ product.id }}</td>
        <td>{{ product.name }}</td>
        <td>{{ product.category }}</td>
        <td>${{ "%.2f"|format(product.price) }}</td>
        <td>{{ product.stock }}</td>
        <td>
            <a href="{{ url_for('admin.edit_product', id=product.id) }}" class="btn btn-outline btn-sm">Edit</a>
            <a href="{{ url_for('admin.delete_product', id=product.id) }}" class="btn btn-outline btn-sm" style="color: red; border-color: red;" onclick="return confirm('Are you sure?')">Delete</a>
        </td>
    </tr>
    {% endfor %}
</table>
{% endblock %}"""

product_form = """{% extends "admin/admin_base.html" %}
{% block content %}
<h2>{{ 'Edit' if product else 'Add' }} Product</h2>
<div style="background: white; padding: 2rem; border-radius: 8px; border: 1px solid #e2e8f0; max-width: 600px; margin-top: 1rem;">
    <form method="POST">
        <label>Product Name</label>
        <input type="text" name="name" value="{{ product.name if product else '' }}" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        
        <label>Category</label>
        <input type="text" name="category" value="{{ product.category if product else '' }}" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        
        <label>Price</label>
        <input type="number" step="0.01" name="price" value="{{ product.price if product else '' }}" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        
        <label>Stock</label>
        <input type="number" name="stock" value="{{ product.stock if product else '0' }}" required style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        
        <label>Rating</label>
        <input type="number" step="0.1" name="rating" value="{{ product.rating if product else '0.0' }}" style="width: 100%; margin-bottom: 1rem; padding: 0.5rem;">
        
        <label>Description</label>
        <textarea name="description" required style="width: 100%; height: 100px; margin-bottom: 1rem; padding: 0.5rem;">{{ product.description if product else '' }}</textarea>
        
        <button type="submit" class="btn btn-primary">Save Product</button>
        <a href="{{ url_for('admin.products') }}" class="btn btn-outline">Cancel</a>
    </form>
</div>
{% endblock %}"""

orders_html = """{% extends "admin/admin_base.html" %}
{% block content %}
<h2>Manage Orders</h2>
<table class="admin-table" style="margin-top: 1rem;">
    <tr><th>ID</th><th>User ID</th><th>Date</th><th>Total</th><th>Status</th><th>Action</th></tr>
    {% for order in orders %}
    <tr>
        <td>#{{ order.id }}</td>
        <td>{{ order.user_id }}</td>
        <td>{{ order.created_at.strftime('%Y-%m-%d') }}</td>
        <td>${{ "%.2f"|format(order.total) }}</td>
        <td>
            <form action="{{ url_for('admin.update_order_status', id=order.id) }}" method="POST" style="display: flex; gap: 0.5rem;">
                <select name="status" style="padding: 0.25rem;">
                    <option value="Processing" {% if order.status == 'Processing' %}selected{% endif %}>Processing</option>
                    <option value="Confirmed" {% if order.status == 'Confirmed' %}selected{% endif %}>Confirmed</option>
                    <option value="Shipped" {% if order.status == 'Shipped' %}selected{% endif %}>Shipped</option>
                    <option value="Delivered" {% if order.status == 'Delivered' %}selected{% endif %}>Delivered</option>
                </select>
                <button type="submit" class="btn btn-primary btn-sm">Update</button>
            </form>
        </td>
        <td>-</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}"""

write_file(f"{base_dir}/templates/admin/admin_base.html", admin_base)
write_file(f"{base_dir}/templates/admin/dashboard.html", dashboard_html)
write_file(f"{base_dir}/templates/admin/products.html", products_html)
write_file(f"{base_dir}/templates/admin/product_form.html", product_form)
write_file(f"{base_dir}/templates/admin/orders.html", orders_html)
print("Admin templates injected successfully")

from flask import Blueprint, render_template, redirect, url_for, flash, request
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
            image_url=request.form.get('image_url') or 'fallback.jpg',
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
        product.image_url = request.form.get('image_url') or product.image_url
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

@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.order_by(User.id.asc()).all()
    return render_template('admin/users.html', users=all_users)

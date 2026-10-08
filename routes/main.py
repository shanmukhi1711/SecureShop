from flask import Blueprint, render_template, redirect, url_for, flash, request
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

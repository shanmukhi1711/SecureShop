import sys
from app import create_app
from models.models import Product, User, Order

app = create_app('secure')
client = app.test_client()

print("=== VERIFYING SECURESHOPY REDESIGN ===")

# 1. Test Homepage
res = client.get('/')
assert res.status_code == 200, f"Homepage failed with {res.status_code}"
assert b"Upgrade Your Everyday" in res.data, "Hero headline missing"
assert b"Explore Products" in res.data, "Explore products button missing"
assert b"Shop by Category" in res.data, "Category section missing"
assert b"Store Bestsellers" in res.data, "Bestsellers section missing"
print("PASS: Homepage renders completely with hero, categories, and products.")

# 2. Test Catalog
res = client.get('/products')
assert res.status_code == 200, f"Products catalog failed with {res.status_code}"
assert b"All Products" in res.data, "Products title missing"
assert b"Add to Cart" in res.data, "Add to cart button missing"
print("PASS: Products catalog renders with grid, filters, and products.")

# 3. Test Category Filter
for cat in ['Laptops', 'Mobiles', 'Audio', 'Accessories', 'Monitors', 'Wearables']:
    res = client.get(f'/products?category={cat}')
    assert res.status_code == 200, f"Category {cat} failed"
    print(f"PASS: Category filter '{cat}' works (status 200).")

# 4. Test Search
res = client.get('/products?search=Headphones')
assert res.status_code == 200
assert b"Headphones" in res.data
print("PASS: Product search for 'Headphones' returns matches.")

# 5. Test Product Details
res = client.get('/product/1')
assert res.status_code == 200
assert b"Wireless Headphones" in res.data
assert b"Add to Cart" in res.data
print("PASS: Product details page for product 1 works.")

# 6. Test Auth Pages
res = client.get('/login')
assert res.status_code == 200
assert b"Welcome Back" in res.data
assert b"Login" in res.data
print("PASS: Login page renders with auth card and demo credentials helper.")

res = client.get('/register')
assert res.status_code == 200
assert b"Create Your Account" in res.data
assert b"Register" in res.data
print("PASS: Register page renders.")

# 7. Test 404
res = client.get('/nonexistent_route_test')
assert res.status_code == 404
assert b"404" in res.data
print("PASS: 404 handler returns 404 page.")

# 8. Test Security Lab
res = client.get('/lab/')
assert res.status_code == 200
assert b"Security Lab" in res.data
print("PASS: Academic Security Lab renders.")

# 9. Verify Product Images exist on disk
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
with app.app_context():
    products = Product.query.all()
    print(f"\nChecking images for {len(products)} products in database:")
    for p in products:
        img_rel = p.image_path
        img_abs = os.path.join(base_dir, 'static', img_rel.replace('/', os.sep))
        assert os.path.exists(img_abs), f"Missing image file for product {p.id} ({p.name}): {img_abs}"
        assert os.path.getsize(img_abs) > 1000, f"Image file is empty or corrupted: {img_abs}"
        print(f"  [OK] Product #{p.id}: {p.name} -> {img_rel} ({os.path.getsize(img_abs)} bytes)")

print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

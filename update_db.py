import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'secureshop.db')

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Check existing products
cur.execute("SELECT id, name, category, price, stock, image_url FROM product")
existing_products = cur.fetchall()
print(f"Existing products in DB: {len(existing_products)}")

# Update existing 12 products
updates = [
    (1, 'Wireless Headphones', 'Audio', 4999.0, 'headphones.jpg', 4.8),
    (2, 'Mechanical Keyboard', 'Accessories', 3499.0, 'keyboard.jpg', 4.7),
    (3, 'Smart Watch', 'Wearables', 14999.0, 'smartwatch.jpg', 4.6),
    (4, 'USB-C Hub', 'Accessories', 1899.0, 'usbc_hub.jpg', 4.5),
    (5, 'Laptop Stand', 'Accessories', 1299.0, 'laptop_stand.jpg', 4.4),
    (6, 'Bluetooth Speaker', 'Audio', 2999.0, 'speaker.jpg', 4.3),
    (7, 'Gaming Mouse', 'Accessories', 2499.0, 'mouse.jpg', 4.7),
    (8, 'Premium Backpack', 'Accessories', 2199.0, 'backpack.jpg', 4.6),
    (9, 'Desk Lamp', 'Accessories', 1499.0, 'lamp.jpg', 4.2),
    (10, 'HD Webcam', 'Accessories', 3299.0, 'webcam.jpg', 4.5),
    (11, 'Power Bank', 'Accessories', 1999.0, 'powerbank.jpg', 4.8),
    (12, 'Python Programming Book', 'Accessories', 899.0, 'python_book.jpg', 4.9)
]

for p_id, name, cat, price, img, rating in updates:
    cur.execute("""
        UPDATE product 
        SET category = ?, price = ?, image_url = ?, rating = ?
        WHERE id = ?
    """, (cat, price, img, rating, p_id))

# New products to insert if they don't already exist
new_products = [
    (13, 'UltraBook Pro 15', 'High-performance 15.6-inch aluminum ultrabook with 16-core processor, 16GB RAM, and 1TB NVMe SSD.', 89999.0, 'Laptops', 25, 'laptop.jpg', 4.9),
    (14, 'Galaxy S24 Ultra Smartphone', 'Next-generation AI flagship smartphone with titanium frame, 200MP camera, and Dynamic AMOLED 2X display.', 119999.0, 'Mobiles', 35, 'smartphone.jpg', 4.9),
    (15, 'Pro True Wireless Earbuds', 'Active Noise Cancellation earbuds with personalized spatial audio, transparency mode, and 30-hour battery case.', 8999.0, 'Audio', 45, 'earbuds.jpg', 4.8),
    (16, 'UltraWide 4K Gaming Monitor 34"', '34-inch curved ultra-wide gaming monitor with 144Hz refresh rate, 1ms response time, and HDR 400 support.', 42999.0, 'Monitors', 20, 'monitor.jpg', 4.8),
    (17, 'Pro Mirrorless 4K Camera', 'Compact mirrorless camera with 24.2MP full-frame sensor, 4K60p video recording, and real-time subject tracking autofocus.', 64999.0, 'Accessories', 15, 'camera.jpg', 4.9),
    (18, 'UltraPad Pro 11-inch Tablet', 'Liquid Retina display tablet with high-speed octa-core chip, stylus support, and all-day battery life.', 54999.0, 'Mobiles', 30, 'tablet.jpg', 4.8),
    (19, 'RGB Gaming Headset & Stand', 'Immersive 7.1 surround sound gaming headset with noise-canceling microphone and matching RGB headset stand.', 5499.0, 'Accessories', 40, 'gaming_accessories.jpg', 4.7),
    (20, 'Apple MacBook Air 15" M3', 'Incredibly thin and fast laptop with Apple M3 chip, Liquid Retina display, and 18 hours of battery life.', 124990.0, 'Laptops', 18, 'macbook.jpg', 5.0)
]

for p in new_products:
    cur.execute("SELECT id FROM product WHERE id = ? OR name = ?", (p[0], p[1]))
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO product (id, name, description, price, category, stock, image_url, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, p)
        print(f"Inserted: {p[1]}")
    else:
        print(f"Already exists: {p[1]}")

conn.commit()

# Verify
cur.execute("SELECT id, name, category, price, image_url FROM product")
rows = cur.fetchall()
print(f"\nTotal products in DB now: {len(rows)}")
for r in rows:
    print(r)

conn.close()

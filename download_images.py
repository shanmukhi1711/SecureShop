import os
import urllib.request
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
products_dir = os.path.join(base_dir, 'static', 'images', 'products')
categories_dir = os.path.join(base_dir, 'static', 'images', 'categories')
images_dir = os.path.join(base_dir, 'static', 'images')

os.makedirs(products_dir, exist_ok=True)
os.makedirs(categories_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

images_to_download = {
    # Products
    os.path.join(products_dir, 'headphones.jpg'): 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
    os.path.join(products_dir, 'keyboard.jpg'): 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80',
    os.path.join(products_dir, 'smartwatch.jpg'): 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
    os.path.join(products_dir, 'usbc_hub.jpg'): 'https://images.unsplash.com/photo-1544652478-6653e09f18a2?w=800&q=80',
    os.path.join(products_dir, 'laptop_stand.jpg'): 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&q=80',
    os.path.join(products_dir, 'speaker.jpg'): 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&q=80',
    os.path.join(products_dir, 'mouse.jpg'): 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80',
    os.path.join(products_dir, 'backpack.jpg'): 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=80',
    os.path.join(products_dir, 'lamp.jpg'): 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80',
    os.path.join(products_dir, 'webcam.jpg'): 'https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=800&q=80',
    os.path.join(products_dir, 'powerbank.jpg'): 'https://images.unsplash.com/photo-1609592807906-8d48a1d7f642?w=800&q=80',
    os.path.join(products_dir, 'python_book.jpg'): 'https://images.unsplash.com/photo-1532012164546-f432f2e3777a?w=800&q=80',
    os.path.join(products_dir, 'laptop.jpg'): 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80',
    os.path.join(products_dir, 'smartphone.jpg'): 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=80',
    os.path.join(products_dir, 'earbuds.jpg'): 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80',
    os.path.join(products_dir, 'monitor.jpg'): 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80',
    os.path.join(products_dir, 'camera.jpg'): 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&q=80',
    os.path.join(products_dir, 'tablet.jpg'): 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&q=80',
    os.path.join(products_dir, 'gaming_accessories.jpg'): 'https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=800&q=80',
    os.path.join(products_dir, 'macbook.jpg'): 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&q=80',

    # Categories
    os.path.join(categories_dir, 'laptops.jpg'): 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&q=80',
    os.path.join(categories_dir, 'mobiles.jpg'): 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&q=80',
    os.path.join(categories_dir, 'audio.jpg'): 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80',
    os.path.join(categories_dir, 'accessories.jpg'): 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&q=80',
    os.path.join(categories_dir, 'monitors.jpg'): 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&q=80',
    os.path.join(categories_dir, 'wearables.jpg'): 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80',

    # Hero & Fallback
    os.path.join(images_dir, 'hero.jpg'): 'https://images.unsplash.com/photo-1468495244123-6c6c332eeede?w=1600&q=85',
    os.path.join(images_dir, 'promo_banner.jpg'): 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1400&q=85',
    os.path.join(images_dir, 'fallback.jpg'): 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=600&q=80',
}

def download_file(target_path, url):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 5000:
        print(f"Already exists: {os.path.basename(target_path)} ({os.path.getsize(target_path)} bytes)")
        return True
    print(f"Downloading: {os.path.basename(target_path)}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response, open(target_path, 'wb') as out_file:
            out_file.write(response.read())
        size = os.path.getsize(target_path)
        print(f"Saved {os.path.basename(target_path)} ({size} bytes)")
        return True
    except Exception as e:
        print(f"Failed to download {os.path.basename(target_path)}: {e}")
        return False

success_count = 0
for target, url in images_to_download.items():
    if download_file(target, url):
        success_count += 1
    time.sleep(0.1)

print(f"\nDone! Downloaded/Verified {success_count}/{len(images_to_download)} images.")

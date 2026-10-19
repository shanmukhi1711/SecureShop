import os
import shutil
import urllib.request

base_dir = os.path.dirname(os.path.abspath(__file__))
products_dir = os.path.join(base_dir, 'static', 'images', 'products')
categories_dir = os.path.join(base_dir, 'static', 'images', 'categories')
images_dir = os.path.join(base_dir, 'static', 'images')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

remaining = {
    os.path.join(products_dir, 'powerbank.jpg'): 'https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800&q=80',
    os.path.join(products_dir, 'python_book.jpg'): 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&q=80',
    os.path.join(images_dir, 'hero.jpg'): 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1600&q=85'
}

for path, url in remaining.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp, open(path, 'wb') as f:
            f.write(resp.read())
        print(f"Downloaded {os.path.basename(path)}: {os.path.getsize(path)} bytes")
    except Exception as e:
        print(f"Error {path}: {e}")

# Copy monitor to categories/monitors.jpg if needed
monitors_cat = os.path.join(categories_dir, 'monitors.jpg')
monitor_prod = os.path.join(products_dir, 'monitor.jpg')
if os.path.exists(monitor_prod) and not os.path.exists(monitors_cat):
    shutil.copyfile(monitor_prod, monitors_cat)
    print(f"Copied {monitor_prod} to {monitors_cat}")

print("Check completed.")

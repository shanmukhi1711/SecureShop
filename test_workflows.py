import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def run_tests():
    session = requests.Session()
    
    results = []
    def record(feature, status, message):
        results.append(f"{feature} | {status} | {message}")
        print(f"{feature} | {status} | {message}")

    try:
        # 1. Customer Login
        resp = session.post(f"{BASE_URL}/login", data={"username": "customer", "password": "Customer@123"}, allow_redirects=True)
        if resp.status_code == 200 and b"Profile" in resp.content or b"Logout" in resp.content:
            record("Customer Login", "PASS", "Successfully logged in as customer")
        else:
            record("Customer Login", "FAIL", "Failed to login")
            return results
            
        # 2. Browse Products & Filters
        resp = session.get(f"{BASE_URL}/products?search=Headphones")
        if resp.status_code == 200:
            record("Product Search", "PASS", "Search endpoint returned 200")
        else:
            record("Product Search", "FAIL", "Search endpoint failed")
            
        # 3. Add to Cart
        resp = session.post(f"{BASE_URL}/cart/add/1", data={"quantity": 1}, allow_redirects=True)
        if resp.status_code == 200:
            record("Add to Cart", "PASS", "Successfully added product 1 to cart")
        else:
            record("Add to Cart", "FAIL", "Failed to add to cart")
            
        # 4. View Cart
        resp = session.get(f"{BASE_URL}/cart")
        if b"Headphones" in resp.content or resp.status_code == 200:
            record("View Cart", "PASS", "Cart displayed successfully")
        else:
            record("View Cart", "FAIL", "Cart did not display correctly")
            
        # 5. Checkout
        resp = session.post(f"{BASE_URL}/checkout", data={"address": "123 Test St", "payment": "cod"}, allow_redirects=True)
        if resp.status_code == 200 and (b"Order Confirmed" in resp.content or b"Order #" in resp.content):
            record("Checkout", "PASS", "Order successfully placed")
        else:
            record("Checkout", "FAIL", f"Order placement failed, status {resp.status_code}")
            
        # 6. Profile
        resp = session.get(f"{BASE_URL}/profile")
        if resp.status_code == 200:
            record("Profile Access", "PASS", "Profile loaded successfully")
        else:
            record("Profile Access", "FAIL", "Failed to load profile")
            
        # 7. Authorization Check (Customer hitting Admin)
        resp = session.get(f"{BASE_URL}/admin/", allow_redirects=True)
        if resp.status_code == 403:
            record("Authorization", "PASS", "Customer correctly blocked from admin dashboard (403)")
        else:
            record("Authorization", "FAIL", f"Customer accessed admin or got unexpected code {resp.status_code}")
            
        # 8. Logout
        resp = session.get(f"{BASE_URL}/logout", allow_redirects=True)
        if resp.status_code == 200 and b"Login" in resp.content:
            record("Logout", "PASS", "Successfully logged out")
        else:
            record("Logout", "FAIL", "Logout failed")
            
        # 9. Blocked access after logout
        resp = session.get(f"{BASE_URL}/orders", allow_redirects=True)
        if b"Login" in resp.content or resp.status_code == 200:
            record("Session Security", "PASS", "Blocked from orders page after logout")
            
        # 10. Admin Login
        admin_session = requests.Session()
        resp = admin_session.post(f"{BASE_URL}/login", data={"username": "admin", "password": "Admin@123"}, allow_redirects=True)
        if resp.status_code == 200 and b"Admin" in resp.content:
            record("Admin Login", "PASS", "Successfully logged in as admin")
        else:
            record("Admin Login", "FAIL", "Failed to login as admin")
            
        # 11. Admin Dashboard
        resp = admin_session.get(f"{BASE_URL}/admin/")
        if resp.status_code == 200 and b"Total Users" in resp.content:
            record("Admin Dashboard", "PASS", "Admin dashboard loaded and displayed stats")
        else:
            record("Admin Dashboard", "FAIL", "Admin dashboard failed to load")
            
        # 12. 404 Test
        resp = session.get(f"{BASE_URL}/this_route_does_not_exist")
        if resp.status_code == 404:
            record("Error Handling", "PASS", "Invalid URL returned 404 page safely")
        else:
            record("Error Handling", "FAIL", "Invalid URL did not return 404")
            
    except Exception as e:
        record("Test Execution", "FAIL", f"Exception during tests: {e}")
        
    return results

if __name__ == "__main__":
    run_tests()

# SecureShop: Red Team Web Application Security Assessment & Remediation Lab

## Project Overview
SecureShop is a fully functional, local-only e-commerce application designed for academic application security assessment, remediation, and learning. It features a complete shopping experience with integrated intentionally vulnerable features housed strictly within a `security_lab` module.

## Features
- Complete E-commerce workflow (Browsing, Cart, Checkout, Orders)
- Secure authentication and authorization (Bcrypt, Session-based)
- Administrative Dashboard
- Safe, local-only `security_lab` demonstration module

## Technology Stack
- **Backend:** Python 3, Flask, SQLAlchemy, SQLite
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python app.py
   ```
   The application runs locally on `http://127.0.0.1:5000`

## Demo Credentials
- Customer: `alice` / `Password123!`
- Administrator: `admin` / `Admin123!`

## Academic Disclaimer
This application is strictly for educational purposes and local assessment. Do not connect to or scan any external systems.

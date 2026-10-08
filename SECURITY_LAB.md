# SecureShop: Red Team Web Application Security Assessment & Remediation Lab

## Project Overview

SecureShop is a local-only e-commerce web application developed for an academic **Red Team Web Application Security Assessment and Remediation** project.

The project follows the security assessment lifecycle:

**Build → Attack → Identify → Fix → Retest**

It provides a realistic e-commerce workflow that can be tested locally using security assessment tools such as OWASP ZAP.

## Features

* User registration and login
* Secure password hashing
* Product browsing and search
* Category filtering and sorting
* Product details
* Shopping cart
* Checkout with demo payment options
* Order placement and order history
* User profile management
* Admin dashboard
* Product management
* User management
* Order management
* Role-based authorization
* Custom 404, 403, and 500 error pages
* Local security demonstration module

## Technology Stack

### Backend

* Python 3
* Flask
* Flask-Login
* SQLAlchemy
* SQLite

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5

### Security Testing

* OWASP ZAP
* Localhost testing environment

## Installation

Clone the repository:

```bash
git clone https://github.com/shanmukhi1711/SecureShop.git
cd SecureShop
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The application is designed to run locally for academic security testing.

## Test Accounts

The application contains separate customer and administrator roles for testing authentication and authorization.

For security reasons, working passwords should not be stored in the public repository. Use the credentials configured locally in the development environment.

## Security Assessment

The application is intended to support an academic security assessment covering areas such as:

* Broken Access Control
* Injection
* Security Misconfiguration
* Vulnerable and Outdated Components
* Authentication and Authorization
* Security Logging and Monitoring

The `security_lab/` directory contains the project's documented security-testing demonstrations.

## Testing Workflow

The project follows:

1. Build the application
2. Run the application locally
3. Perform security assessment
4. Identify vulnerabilities
5. Document evidence and impact
6. Apply remediation
7. Retest the application
8. Compare the security posture before and after remediation

## Academic Disclaimer

SecureShop is strictly intended for **educational and authorized local testing purposes**.

The application should only be run and assessed on systems you own or have explicit permission to test.

Do not deploy or scan this application against public, production, university, or third-party systems without authorization.


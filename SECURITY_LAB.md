# Security Lab Documentation

## Project Overview
SecureShop is an academic Red Team / Application Security laboratory. The application runs strictly on `http://127.0.0.1:5000` and simulates an e-commerce platform for security analysis and remediation.

## Scope
**Authorized Target:** `http://127.0.0.1:5000`
No external systems, production APIs, or university infrastructure are within scope.

## OWASP Mapping

| ID | Category | Finding | Location | Impact | Remediation |
|---|---|---|---|---|---|
| A01 | Broken Access Control | Admin endpoints accessible | /admin | High | Implemented @admin_required |
| A03 | Injection | SQLi in search | /search | High | Used parameterized SQLAlchemy queries |
| A05 | Security Misconfiguration | Debug mode on | Config | Medium | Disabled DEBUG in secure config |
| A06 | Vulnerable Components | Outdated Flask | requirements | Low | Updated to latest secure versions |

## ZAP Testing Procedure
Use OWASP ZAP to spider and active scan the local instance only (`http://127.0.0.1:5000`).

- **Scan Target:** `http://127.0.0.1:5000`
- **Scan Type:** Active Scan
- **Authentication:** Use demo credentials for authenticated surface area testing.

## Remediation Methodology
1. **Identify Finding:** Confirm vulnerability with ZAP or manual testing.
2. **Root Cause Analysis:** Locate the vulnerable code snippet.
3. **Remediate:** Implement secure coding practices (e.g., parameterized queries, proper authorization decorators).
4. **Retest:** Rerun ZAP scan or manual payload to confirm the vulnerability is mitigated.
